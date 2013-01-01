import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *


def body( a=10, x=10, y=10, z=10, s='hello ', *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( [''] )
  _m.append(_m.evalexprs( "func( 'pass', x, y, z, s )", '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( "func( ':', x, y, z, s )", '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func( 1, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func( 2, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func( 3, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func( 4, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func( 5, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func( 6, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func( 7, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func( 10, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n'] )
  return _m.popbuftext()

# ---- Global Functions

def func( a, x, y, z, s ) :  
  _m.pushbuf()
  # if a == 'pass' :
  if a == 'pass' :    
    pass  
  # elif a == ':' :
  elif a == ':' :    
    pass  
  # elif a == 1 :
  elif a == 1 :    
    _m.extend( ['Google will join its biggest mobile rival, Apple, on the space trip as', '\n    ', "well.  Apple's iPhone 4 will join a crew running an app, called", '\n    ', '"SpaceLab for iOS."', '\n  '] )  
  # elif a== 2 :
  elif a== 2 :    
    _m.extend( ['The program, designed by Odyssey Space Research, will allow crew members', '\n    ', "to conduct several experiments with the phones' cameras, gyroscopes and", '\n    ', 'other', '\n  '] )  
  # elif a == 3 :
  elif a == 3 :    
    _m.pushbuf()
    _m.extend( ['<html #std1 .testcase.sample { color: red; font-size : '] )
    _m.append(_m.evalexprs( 'z*2', '', globals(), locals()) )
    _m.extend( ['px }\n          title="hello world">'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    _m.pushbuf()
    _m.extend( ['<head>'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.pushbuf()
    _m.extend( ['<body>'] )
    _m.pushbuf()
    _m.extend( ['\n        '] )
    _m.pushbuf()
    _m.extend( ['<abbr "World Health Organization">'] )
    _m.pushbuf()
    _m.extend( [' WHO', '\n    \n        '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.pushbuf()
    _m.extend( ['<button #id_ reset disabled makefriend "button value">'] )
    _m.pushbuf()
    _m.extend( ['\n\n  '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')  
  # elif a == 4 :
  elif a == 4 :    
    _m.pushbuf()
    _m.extend( ['<div>'] )
    _m.pushbuf()
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '"hello " + str([ str(10) ]) + \' world\'', '', globals(), locals()) )
    _m.extend( ['\n      '] )
    _m.pushbuf()
    _m.extend( ['<a #'] )
    _m.append(_m.evalexprs( "'idname \\ '", '', globals(), locals()) )
    _m.extend( [' .'] )
    _m.append(_m.evalexprs( "'cls' 'name'", '', globals(), locals()) )
    _m.extend( [' \n         "'] )
    _m.append(_m.evalexprs( '"http://" \'google.com\'', '', globals(), locals()) )
    _m.extend( ['" { '] )
    _m.append(_m.evalexprs( "'color : '", '', globals(), locals()) )
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '"red;"', '', globals(), locals()) )
    _m.extend( [' } \n         '] )
    _m.append(_m.evalexprs( '"title"', '', globals(), locals()) )
    _m.extend( ['="'] )
    _m.append(_m.evalexprs( '"sun is " " shining"', '', globals(), locals()) )
    _m.extend( [' brightly">'] )
    _m.pushbuf()
    _m.extend( ['\n  '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')  
  # elif a == 5 :
  elif a == 5 :    
    _m.pushbuf()
    _m.extend( ['<div {} >'] )
    _m.pushbuf()
    _m.extend( ['\n\n      '] )
    _m.pushbuf()
    _m.extend( ['<a #'] )
    _m.append(_m.evalexprs( "'idname'", '', globals(), locals()) )
    _m.extend( [' .'] )
    _m.append(_m.evalexprs( "'cls'", '', globals(), locals()) )
    _m.extend( ['\n     \n        "http://pluggdapps.com"\n        { '] )
    _m.append(_m.evalexprs( "'color : '", '', globals(), locals()) )
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '"red;"', '', globals(), locals()) )
    _m.extend( [" ' style with line\n          break' } >"] )
    _m.pushbuf()
    _m.extend( [' hello {world} /> ', '\n  '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')  
  # elif a == 6 :
  elif a == 6 :    
    _m.pushbuf()
    _m.extend( ['<html>'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    b = 'hello'   
    _m.extend( [''] )
    _m.append(_m.evalexprs( 'x+y', '', globals(), locals()) )
    _m.extend( ['\n      '] )
    _m.pushbuf()
    _m.extend( ['<head #headid .cls1.'] )
    _m.append(_m.evalexprs( 's.strip()', '', globals(), locals()) )
    _m.extend( [' "title" {color:red} lang="en"\n       data="hello">'] )
    _m.pushbuf()
    _m.extend( ['\n        '] )
    _m.pushbuf()
    _m.extend( ['<title #titleid .cls1 "title \n          string">'] )
    _m.pushbuf()
    _m.extend( [' hello '] )
    _m.append(_m.evalexprs( 's', '', globals(), locals()) )
    _m.extend( [' @ ! # "helo" \'world "ok', '\n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.pushbuf()
    _m.extend( ['<body>'] )
    _m.pushbuf()
    _m.extend( ['\n        '] )
    _m.pushbuf()
    _m.extend( ['<h1 { color : red;\n    border : 1px solid gray;\n        }>'] )
    _m.pushbuf()
    _m.extend( [' I am the space station '] )
    _m.append(_m.evalexprs( '"These "', '', globals(), locals()) )
    _m.extend( [' seven cameras', '\n        '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.extend( ['<!--', ' comment1\n       comment ', '-->', '\n        ', 'have a zoom range', '\n        '] )
    _m.pushbuf()
    _m.extend( ['<p first\n        second>'] )
    _m.pushbuf()
    _m.extend( [' of any 12x or more,', '\n        '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.extend( ['<!--', ' comment1\n           comment ', '-->', '\n        ', 'and some of the wide-angle view', '\n        '] )
    _m.pushbuf()
    _m.extend( ['<div>'] )
    _m.pushbuf()
    _m.extend( [' of good. They also have a', '\n          ', 'lot of image stabilization (either optical or mechanical), which is', '\n          ', 'important for people who are with a powerful zoom lens. Some other', '\n        '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.extend( ['important features thatThese cameras contain electronic viewfinder,', '\n          ', '<!--', ' comment1 comment ', '-->', '\n    \n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.extend( ['full control while shooting. In general, these cameras are all seem', '\n        ', 'very similar.', '\n      \n        '] )
    _m.pushbuf()
    _m.extend( ['<p #'] )
    _m.append(_m.evalexprs( 'b', '', globals(), locals()) )
    _m.extend( ['>'] )
    _m.pushbuf()
    _m.extend( [' Sign my guestbook', '\n  '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')  
  # elif a == 7 :
  elif a == 7 :    
    world = 10
    _m.pushbuf()
    _m.extend( ['<form #idname\n    formname "', 'http://\n    google.com" >'] )
    _m.pushbuf()
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '"hello " + str(10) + \' world\'', '', globals(), locals()) )
    _m.extend( ['\n        '] )
    _m.pushbuf()
    _m.extend( ["<input text  =$_0(*&^%%$#@!@~}= world }$ {' title= hello "] )
    _m.append(_m.evalexprs( 'world', '', globals(), locals()) )
    _m.extend( ['}>'] )
    _m.pushbuf()
    _m.extend( ['\n  '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')  
  # else :
  else :    
    _m.extend( ['sensors. Each device will include step-by-step directions for the', '\n    ', 'astronauts, eliminating the need for printed instructions.', '\n\n'] )  
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/ifblock.ttl' 