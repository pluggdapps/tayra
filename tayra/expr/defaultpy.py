# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Provides default expression evaluator and a common set of filtering
methods. Evaluates python expression."""

import re, urllib.parse, html

from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra.interfaces     import ITayraExpression

class ExpressionPy( Plugin ):
    """Plugin evaluates python expression, converts the result into
    string and supplies escape filtering like url-encode, xml-encode, 
    html-encode, stripping whitespaces on expression substitution."""

    implements( ITayraExpression )

    def eval( self, mach, text, globals_, locals_ ):
        """:meth:`tayra.interfaces.ITayraExpression.eval` interface 
        method."""
        return str( eval( text, globals_, locals_ ))

    def filter( self, mach, name, text ):
        """:meth:`tayra.interfaces.ITayraExpression.filter` interface 
        method."""
        handler = getattr( self, name, self.default )
        return handler( mach, text )

    def u( self, mach, text ):
        """Assume text as url and quote using urllib.parse.quote()"""
        return urllib.parse.quote( text )

    xmlescapes = {
        '&' : '&amp;',
        '>' : '&gt;', 
        '<' : '&lt;', 
        '"' : '&#34;',
        "'" : '&#39;',
    }
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
_default_settings.__doc__ = ExpressionPy.__doc__
