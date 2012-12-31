import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( [''] )
  _m.append(_m.evalexprs( "render('hello')", '', globals(), locals()) )
  _m.extend( ['\n'] )
  return _m.popbuftext()

# ---- Global Functions

def render( a ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( [' '] )
  _m.append(_m.evalexprs( 'a', '', globals(), locals()) )
  _m.extend( ['\n    ', ''] )
  _m.append(_m.evalexprs( 'a', '', globals(), locals()) )
  _m.extend( ['\n  \n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '././test/stdttl/exprs1.ttl' 