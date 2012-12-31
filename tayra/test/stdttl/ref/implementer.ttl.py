import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n'] )
  return _m.popbuftext()

# ---- Global Functions

def render( *args, **kwargs ):  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( [' interface successfully invoked', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Interface functions
from  tayra.interfaces import ITayraTestInterface
class XYZTestInterface( BaseTTLPlugin ):
  implements(ITayraTestInterface) 

# ---- Footer
_ttlhash = ''
_ttlfile = '././test/stdttl/implementer.ttl' 