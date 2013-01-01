import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra                import BaseTTLPlugin


def body( *args, **kwargs ) :  
  _m.pushbuf()
  world = 'world'
  _m.pushbuf()
  _m.extend( ["<div #id {' title= hello "] )
  _m.append(_m.evalexprs( 'world', '', globals(), locals()) )
  _m.extend( ['}>'] )
  _m.pushbuf()
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ["<input text  =$_0(*&^%%$#@!@~}= world }$ {' title= hello "] )
  _m.append(_m.evalexprs( 'world', '', globals(), locals()) )
  _m.extend( ['}>'] )
  _m.pushbuf()
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/obfus1.ttl' 