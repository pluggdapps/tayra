from   zope.interface       import implements
from   tayra.interfaces     import ITTLPlugins

class TestPlugins( object ):
    implements( ITTLPlugins )

    def implementers( self ):
        # return ['tayra:test/stdttl/implementer.ttl']
        return []
