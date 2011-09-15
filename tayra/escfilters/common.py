import re, markupsafe, urllib 
from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.interfaces     import  ITayraEscapeFilter

gsm = getGlobalSiteManager()

class UrlEscape( object ):
    pluginname = 'u'
    implements( ITayraEscapeFilter )
    def do( self, mach, text, filterns=None ):
        return urllib.quote( text )

class Unicode( object ):
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
    pluginname = 'h'
    implements( ITayraEscapeFilter )
    def do( self, mach, text, filterns=None ):
        return markupsafe.escape( text )

class Trim( object ):
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
