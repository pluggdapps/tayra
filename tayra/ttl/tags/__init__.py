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

    def tagline( self, node, igen, pruneinner, handletag, *args, **kwargs ):
        # If prune syntax is detected, do that before doing anything.
        node._pruneinner() if pruneinner else None
        # Generate indentation of tagline
        igen.comment( node.dump( Context() ))
        igen.indent()
        # Do the actual tag-line, but don't handle the tagline during runtime,
        # for taglines that are children to tagblocks,
        # because for tagblocks the runtime handling must be deferred after
        # the siblings are also populated in the stack.
        tag, content = node.tag, node.content
        igen.pushbuf()      # Push tag element
        tag.generate( igen, *args, **kwargs )
        igen.pushbuf()      # Push tag content
        content.generate( igen, *args, **kwargs ) if content else None
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
        self.tagline( node, igen, node.tag.pruneinner, True, *args, **kwargs )

    def generate_tagblock( self, node, igen, *args, **kwargs ):
        tagline = node.tagline
        pruneindent = tagline.tag.pruneindent
        pruneinner = tagline.tag.pruneinner or pruneindent
        self.tagline( tagline, igen, pruneinner, False, *args, **kwargs )

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
    
    def handle( self, tagopen, specifiers, style, attrs, tagfinish ):
        id_, classes, _s, _a = self.parsespecifiers( specifiers )
        return self.composetag(
            tagopen, filter(None, [id_, classes]), style, attrs, tagfinish
        )

    #---- Helper methods

    ws = r'[ \r\n\t]*'
    parseexp = re.compile(
        r'(\'[^\']+\'%s)|(\"[^"]+\"%s)|([^" \t\r\n\']+%s)' % (ws,ws,ws)
    )
    def parsespecifiers( self, specifiers ):
        parsed = self.parseexp.findall( specifiers )
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
            id_ = classes = None

        id_ = 'id="%s"' % id_[1:] if id_ else None
        classes = 'class="%s"' % classes if classes else None

        strings = filter( None, reduce( lambda x, t : x + list(t[:2]), parsed, [] ))
        atoms   = filter( None, map( lambda t : t[2], parsed ))
        return id_, classes, strings, atoms

    def atoms2attrs( self, spectokens ):
        leftover, attrs = [], []
        for token in spectokens :
            if token.startswith( 'key:' ):
                attr = 'accesskey="%s"' % token.split(':', 1)[1]
            if token.startswith( 'tab:' ):
                attr = 'tabindex="%s"' % token.split(':', 1)[1]
            else :
                attr = atom2attr.get( token, None )
            attrs.append( attr ) if attr != None else leftover.append( token )
        return filter(None, leftover), attrs

    def composetag( self, tagopen, specattrs, style, attrs, tagfinish ):
        tagopen = tagopen.rstrip(' ')
        style = 'style="%s"' % style.strip(' ') if style else style
        specattrs = ' '.join( specattrs )
        attrs = ' '.join( attrs )
        cont = ' '.join( filter( None, [ tagopen, specattrs, style, attrs ]) )
        return cont + tagfinish

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
      # encoding type
      'application/x-www-form-urlencoded': 'enctype="application/x-www-form-urlencoded"',
      'multipart/form-data': 'enctype="multipart/form-data"',
      'text/plain': 'enctype="text/plain"',
      # shape
      'default' : 'shape="default"',
      'rect'    : 'shape="rect"',
      'circle'  : 'shape="circle"',
      'poly'    : 'shape="poly"',
      # dir
      'ltr'     : 'shape="ltr"',
      'rtl'     : 'shape="rtl"',
      # target
      '_blank'  : 'target="_blank"',
      '_self'   : 'target="_self"',
      '_parent' : 'target="_parent"',
      '_top'    : 'target="_top"',
      # method
      'get'     : 'method="get"',
      'post'    : 'method="post"',
      # atoms
      'disabled': 'disabled="disabled"',
      'checked' : 'checked="checked"',
      'readonly': 'readonly="readonly"',
      'selected': 'selected="selected"',
      'multiple': 'multiple="multiple"',
      'defer'   : 'defer="defer"',
    }

gsm.registerUtility( TagPlugin(), ITayraTag, '_default' )
