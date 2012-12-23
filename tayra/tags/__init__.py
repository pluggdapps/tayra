# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

from   pluggdapps.plugin        import Plugin, implements
from   tayra.interfaces         import ITayraTags

class TayraTags( Plugin ):
    implements( ITayraTags )

    token2attr = {
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

    def parse_tokens( self, tokens ):
        tagid, tagclasses, tagattrs, remtoks = '', [], [], []
        for tok in tokens :
            if tok[0] == '#' :
                tagid = tok[1:]
                continue
            if tok[0] == '.' :
                tagclasses += list( filter( None, tok.split('.') ))
                continue
            if tok in self.token2attr :
                tagattrs.append( self.token2attr.get( tok, '' ))
                continue
            remtoks.append( tok )
        return tagid, tagclasses, tagattrs, remtoks

    def parse_specs( self, tokens, styles, attributes ):
        tagid, tagclasses, tagattrs, remtoks = self.parse_tokens( tokens )
        attrs = ''
        attrs += 'id="%s"' % tagid if tagid else ''
        attrs += (' class="%s"' % ' '.join( tagclasses )) if tagclasses else ''
        attrs += (' ' + ' '.join( tagattrs )) if tagattrs else ''
        attrs += (' style="%s"' % ';'.join( styles )) if styles else ''
        attrs += (' ' + ' '.join( attributes )) if attributes else ''
        return attrs, remtoks

    def handle( self, mach, tagname, tokens, styles, attributes, content ):
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = attrs.strip()
        l = len(content) - len(content.rstrip())
        content, nl = (content[:-l], content[-l:]) if l else (content, '')
        return ('<%s %s>%s</%s>' % (tagname, attrs, content, tagname)) + nl


import tayra.tags.html
import tayra.tags.forms
