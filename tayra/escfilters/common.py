# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Proviles common set of escape filters for expression substition."""

import re, urllib.parse, html

from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra.interfaces     import ITayraEscapeFilter

class TayraEscFilterCommon( Plugin ):
    """Plugin supplies escape filtering like url-encode, xml-encode, 
    html-encode, stripping whitespaces on expression substitution."""

    implements( ITayraEscapeFilter )

    xmlescapes = {
        '&' : '&amp;',
        '>' : '&gt;', 
        '<' : '&lt;', 
        '"' : '&#34;',
        "'" : '&#39;',
    }
    def filter( self, mach, name, text ):
        """:meth:`tayra.interfaces.ITayraEscapeFilter.filter` interface 
        method."""
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
_default_settings.__doc__ = TayraEscFilterCommon.__doc__
