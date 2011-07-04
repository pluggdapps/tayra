from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.ttl.interfaces import ITayraTags
from   tayra.ttl.plugins    import parsespecifiers

gsm = getGlobalSiteManager()

def handle_html( tagopen, specifiers, style, attrs, tagfinish ) :
    tagname = tagopen[1:]
    _id, classes, tokens = parsespecifiers( specifiers )
    style = 'style="%s"' % style if style else style
    attributes = ' '.join( attrs )
    return ' '.join([ tagopen, _id, classes, attributes, tagfinish ])

def handle_head( tagopen, specifiers, style, attrs, tagfinish ) :
    return ''

def handle_body( tagopen, specifiers, style, attrs, tagfinish ) :
    return ''

def handle_h1( tagopen, specifiers, style, attrs, tagfinish ) :
    return ''

def handle_p( tagopen, specifiers, style, attrs, tagfinish ) :
    return ''

class HtmlTags( object ):
    implements( ITayraTags )
    def handlers( self ):
        g = globals()
        return dict([
            (fn[7:], val) for fn, val in g.items() if fn.startswith('handle_')
        ])

# Register this plugin
gsm.registerUtility( HtmlTags(), ITayraTags, 'html' )
