import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  ', ''] )
  _m.append(_m.evalexprs( 'func("hello world")', '', globals(), locals()) )
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions

@useragent( 'ff5' )
def func( a ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( [' hey firefox 5 '] )
  _m.append(_m.evalexprs( 'a', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()


@useragent( 'ch8' )
def func( a ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( [' hey chromium 8 '] )
  _m.append(_m.evalexprs( 'a', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()


@useragent()
def func( a ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( [' Hey everyone '] )
  _m.append(_m.evalexprs( 'a', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '././test/stdttl/func_decorator.ttl' 