# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

import re, urllib.parse, html

from   pluggdapps.plugin    import Plugin, implements
from   tayra.interfaces     import ITayraEscapeFilter

class UrlEscapeFilter( Plugin ):
    """Assume text as url and quote using urllib.parse.quote()"""
    implements( ITayraEscapeFilter )
    codename = 'u'
    def filter( self, mach, text ):
        return urllib.parse.quote( text )


class XmlEscapeFilter( Plugin ):
    """Assume text as XML, and apply escape encoding."""
    implements( ITayraEscapeFilter )
    codename = 'x'
    escapes = {
        '&' : '&amp;',
        '>' : '&gt;', 
        '<' : '&lt;', 
        '"' : '&#34;',
        "'" : '&#39;',
    }
    def filter( self, mach, text ):
        return re.sub( r'([&<"\'>])', lambda m: self.escapes[m.group()], text )


class HtmlEscape( Plugin ):
    """Assume text as HTML and apply html.escape( quote=True )"""
    implements( ITayraEscapeFilter )
    codename = 'h'
    def filter( self, mach, text ):
        return html.escape( text, quote=True )


class Trim( Plugin ):
    """Strip whitespaces before and after text using strip()"""
    implements( ITayraEscapeFilter )
    codename = 't'
    def filter( self, mach, text ):
        return text.strip()
