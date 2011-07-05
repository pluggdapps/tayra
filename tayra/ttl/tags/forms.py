from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.ttl.interfaces import ITayraTags
from   tayra.ttl.tags       import parsespecifiers, composetag, stdspecifiers

gsm = getGlobalSiteManager()

class Forms( object ):
    implements( ITayraTags )
    def handlers( self ):
        g = globals()
        return dict([
            (fn[7:], val) for fn, val in g.items() if fn.startswith('handle_')
        ])

# Register this plugin
gsm.registerUtility( Forms(), ITayraTags, 'forms' )
