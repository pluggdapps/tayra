# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

import re
from   copy                     import deepcopy

from   zope.component           import getGlobalSiteManager
from   zope.interface           import implements

from   tayra.interfaces         import ITayraTag

gsm = getGlobalSiteManager()

class Context( object ):
    def __init__( self, htmlindent=u'' ):
        self.htmlindent = htmlindent

class TagPlugin( object ):
    implements( ITayraTag )

    def dotag( self, node, igen, *args, **kwargs ):
        has_exprs = False
        specifiers, style, attributes = node.specifiers, node.style, node.attributes
        spectext  = specifiers and specifiers.spectext or u''
        styletext = style and style.styletext
        attrslist = attributes and attributes.attrslist

        items = []      # Items to stack-compute

        # Tagname 
        tagopen = node.TAGOPEN.dump(None)
        tagnm   = self.maketagname( tagopen.strip(' \t\r\n')[1:] )

        # Specifier
        if spectext :           # Static specifier content
            tagspec = self.handle_specifiers( spectext )
            fnspec, astext = lambda : igen.putattrs( attrstext=tagspec ), False
        elif specifiers :       # Dynamic specifier content
            fnspec, astext = lambda : specifiers.generate(igen, *args, **kwargs), True
            has_exprs = True
        else :                  # Empty specifier, by call them anyhow
            tagspec = self.handle_specifiers( spectext )
            fnspec, astext = lambda : igen.puttext( tagspec ), True
        items.append( (fnspec, astext) )

        # Style
        if styletext :          # Static style content
            tagstyle = 'style="%s"' % self.handle_style(styletext)
            fnstyle, astext = lambda : igen.puttext( tagstyle ), False
        elif style :            # Dynamic style content
            fnstyle, astext = lambda : style.generate( igen, *args, **kwargs ), True
            has_exprs = True
        else :
            tagstyle = u''
            fnstyle, astext = lambda : igen.puttext( tagstyle ), True
        items.append( (fnstyle, astext) )

        # Attributes
        if attrslist :              # Static attribute content
            tagattrs = self.handle_attributes( attrslist )
            fnattrs = lambda : igen.puttext( tagattrs )
        elif attributes :           # Dynamic attribute content
            fnattrs = lambda : attributes.generate(igen, *args, **kwargs)
            has_exprs = True
        else :
            tagattrs = u''
            fnattrs = lambda : igen.puttext( tagattrs )
        items.append( (fnattrs, False) )# pop-out as list
    
        igen.puttext( tagnm )
        if has_exprs == False : # Tag definition is fully static
            tagdef = u'<' + tagnm + u' ' + u' '.join(filter(None, [tagspec,tagstyle,tagattrs]))
            tagdef += node.TAGEND and node.TAGEND.dump(None) or u''
            tagdef += node.TAGCLOSE and node.TAGCLOSE.dump(None) or u''
            igen.puttext( tagdef )
        else :
            node.TAGOPEN.generate( igen, *args, **kwargs )
            [ node.stackcompute(igen, fn, astext=astext) for fn, astext in items ]
            node.TAGEND and node.TAGEND.generate( igen, *args, **kwargs )
            node.TAGCLOSE and node.TAGCLOSE.generate( igen, *args, **kwargs )
        igen.puttext( self.handle_tagclose(tagnm) if node.TAGCLOSE else u'' )
        return has_exprs

    def dotagline( self, node, igen, pruneinner, handletag,
                          *args, **kwargs ):
        """Do the actual tag-line, but don't handle the tagline during runtime,
        for taglines that are children to tagblocks, because for tagblocks the
        runtime handling must be deferred after the siblings are also populated
        in the stack.  If prune syntax is detected, do that before doing
        anything.
        """
        node._pruneinner() if pruneinner else None
        # Generate indentation of tagline
        igen.comment( node.dump( Context() ))
        igen.indent()

        igen.pushbuf()      # Push tag element
        self.dotag( node.tag, igen, *args, **kwargs )
        igen.pushbuf()      # Push tag content
        node.content.generate( igen, *args, **kwargs ) if node.content else None
        igen.handletag() if handletag else None
        # Remaining nodes
        node.NEWLINES and node.NEWLINES.generate( igen, *args, **kwargs )
        node.dirtyblocks and node.dirtyblocks.generate( igen, *args, **kwargs )

    #---- ITayraTag interface methods

    def headpass1( self, node, igen ):
        return True

    def headpass2( self, node, igen ):
        return True

    def generate_tagline( self, node, igen, *args, **kwargs ):
        self.dotagline( node, igen, node.tag.pruneinner, True, *args, **kwargs )

    def generate_tagblock( self, node, igen, *args, **kwargs ):
        tagline = node.tagline
        pruneindent = tagline.tag.pruneindent
        pruneinner = tagline.tag.pruneinner or pruneindent
        self.dotagline( tagline, igen, pruneinner, False, *args, **kwargs )

        # siblings
        if pruneindent != True :
            igen.upindent( up=node.INDENT.dump(None) )
        node.siblings.generate( igen, *args, **kwargs )
        if pruneindent != True :
            igen.downindent( down=node.DEDENT.dump(None) )

        # handle tag with siblings
        igen.handletag( indent=(not pruneinner), newline='\n' )

    def tailpass( self, node, igen ):
        return True
    
    def handle( self, mach, tag, contents, indent=False, newline=u'' ):
        A = mach.Attributes
        # Tag definition
        if len(tag) == 7 :
            tagnm, tagopen, spec, style, attr, tagclose, tagfinish = tag
            t = tagopen
            spec  = unicode(spec[0])  if spec and isinstance(spec[0], A) \
                               else self.handle_specifiers(spec)
            style = unicode(style[0]) if style and isinstance(style[0], A) \
                               else self.handle_style(style)
            attr  = unicode(attr[0])  if attr and isinstance(attr[0], A) \
                               else self.handle_attributes(attr)
            style = u'style="%s"' % style if style else style
            t += u' ' + u' '.join(filter(None, [ spec, style, attr, tagclose ]))
        elif len(tag) == 3 :
            tagnm, t, tagfinish = tag
        else :
            raise Exception( 'Tag definition not in the expected format' )
        # Tag content
        t += self.handle_content( u''.join(contents) )
        # Tag close
        t += tagfinish
        return t

    def handle_specifiers( self, spectext ):
        attr, strings, atoms = self.parsespecifiers( spectext or u'' )
        str2attrs = self.specstrings2attrs(strings)
        atom2attrs, leftover = self.specatoms2attrs( atoms if atoms else [] )
        return u' '.join(filter(None, [ attr, str2attrs, atom2attrs ]))

    def handle_style( self, styletext ):
        return u''.join(styletext) if styletext else u''

    def handle_attributes( self, attrslist ):
        return u' '.join(filter( None, attrslist)) if attrslist else u''

    def handle_content( self, text ):
        return text

    def handle_tagclose( self, tagnm ):
        return  '</%s>'%tagnm

    ws = r'[ \r\n\t]*'
    parseexp = re.compile(
        r'(\'[^\']+\'%s)|(\"[^"]+\"%s)|([^" \t\r\n\']+%s)' % (ws,ws,ws)
    )
    skipchar = '" \t\r\n\'#\.:'
    primespec = re.compile(
            r'(\#[^%s]+)|(\.[^%s]+)|(:[^%s]+)' % (skipchar,skipchar,skipchar)
    )
    def parsespecifiers( self, spectext ):
        parsed = self.parseexp.findall( spectext )
        idclass = parsed and parsed[0][-1]
        attr = []
        if idclass and idclass[0] in '#.:' :
            parsed.pop(0)
            primespecs = self.primespec.findall( idclass )
            ids, classes, name = [], [], []
            for id_, cls, nm in primespecs :
                id_ and ids.append(id_) 
                cls and classes.append(cls)
                nm and name.append(nm)
            attr.append( 'id="%s"' % ids[0][1:] if ids else u'' )
            attr.append(
                u'class="%s"' % u''.join(classes)[1:].replace('.',' ') if classes else u''
            )
            attr.append( u'name="%s"' % name[0][1:] if name else u'' )

        strings = filter( None, reduce( lambda x, t : x + list(t[:2]), parsed, [] ))
        atoms   = filter( None, map( lambda t : t[2].strip(), parsed ))
        return u' '.join(attr), strings, atoms

    atom2attr = {
      # global attributes
      'edit'         : 'contenteditable="true"',
      'noedit'       : 'contenteditable="false"',
      'dragcopy'     : 'draggable="true" dragzone="copy"',
      'dragmove'     : 'draggable="true" dragzone="move"',
      'draglink'     : 'draggable="true" dragzone="link"',
      'nodrag'       : 'draggable="false"',
      'hidden'       : 'hidden',
      'spellcheck'   : 'spellcheck="true"',
      'nospellcheck' : 'spellcheck="false"',
      # dir
      'ltr'     : 'dir="ltr"',
      'rtl'     : 'dir="rtl"',
      # atoms
      'disabled': 'disabled="disabled"',
      'checked' : 'checked="checked"',
      'readonly': 'readonly="readonly"',
      'selected': 'selected="selected"',
      'multiple': 'multiple="multiple"',
      'defer'   : 'defer="defer"',
    }
    def specatoms2attrs( self, atoms ):
        attrs, leftover = [], []
        for atom in atoms :
            if atom.startswith( 'key:' ):
                attr = 'accesskey="%s"' % atom.split(':', 1)[1]
            elif atom.startswith( 'tab:' ):
                attr = 'tabindex="%s"' % atom.split(':', 1)[1]
            else :
                attr = self.atom2attr.get( atom, None )
            attrs.append(attr) if attr != None else leftover.append(atom)
        return (u' '.join(attrs), leftover)

    def specstrings2attrs( self, strings ):
        return u' '.join(filter( None, strings ))

    def maketagname( self, tagopen ):
        return tagopen

