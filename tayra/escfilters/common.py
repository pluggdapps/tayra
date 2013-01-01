# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

import re, urllib.parse, html

from   pluggdapps.plugin    import Plugin, implements
from   tayra.interfaces     import ITayraEscapeFilter

class CommonEscapeFilters( Plugin ):
    implements( ITayraEscapeFilter )

    xmlescapes = {
        '&' : '&amp;',
        '>' : '&gt;', 
        '<' : '&lt;', 
        '"' : '&#34;',
        "'" : '&#39;',
    }
    def filter( self, mach, name, text ):
        handler = getattr( self, name, self.default )
        return handler( mach, text )

    def u( self, mach, text ):
        """Assume text as url and quote using urllib.parse.quote()"""
        return urllib.parse.quote( text )

    def x( self, mach, text ):
        """Assume text as XML, and apply escape encoding."""
        return re.sub( r'([&<"\'>])', 
                       lambda m: self.xmlescapes[m.group()], text )

    def h( self, mach, text ):
        """Assume text as HTML and apply html.escape( quote=True )"""
        return html.escape( text, quote=True )

    def t( self, mach, text ):
        """Strip whitespaces before and after text using strip()"""
        return text.strip()

    def default( self, mach, text ):
        """Default handler. Return ``None`` so that runtime will try other
        plugins implementing the filter."""
        return None
