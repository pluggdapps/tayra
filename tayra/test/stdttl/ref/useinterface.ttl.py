import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra                import BaseTTLPlugin

from tayra.interfaces import ITayraTestInterface 

def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n'] )
  obj = _compiler.query_plugin( ITayraTestInterface, 'XYZTestInterface' )
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
  _m.extend( ['\n    ', ''] )
  _m.append(_m.evalexprs( 'obj.render()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/useinterface.ttl' 