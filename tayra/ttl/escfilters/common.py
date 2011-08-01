import re, markupsafe, urllib 
from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.ttl.interfaces import  ITayraEscapeFilter

gsm = getGlobalSiteManager()

class XmlEscape( object ):
    implements( ITayraEscapeFilter )
    escapes = {
        '&' : '&amp;',
        '>' : '&gt;', 
        '<' : '&lt;', 
        '"' : '&#34;',
        "'" : '&#39;',
    }
    def __call__( self, mach, text ):
        return re.sub( r'([&<"\'>])', lambda m: self.escapes[m.group()], text )

class HtmlEscape( object ):
    implements( ITayraEscapeFilter )
    def __call__( self, mach, text ):
        return markupsafe.escape( text )

class UrlEscape( object ):
    implements( ITayraEscapeFilter )
    def __call__( self, mach, text ):
        return urllib.quote( text )

class Trim( object ):
    implements( ITayraEscapeFilter )
    def __call__( self, mach, text ):
        return text.strip()

class Unicode( object ):
    implements( ITayraEscapeFilter )
    def __call__( self, mach, text ):
        return unicode( text, mach.encoding )

# Register this plugin
gsm.registerUtility( XmlEscape(), ITayraEscapeFilter, 'x' )
gsm.registerUtility( HtmlEscape(), ITayraEscapeFilter, 'h' )
gsm.registerUtility( UrlEscape(), ITayraEscapeFilter, 'u' )
gsm.registerUtility( Trim(), ITayraEscapeFilter, 't' )
gsm.registerUtility( Unicode(), ITayraEscapeFilter, 'un' )
