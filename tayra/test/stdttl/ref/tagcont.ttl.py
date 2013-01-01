import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra                import BaseTTLPlugin


def body( x=10, y=10, a="cls2 ", b="cls3", *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ["<!--\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\nCopyright (c) 2011 R Pratap Chakravarthy\n-->\n\n"] )
  m = 10
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  b = 'hello'   
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'x+y', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  _m.pushbuf()
  _m.extend( ['<head #headid .cls1.'] )
  _m.append(_m.evalexprs( 'a.strip()', '', globals(), locals()) )
  _m.extend( [' "title" {color:red} lang="en"\n   data="hello">'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  _m.pushbuf()
  _m.extend( ['<title #titleid .cls1 "title \n      string">'] )
  _m.pushbuf()
  _m.extend( [' hello '] )
  _m.append(_m.evalexprs( 'a', '', globals(), locals()) )
  _m.extend( [' @ ! # "helo" \'world "ok', '\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  _m.pushbuf()
  _m.extend( ['<h1 { color : red; border : 1px solid gray;\n    }>'] )
  _m.pushbuf()
  _m.extend( [' I am the space station '] )
  _m.append(_m.evalexprs( '"These "', '', globals(), locals()) )
  _m.extend( [' seven cameras', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['<!--', ' comment1\n   comment ', '-->', '\n    ', 'have a zoom range', '\n    '] )
  _m.pushbuf()
  _m.extend( ['<p first\n    second>'] )
  _m.pushbuf()
  _m.extend( [' of any 12x or more,', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['<!--', ' comment1\n       comment ', '-->', '\n    ', 'and some of the wide-angle view', '\n    '] )
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( [' of good. They also have a', '\n      ', 'lot of image stabilization (either optical or mechanical), which is', '\n      ', 'important for people who are with a powerful zoom lens. Some other', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['important features thatThese cameras contain electronic viewfinder,', '\n      ', '<!--', ' comment1 comment ', '-->', '\n\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['full control while shooting. In general, these cameras are all seem', '\n    ', 'very similar.', '\n  \n    '] )
  _m.pushbuf()
  _m.extend( ['<p #'] )
  _m.append(_m.evalexprs( 'b', '', globals(), locals()) )
  _m.extend( ['>'] )
  _m.pushbuf()
  _m.extend( [' Sign my guestbook', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/tagcont.ttl' 