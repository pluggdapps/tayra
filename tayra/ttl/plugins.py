from   zope.interface       import implements
from   tayra.ttl.interfaces import ITTLPlugins

class TestPlugins( object ):
    implements( ITTLPlugins )

    def implementers( self ):
        return ['tayra:ttl/test/stdttl/implementer.ttl']
