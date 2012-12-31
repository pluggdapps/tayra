import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ["<!--\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\nCopyright (c) 2011 R Pratap Chakravarthy\n-->\n\n"] )
  _m.pushbuf()
  _m.extend( ['<pre>'] )
  _m.pushbuf()
  _m.extend( ['\n  ', 'int foo( int a, int b  ){', '\n    ', "printf( 'helloworld' )", '\n  ', '}', '\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'helloword()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  return _m.popbuftext()

# ---- Global Functions

def helloword( x=10, y=20, a='wer', b='ehl' ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  b = 'hello'   
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'x+y', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  _m.pushbuf()
  _m.extend( ['<head #headid .cls1.'] )
  _m.append(_m.evalexprs( 'a.strip()', '', globals(), locals()) )
  _m.extend( [' "title" {color:red} lang="en" data="hello">'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  _m.pushbuf()
  _m.extend( ['<title #titleid .cls1 "title string">'] )
  _m.pushbuf()
  _m.extend( [' hello '] )
  _m.append(_m.evalexprs( 'a', '', globals(), locals()) )
  _m.extend( [' @ ! # "helo" \'world "ok', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  _m.pushbuf()
  _m.extend( ['<h1 { color : red; border : 1px solid gray; }>'] )
  _m.pushbuf()
  _m.extend( [' ', '\n        ', 'I am the space station '] )
  _m.append(_m.evalexprs( '"These "', '', globals(), locals()) )
  _m.extend( [' seven cameras have a zoom range', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<p first second>'] )
  _m.pushbuf()
  _m.extend( [' of any 12x or more,  '] )
  _m.append(_m.evalexprs( '20', '', globals(), locals()) )
  _m.extend( ['  ', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['and some of the wide-angle view', '\n      '] )
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( [' of good. They also have a', '\n        ', 'lot of image stabilization (either optical or mechanical), which is', '\n        ', 'important for people who are with a powerful zoom lens. Some other', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['important features thatThese cameras contain electronic viewfinder,', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['full control while shooting. In general, these cameras are all seem', '\n      ', 'very similar.', '\n    \n      '] )
  _m.pushbuf()
  _m.extend( ['<p #'] )
  _m.append(_m.evalexprs( 'b', '', globals(), locals()) )
  _m.extend( ['>'] )
  _m.pushbuf()
  _m.extend( [' Sign my guestbook', '\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '././test/stdttl/stripsyntax.ttl' 