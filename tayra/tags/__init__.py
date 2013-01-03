# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

from   pluggdapps.plugin        import Plugin, implements
from   tayra.interfaces         import ITayraTags

class TayraTags( Plugin ):
    """Plugin handles basic html tags."""
    implements( ITayraTags )

    general_toks = {
      # global attributes
      'edit'         : ' contenteditable="true"',
      'noedit'       : ' contenteditable="false"',
      'dragcopy'     : ' draggable="true" dragzone="copy"',
      'dragmove'     : ' draggable="true" dragzone="move"',
      'draglink'     : ' draggable="true" dragzone="link"',
      'nodrag'       : ' draggable="false"',
      'hidden'       : ' hidden',
      'spellcheck'   : ' spellcheck="true"',
      'nospellcheck' : ' spellcheck="false"',
      # dir
      'ltr'          : ' dir="ltr"',
      'rtl'          : ' dir="rtl"',
      # atoms
      'disabled'     : ' disabled="disabled"',
      'checked'      : ' checked="checked"',
      'readonly'     : ' readonly="readonly"',
      'selected'     : ' selected="selected"',
      'multiple'     : ' multiple="multiple"',
      'defer'        : ' defer="defer"',
    }

    token_shortcuts = {
        '#' : lambda tok : \
                    ' id="%s"' % tok[1:],
        '.' : lambda tok : \
                    ' class="%s"' % ' '.join( filter( None, tok.split('.') )),
        ':' : lambda tok : \
                    ' name="%s"' % tok[1:],
    }

    def parse_tokens( self, tokens ):
        tagattrs, remtoks = '', []
        for tok in tokens :
            attr = self.token_shortcuts.get( tok[0], lambda tok : tok )( tok )
            attr = self.general_toks.get( attr, attr )
            if tok == attr :
                remtoks.append( tok )
            else :
                tagattrs += attr
        return tagattrs, remtoks

    def parse_specs( self, tokens, styles, attributes ):
        tagattrs, remtoks = self.parse_tokens( tokens )
        tagattrs += (' style="%s"' % ';'.join( styles )) if styles else ''
        tagattrs += (' ' + ' '.join( attributes )) if attributes else ''
        return tagattrs, remtoks

    def handle( self, mach, tagname, tokens, styles, attributes, content ):
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        l = len(content) - len(content.rstrip())
        content, nl = (content[:-l], content[-l:]) if l else (content, '')
        return ('<%s %s>%s</%s>' % (tagname, attrs, content, tagname)) + nl


import tayra.tags.html
import tayra.tags.forms
