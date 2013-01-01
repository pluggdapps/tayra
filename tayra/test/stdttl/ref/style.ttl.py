import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<div #_id .cls {color: red} a="b">'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.pushbuf()
  _m.extend( ['<a #'] )
  _m.append(_m.evalexprs( "'idname'", '', globals(), locals()) )
  _m.extend( [' .'] )
  _m.append(_m.evalexprs( "'cls'", '', globals(), locals()) )
  _m.extend( ['\n    "http://pluggdapps.com"\n    { '] )
  _m.append(_m.evalexprs( "'color : '", '', globals(), locals()) )
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '"red;"', '', globals(), locals()) )
  _m.extend( [" ' style with line break' } >"] )
  _m.pushbuf()
  _m.extend( [' hello {world}', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/style.ttl' 