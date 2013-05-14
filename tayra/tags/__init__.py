# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Template tags have one-to-one correspondence with HTML tags. On top of that
plugins can extend tag definitions, adding composite tags, by implementing 
:class:`tayra.interfaces.ITayraTags` interface specification. An example of
this can be found in :class:`tayra.tags.forms.HTML5Forms` plugin. 
Plugins wanting to implement :class:`ITayraTags` interface must derive from 
the base class :class:`Tags` defined in this module. The base class
defines standard specifier tokens common to all template tags, also gracefully
handles undefined tags in safest possible way.

Tag meta syntax,::

<tagname list-of-specifiers { inline-css-style } list-of-attributes>

``tagname``,
    can be standard HTML tag or custom tags that are translated to HTML
    tags by a plugin.

``specifiers``,
    a token or string that are delimited by whitespace.

``style``,
    CSS style parameters that can be otherwise specified as value for `style`
    attribute.

``attribute``,
    regular HTML attributes.

List of specifiers that are common to all template tags.
--------------------------------------------------------

- **id** attribute can be specified as **#<id-value>**.
- **class** attribute can be specified as **.<class1>.<class2>**
- **name** attribute can be specified as **:<name>**.

tokens that will be translated to attribute values.

    +-----------------+-------------------------------------+
    |      token      |   Equivalent attribute pairs        |
    +=================+=====================================+
    |  edit           | contenteditable="true"              |
    +-----------------+-------------------------------------+
    |  noedit         | contenteditable="false"             |
    +-----------------+-------------------------------------+
    |  dragcopy       | draggable="true" dragzone="copy"    |
    +-----------------+-------------------------------------+
    |  dragmove       | draggable="true" dragzone="move"    |
    +-----------------+-------------------------------------+
    |  draglink       | draggable="true" dragzone="link"    |
    +-----------------+-------------------------------------+
    |  nodrag         | draggable="false"                   |
    +-----------------+-------------------------------------+
    |  hidden         | hidden                              |
    +-----------------+-------------------------------------+
    |  spellcheck     | spellcheck="true"                   |
    +-----------------+-------------------------------------+
    |  nospellcheck   | spellcheck="false"                  |
    +-----------------+-------------------------------------+
    |  ltr            | dir="ltr"                           |
    +-----------------+-------------------------------------+
    |  rtl            | dir="rtl"                           |
    +-----------------+-------------------------------------+
    |  disabled       | disabled="disabled"                 |
    +-----------------+-------------------------------------+
    |  checked        | checked="checked"                   |
    +-----------------+-------------------------------------+
    |  readonly       | readonly="readonly"                 |
    +-----------------+-------------------------------------+
    |  selected       | selected="selected"                 |
    +-----------------+-------------------------------------+
    |  multiple       | multiple="multiple"                 |
    +-----------------+-------------------------------------+
    |  defer          | defer="defer"                       |
    +-----------------+-------------------------------------+
"""

from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra.interfaces     import ITayraTags

class Tags( Plugin ):
    """Base class for all plugins wanting to handle template tags. Since the
    base class declares that it implements :class:`tayra.interfaces.ITayraTags`
    interface, deriving plugins need not do the same. 

    - provides standard specifier syntax for common tag attributes.
    - gracefully handles undefined tags.
    """
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

    #---- ITayraTags interface methods

    def handle( self, mach, tagname, tokens, styles, attributes, content ):
        """:meth:`pluggdapps.plugin.ISettings.default_settings` interface 
        method.
        
        This method is expected to be overriden by the deriving plugin
        class, only for undefined template tags this method will be called,
        after trying with other plugins in the list of ``tag.plugins``."""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        l = len(content) - len(content.rstrip())
        content, nl = (content[:-l], content[-l:]) if l else (content, '')
        return ('<%s %s>%s</%s>' % (tagname, attrs, content, tagname)) + nl

    def parse_specs( self, tokens, styles, attributes ):
        """The base class provides standard set of tokens and specifiers that
        are common to most HTML tags. To parse these tokens into
        tag-attributes, deriving plugins can use this method."""
        tagattrs, remtoks = self.parse_tokens( tokens )
        tagattrs += (' style="%s"' % ';'.join( styles )) if styles else ''
        tagattrs += (' ' + ' '.join( attributes )) if attributes else ''
        return tagattrs, remtoks

    #-- Local methods.

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

    #---- ISettings interface methods

    @classmethod
    def default_settings( cls ):
        """:meth:`pluggdapps.plugin.ISettings.default_settings` interface 
        method."""
        return _default_settings

    @classmethod
    def normalize_settings( cls, sett ):
        """:meth:`pluggdapps.plugin.ISettings.normalize_settings` interface 
        method."""
        return sett

_default_settings = h.ConfigDict()
_default_settings.__doc__ = (
    "Base plugin to handle tayra template's tag markups." )

import tayra.tags.html
import tayra.tags.forms
