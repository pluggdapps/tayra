import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '"hello עברית" + str([ str(10) ]) + \' world\'', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  _m.pushbuf()
  _m.extend( ['<a #'] )
  _m.append(_m.evalexprs( "'idname'", '', globals(), locals()) )
  _m.extend( [' .'] )
  _m.append(_m.evalexprs( "'cls' 'name'", '', globals(), locals()) )
  _m.extend( [' \n     "'] )
  _m.append(_m.evalexprs( '"http://" \'google.com\'', '', globals(), locals()) )
  _m.extend( ['" \n     { '] )
  _m.append(_m.evalexprs( "'color : '", '', globals(), locals()) )
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '"red;"', '', globals(), locals()) )
  _m.extend( [' }\n     '] )
  _m.append(_m.evalexprs( '"title"', '', globals(), locals()) )
  _m.extend( ['="'] )
  _m.append(_m.evalexprs( '"sun is " " shining"', '', globals(), locals()) )
  _m.extend( [' brightly">'] )
  _m.pushbuf()
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '././test/stdttl/exprs.ttl' 