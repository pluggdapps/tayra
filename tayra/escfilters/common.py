# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

import re, markupsafe, urllib 
from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.interfaces     import  ITayraEscapeFilter

gsm = getGlobalSiteManager()

class UrlEscape( object ):
    """Assume text as url and quote using urllib.quote()"""
    pluginname = 'u'
    implements( ITayraEscapeFilter )
    def do( self, mach, text, filterns=None ):
        return urllib.quote( text )

class Unicode( object ):
    """Decode text into unicoded string, using encoding-type provided in
    configuration parameter or using the namespace parameter supplied in 
    this filter, like,

    > [<pre ${ text | uni.utf-8 } >]
    """
    pluginname = 'uni'
    implements( ITayraEscapeFilter )
    def do( self, mach, val, filterns=None ):
        try :
            encoding = filterns
        except :
            encoding = mach.encoding
        if isinstance(val, unicode) :
            return val
        elif isinstance(val, str) :
            return val.decode( encoding )
        else :
            return unicode( str(val), encoding=encoding )

class XmlEscape( object ):
    """Assume text as XML, and apply escape encoding."""
    pluginname = 'x'
    implements( ITayraEscapeFilter )
    escapes = {
        '&' : '&amp;',
        '>' : '&gt;', 
        '<' : '&lt;', 
        '"' : '&#34;',
        "'" : '&#39;',
    }
    def do( self, mach, text, filterns=None ):
        return re.sub( r'([&<"\'>])', lambda m: self.escapes[m.group()], text )

class HtmlEscape( object ):
    """Assume text as HTML and apply markupsafe.escape()"""
    pluginname = 'h'
    implements( ITayraEscapeFilter )
    def do( self, mach, text, filterns=None ):
        return markupsafe.escape( text )

class Trim( object ):
    """Strip whitespaces before and after text using strip()"""
    pluginname = 't'
    implements( ITayraEscapeFilter )
    def do( self, mach, text, filterns=None ):
        return text.strip()

# Register this plugin
gsm.registerUtility( XmlEscape(), ITayraEscapeFilter, XmlEscape.pluginname )
gsm.registerUtility( HtmlEscape(), ITayraEscapeFilter, HtmlEscape.pluginname )
gsm.registerUtility( UrlEscape(), ITayraEscapeFilter, UrlEscape.pluginname )
gsm.registerUtility( Trim(), ITayraEscapeFilter, Trim.pluginname )
gsm.registerUtility( Unicode(), ITayraEscapeFilter, Unicode.pluginname )
