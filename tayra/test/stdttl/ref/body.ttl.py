import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *


def body( id="hello", cls="world", style='color: red;', *args, **kwargs ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<div #'] )
  _m.append(_m.evalexprs( 'id', '', globals(), locals()) )
  _m.extend( [' .'] )
  _m.append(_m.evalexprs( 'cls', '', globals(), locals()) )
  _m.extend( [' {'] )
  _m.append(_m.evalexprs( 'style', '', globals(), locals()) )
  _m.extend( ['} >'] )
  _m.pushbuf()
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '././test/stdttl/body.ttl' 