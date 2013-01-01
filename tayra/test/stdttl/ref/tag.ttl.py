import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *


def body( *args, **kwargs ) :  
  _m.pushbuf()
  world = 'jasper'
  _m.pushbuf()
  _m.extend( ['<form #idname\nformname "', 'http://\ngoogle.com" >'] )
  _m.pushbuf()
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '"hello " + str(10) + \' world\'', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  _m.pushbuf()
  _m.extend( ['<input>'] )
  _m.pushbuf()
  _m.extend( ['\n\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['<!--', ' Comment\n    ', '-->', '\n    '] )
  _m.pushbuf()
  _m.extend( ['<input>'] )
  _m.pushbuf()
  _m.extend( ['\n       ', '<!--', ' Comment\n       ', '-->', '\n   \n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ["<input text  =$_0(*&^%%$#@!@~}= world }$ {' title= hello "] )
  _m.append(_m.evalexprs( 'world', '', globals(), locals()) )
  _m.extend( ['}>'] )
  _m.pushbuf()
  _m.extend( ['\n      \n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/tag.ttl' 