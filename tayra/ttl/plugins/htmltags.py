from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.ttl.interfaces import ITayraTags

gsm = getGlobalSiteManager()

def handle_html( tagname, specifiers, style, attrs, tagfinish ) :
    return ''

def handle_head( tagname, specifiers, style, attrs, tagfinish ) :
    return ''

def handle_body( tagname, specifiers, style, attrs, tagfinish ) :
    return ''

def handle_h1( tagname, specifiers, style, attrs, tagfinish ) :
    return ''

def handle_p( tagname, specifiers, style, attrs, tagfinish ) :
    return ''

class HtmlTags( object ):
    implements( ITayraTags )
    def handlers( self ):
        g = globals()
        return dict([
            (fn, val) for fn, val in g.items() if fn.startswith('handle_')
        ])

# Register this plugin
gsm.registerUtility( HtmlTags(), ITayraTags, 'html' )
