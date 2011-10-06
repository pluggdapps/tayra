
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body(  ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n'] )
  return _m.popbuftext()

# ---- Global Functions

# def render( *args, **kwargs ):
def render( *args, **kwargs ):  
  _m.pushbuf()
  # <div> interface successfully invoked
  _m.pushbuf()
  _m.extend( [u'div', u'<div  > ', u'</div>'] )
  _m.pushbuf()
  _m.extend( [u'interface successfully invoked'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  return _m.popbuftext()
# ---- Interface functions

from  tayra.interfaces import ITestInterface
class Interface_1( BaseTTLPlugin ):
  implements(ITestInterface)
  itype = 'ttlplugin'
  render = render
_m.register( Interface_1(), ITestInterface, u'testinterface' )
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/implementer.ttl'
