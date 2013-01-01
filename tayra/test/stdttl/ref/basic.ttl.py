import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra                import BaseTTLPlugin


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.pushbuf()
  _m.extend( ['<head>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( [' hello world', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions

def render(
              this, id='', cssasset='bootstrap:static/paview_metanav.css' ):  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<div #'] )
  _m.append(_m.evalexprs( 'id', '', globals(), locals()) )
  _m.extend( [' .metanav-pa>'] )
  _m.pushbuf()
  _m.extend( ['\n    ', 'how are your world', '\n    '] )
  # if cssasset :
  if cssasset :    
    pass  
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Interface functions
from  tayra.interfaces import ITayraTestInterface
class XYZPlugin( BaseTTLPlugin ):
  implements(ITayraTestInterface) 

  render = render

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/basic.ttl' 