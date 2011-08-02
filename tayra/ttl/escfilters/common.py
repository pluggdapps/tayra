import re, markupsafe, urllib 
from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.ttl.interfaces import  ITayraEscapeFilter

gsm = getGlobalSiteManager()

class UrlEscape( object ):
    filtername = 'u'
    implements( ITayraEscapeFilter )
    def __call__( self, mach, text, filterns=None ):
        return urllib.quote( text )

class Unicode( object ):
    filtername = 'uni'
    implements( ITayraEscapeFilter )
    def __call__( self, mach, val, filterns=None ):
        try :
            _, encoding = filterns
        except :
            encoding = mach.encoding
        if isinstance(val, unicode) :
            return val
        elif isinstance(val, str) :
            return val.decode( encoding )
        else :
            return unicode( str(val), encoding=encoding )

class XmlEscape( object ):
    filtername = 'x'
    implements( ITayraEscapeFilter )
    escapes = {
        '&' : '&amp;',
        '>' : '&gt;', 
        '<' : '&lt;', 
        '"' : '&#34;',
        "'" : '&#39;',
    }
    def __call__( self, mach, text, filterns=None ):
        return re.sub( r'([&<"\'>])', lambda m: self.escapes[m.group()], text )

class HtmlEscape( object ):
    filtername = 'h'
    implements( ITayraEscapeFilter )
    def __call__( self, mach, text, filterns=None ):
        return markupsafe.escape( text )

class Trim( object ):
    filtername = 't'
    implements( ITayraEscapeFilter )
    def __call__( self, mach, text, filterns=None ):
        return text.strip()

# Register this plugin
gsm.registerUtility( XmlEscape(), ITayraEscapeFilter, XmlEscape.filtername )
gsm.registerUtility( HtmlEscape(), ITayraEscapeFilter, HtmlEscape.filtername )
gsm.registerUtility( UrlEscape(), ITayraEscapeFilter, UrlEscape.filtername )
gsm.registerUtility( Trim(), ITayraEscapeFilter, Trim.filtername )
gsm.registerUtility( Unicode(), ITayraEscapeFilter, Unicode.filtername )
