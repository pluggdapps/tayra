import re
from   copy                     import deepcopy

from   zope.interface           import implements
from   zope.component           import getGlobalSiteManager

from   tayra.ttl.interfaces     import ITayraTag

gsm = getGlobalSiteManager()

class Context( object ):
    def __init__( self, htmlindent='' ):
        self.htmlindent = htmlindent

class TagPlugin( object ):
    implements( ITayraTag )

    def dotag( self, node, igen, *args, **kwargs ):
        has_exprs = False
        specifiers, style, attributes = node.specifiers, node.style, node.attributes
        spectext  = specifiers and specifiers.spectext
        styletext = style and style.styletext
        attrslist = attributes and attributes.attrslist

        items = []      # Items to stack-compute

        # Specifier
        if spectext :           # Static specifier content
            tagspec = self.handle_specifiers( spectext )
            fnspec, astext = lambda : igen.putattrs( tagspec ), False
        elif specifiers :       # Dynamic specifier content
            fnspec, astext = lambda : specifiers.generate(igen, *args, **kwargs), True
            has_exprs = True
        else :
            tagspec = ''
            fnspec, astext = lambda : igen.puttext( tagspec ), True
        items.append( (fnspec, astext) )

        # Style
        if styletext :          # Static style content
            tagstyle = self.handle_style( styletext )
            fnstyle, astext = lambda : igen.putattrs( tagstyle ), False
        elif style :            # Dynamic style content
            fnstyle, astext = lambda : style.generate( igen, *args, **kwargs ), True
            has_exprs = True
        else :
            tagstyle = ''
            fnstyle, astext = lambda : igen.puttext( tagstyle ), True
        items.append( (fnstyle, astext) )

        # Attributes
        if attrslist :              # Static attribute content
            tagattrs = self.handle_attributes( attrslist )
            fnattrs = lambda : igen.putattrs( tagattrs )
        elif attributes :           # Dynamic attribute content
            fnattrs = lambda : attributes.generate(igen, *args, **kwargs)
            has_exprs = True
        else :
            tagattrs = ''
            fnattrs = lambda : igen.puttext( tagattrs )
        items.append( (fnattrs, False) )# pop-out as list
    
        tagopen = node.TAGOPEN.dump(None)
        tagnm   = tagopen.strip(' \t\r\n')[1:]
        igen.puttext( tagnm )
        if has_exprs == False : # Tag definition is fully static
            tagdef = tagopen + ' '.join(filter(None, [ tagspec, tagstyle, tagattrs ]))
            tagdef += node.TAGEND and node.TAGEND.dump(None) or ''
            tagdef += node.TAGCLOSE and node.TAGCLOSE.dump(None) or ''
            igen.puttext( tagdef )
        else :
            node.TAGOPEN.generate( igen, *args, **kwargs )
            [ node.stackcompute(igen, fn, astext=astext) for fn, astext in items ]
            node.TAGEND and node.TAGEND.generate(igen, *args, **kwargs)
            node.TAGCLOSE and node.TAGCLOSE.generate(igen, *args, **kwargs)
        igen.puttext( self.handle_tagclose(tagnm) if node.TAGCLOSE else '' )
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
    
    def handle( self, mach, tag, contents, indent=False, newline='' ):
        A = mach.Attributes
        # Tag definition
        if len(tag) == 7 :
            tagnm, tagopen, spec, style, attr, tagclose, tagfinish = tag
            t = tagopen
            spec  = str(spec)  if spec and isinstance(spec[0], A) \
                               else self.handle_specifiers(spec)
            style = str(style) if style and isinstance(style[0], A) \
                               else self.handle_style(style)
            attr  = str(attr)  if attr and isinstance(attr[0], A) \
                               else self.handle_attributes(attr)
            t += spec + style + attr
        elif len(tag) == 3 :
            tagnm, t, tagfinish = tag
        else :
            raise Exception( 'Tag definition not in the expected format' )
        # Tag content
        t += self.handle_content( ''.join(contents) )
        # Tag close
        t += tagfinish
        return t

    def handle_specifiers( self, spectext ):
        if spectext :
            id_, classes, strings, atoms = self.parsespecifiers( spectext )
            str2attrs = self.specstrings2attrs(strings) if strings else ''
            atom2attrs, leftover = self.specatoms2attrs(atoms) if atoms else '', []
            return ' ' + ' '.join(filter(None, [ id_, classes, str2attrs, atom2attrs ]))
        else :
            return ''

    def handle_style( self, styletext ):
        return 'style="%s"' % styletext if styletext else ''

    def handle_attributes( self, attrslist ):
        return ' '.join(filter( None, attrslist)) if attrslist else ''

    def handle_content( self, text ):
        return text

    def handle_tagclose( self, tagnm ):
        return  '</%s>'%tagnm

    ws = r'[ \r\n\t]*'
    parseexp = re.compile(
        r'(\'[^\']+\'%s)|(\"[^"]+\"%s)|([^" \t\r\n\']+%s)' % (ws,ws,ws)
    )
    def parsespecifiers( self, spectext ):
        parsed = self.parseexp.findall( spectext )
        idclass = parsed and parsed[0][-1]
        if idclass and idclass[0] == '#' :
            parts = idclass.split('.')
            if len(parts) > 1 :
                id_, classes = parts[0], ' '.join( parts[1:] )
            else :
                id_, classes = parts[0], ''
            parsed.pop(0)
        elif idclass and idclass[0] == '.' :
            id_, classes = '', idclass[1:].replace('.', ' ')
            parsed.pop(0)
        else :
            id_ = classes = ''

        id_ = 'id="%s"' % id_[1:] if id_ else ''
        classes = 'class="%s"' % classes if classes else ''

        strings = filter( None, reduce( lambda x, t : x + list(t[:2]), parsed, [] ))
        atoms   = filter( None, map( lambda t : t[2], parsed ))
        return id_, classes, strings, atoms

    atom2attr = {
      # global attributes
      'edit'         : 'contenteditable="true"',
      'noedit'       : 'contenteditable="false"',
      'dragcopy'     : 'draggable="true" dragzone="copy"',
      'dragmove'     : 'draggable="true" dragzone="move"',
      'draglink'     : 'draggable="true" dragzone="link"',
      'nodrag'       : 'draggable="false"',
      'hidden'       : 'hidden',
      'spellcheck'   : 'spellcheck="true',
      'nospellcheck' : 'spellcheck="false',
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
        leftover, attrs = [], []
        for atom in atoms :
            if atom.startswith( 'key:' ):
                attr = 'accesskey="%s"' % atom.split(':', 1)[1]
            elif atom.startswith( 'tab:' ):
                attr = 'tabindex="%s"' % atom.split(':', 1)[1]
            else :
                attr = self.atom2attr.get( atom, None )
            attrs.append(attr) if attr != None else leftover.append(atom)
        return ' '.join( attr ), leftover

    def specstrings2attrs( self, strings ):
        return ' '.join(filter( None, strings ))

gsm.registerUtility( TagPlugin(), ITayraTag, '_default' )