class HtmlDefault( TagPlugin ):
    """Default handler translates TTL tag-definition to HTML tag, when no
    other matching handler is available.

    * ''edit'' atom translates to //contenteditable="true"//
    * ''noedit'' atom translates to //contenteditable="false"//
    * ''dragcopy'' atom translates to //draggable="true" dragzone="copy"//
    * ''dragmove'' atom translates to //draggable="true" dragzone="move"//
    * ''draglink'' atom translates to //draggable="true" dragzone="link"//
    * ''nodrag'' atom translates to //draggable="false"//
    * ''hidden'' atom translates to //hidden//
    * ''spellcheck'' atom translates to //spellcheck="true"//
    * ''nospellcheck'' atom translates to //spellcheck="false"//
    * ''ltr'' atom translates to //dir="ltr"//
    * ''rtl'' atom translates to //dir="rtl"//
    * ''disabled'' atom translates to //disabled="disabled"//
    * ''checked'' atom translates to //checked="checked"//
    * ''readonly'' atom translates to //readonly="readonly"//
    * ''selected'' atom translates to //selected="selected"//
    * ''multiple'' atom translates to //multiple="multiple"//
    * ''defer'' atom translates to //defer="defer"//
    """
    pluginname = '_default'

gsm.registerUtility( HtmlDefault(), ITayraTag, HtmlDefault.pluginname )
