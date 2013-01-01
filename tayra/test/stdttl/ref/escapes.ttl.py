import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra                import BaseTTLPlugin


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n\n'] )
  _m.extend( ['@body any directive', '\n\n'] )
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
  _m.extend( ['\n    ', 'Escaping the indent', '\n    '] )
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( ['\n      ', 'Escaping newlines       across textblocks, all of this belongs to body content.', '\n      ', '@def escapedfunction():', '\n        ', '@@pass', '\n      ', '\\${ this expresion is also escaped } and displayed as text', '\n      ', '@if so is this if block :', '\n      ', '@elif block :', '\n      ', '@else block :', '\n      ', '@for block :', '\n      ', '@while block :', '\n      ', 'all of them are interpreted as text.', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'willbecomeglobal()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions

def willbecomeglobal( *args ):  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<b>'] )
  _m.pushbuf()
  _m.extend( [' Ghost', '\n        '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  
  def nestedfunc():    
    _m.pushbuf()
    _m.pushbuf()
    _m.extend( ['<em>'] )
    _m.pushbuf()
    _m.extend( [' Rider', '\n        '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    return _m.popbuftext()  
  
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'nestedfunc()', '', globals(), locals()) )
  _m.extend( ['\n      '] )
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/escapes.ttl' 