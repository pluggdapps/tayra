import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra                import BaseTTLPlugin


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ['<!-- comment1 comment -->\n\n'] )
  a = x = y = z = 10;  s='hello '
  _m.extend( ['\n  '] )
  # for i in range(1) :
  for i in range(1) :    
    pass  
  _m.extend( ['\n\n  '] )
  # for i in range(1):
  for i in range(1):    
    pass  
  _m.extend( ['\n    \n  '] )
  # for i in range(1):
  for i in range(1):    
    pass  
  _m.extend( ['\n  '] )
  # for i in range(2) :
  for i in range(2) :    
    _m.extend( ['Google will join its biggest mobile rival, Apple, on the space trip as well.', '\n  ', 'Apple\'s iPhone 4 will join a crew running an app, called "SpaceLab for iOS."', '\n\n'] )  
  _m.extend( ['\n  '] )
  # for i in range(1):
  for i in range(1):    
    _m.pushbuf()
    _m.extend( ['<html #std1 .testcase.sample \n        { color: red; font-size : '] )
    _m.append(_m.evalexprs( 'z*2', '', globals(), locals()) )
    _m.extend( ['px } title="hello world">'] )
    _m.pushbuf()
    _m.extend( ['\n    '] )
    _m.pushbuf()
    _m.extend( ['<head>'] )
    _m.pushbuf()
    _m.extend( ['\n    '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.pushbuf()
    _m.extend( ['<body>'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    _m.pushbuf()
    _m.extend( ['<abbr "World Health Organization">'] )
    _m.pushbuf()
    _m.extend( [' WHO', '\n  \n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.pushbuf()
    _m.extend( ['<button #id_ reset disabled makefriend "button value">'] )
    _m.pushbuf()
    _m.extend( ['\n\n'] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')  
  _m.extend( ['\n   \n  '] )
  # for i in range(2):
  for i in range(2):    
    _m.pushbuf()
    _m.extend( ['<div>'] )
    _m.pushbuf()
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '"hello " + str([ str(10) ]) + \' world\'', '', globals(), locals()) )
    _m.extend( ['\n    '] )
    _m.pushbuf()
    _m.extend( ['<a #'] )
    _m.append(_m.evalexprs( "'idname \\ '", '', globals(), locals()) )
    _m.extend( [' .'] )
    _m.append(_m.evalexprs( "'cls' 'name'", '', globals(), locals()) )
    _m.extend( [' "'] )
    _m.append(_m.evalexprs( '"http://" \'google.com\'', '', globals(), locals()) )
    _m.extend( ['" \n       { '] )
    _m.append(_m.evalexprs( "'color : '", '', globals(), locals()) )
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '"red;"', '', globals(), locals()) )
    _m.extend( [' } \n       '] )
    _m.append(_m.evalexprs( '"title"', '', globals(), locals()) )
    _m.extend( ['="'] )
    _m.append(_m.evalexprs( '"sun is " " shining"', '', globals(), locals()) )
    _m.extend( [' brightly">'] )
    _m.pushbuf()
    _m.extend( ['\n'] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')  
  _m.extend( ['\n\n  '] )
  # for i in range(1) :
  for i in range(1) :    
    _m.pushbuf()
    _m.extend( ['<div {} >'] )
    _m.pushbuf()
    _m.extend( ['\n\n    '] )
    _m.pushbuf()
    _m.extend( ['<a #'] )
    _m.append(_m.evalexprs( "'idname'", '', globals(), locals()) )
    _m.extend( [' .'] )
    _m.append(_m.evalexprs( "'cls'", '', globals(), locals()) )
    _m.extend( ['\n   \n      "http://pluggdapps.com"\n      { '] )
    _m.append(_m.evalexprs( "'color : '", '', globals(), locals()) )
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '"red;"', '', globals(), locals()) )
    _m.extend( [" ' style with line\n        break' } >"] )
    _m.pushbuf()
    _m.extend( [' hello {world} /> ', '\n\n'] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')  
  _m.extend( ['\n  '] )
  # for i in range(1) :
  for i in range(1) :    
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
    _m.append(_m.evalexprs( 's.strip(\n    )', '', globals(), locals()) )
    _m.extend( [' "title" {color:red} lang="en"\n     data="hello">'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    _m.pushbuf()
    _m.extend( ['<title #titleid .cls1 "title \n        string">'] )
    _m.pushbuf()
    _m.extend( [' hello '] )
    _m.append(_m.evalexprs( 's', '', globals(), locals()) )
    _m.extend( [' @ ! # "helo" \'world "ok', '\n    '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.pushbuf()
    _m.extend( ['<body>'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    _m.pushbuf()
    _m.extend( ['<h1 { color : red;\n  border : 1px solid gray;\n      }>'] )
    _m.pushbuf()
    _m.extend( [' I am the space station '] )
    _m.append(_m.evalexprs( '"These "', '', globals(), locals()) )
    _m.extend( [' seven cameras', '\n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.extend( ['<!--', ' comment1\n     comment ', '-->', '\n      ', 'have a zoom range', '\n      '] )
    _m.pushbuf()
    _m.extend( ['<p first\n      second>'] )
    _m.pushbuf()
    _m.extend( [' of any 12x or more,', '\n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.extend( ['<!--', ' comment1\n         comment ', '-->', '\n      ', 'and some of the wide-angle view', '\n      '] )
    _m.pushbuf()
    _m.extend( ['<div>'] )
    _m.pushbuf()
    _m.extend( [' of good. They also have a', '\n        ', 'lot of image stabilization (either optical or mechanical), which is', '\n        ', 'important for people who are with a powerful zoom lens. Some other', '\n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.extend( ['important features thatThese cameras contain electronic viewfinder,', '\n        ', '<!--', ' comment1 comment ', '-->', '\n  \n    '] )
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
  _m.extend( ['\n  '] )
  # for i in range(1) :
  for i in range(1) :    
    world = 10
    _m.pushbuf()
    _m.extend( ['<form #idname\n  formname "', 'http://\n  google.com" >'] )
    _m.pushbuf()
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '"hello " + str(10) +     \' world\'', '', globals(), locals()) )
    _m.extend( ['\n      '] )
    _m.pushbuf()
    _m.extend( ["<input text  =$_0(*&^%%$#@!@~}= world }$ {' title= hello "] )
    _m.append(_m.evalexprs( 'world', '', globals(), locals()) )
    _m.extend( ['}>'] )
    _m.pushbuf()
    _m.extend( ['\n'] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')  
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/forblock.ttl' 