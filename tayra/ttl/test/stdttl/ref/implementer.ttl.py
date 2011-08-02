
from   StringIO             import StringIO
from   zope.interface       import implements
import tayra



def body(  ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n'] )
  return _m.popbuftext()

# ---- Global Functions

# def render(*args, **kwargs ):
def render(*args, **kwargs ):  
  _m.pushbuf()
  # <div> interface successfully invoked
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<div', '', '', '', u'> '] )
  _m.pushbuf()
  _m.extend( [u'interface successfully invoked'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( [u'\n'] )
  return _m.popbuftext()
# ---- Interface functions

from  tayra.ttl.interfaces import ITestInterface
class Interface_1( object ):
  implements(ITestInterface)
Interface_1_obj = Interface_1()
Interface_1_obj.render = _m.hitch( Interface_1_obj, Interface_1, render )
_m.register( Interface_1_obj, ITestInterface, u'testinterface' )
# ---- Footer

_ttlhash = 'c70d37fa7c67b77f60565e84c917e8ec9840be79'
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/implementer.ttl'
