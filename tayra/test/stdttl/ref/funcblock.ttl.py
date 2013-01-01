import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'func1()', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func2()', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func3()', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func4()', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func5()', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func6()', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func7()', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func8()', '', globals(), locals()) )
  _m.extend( ['\n', ''] )
  _m.append(_m.evalexprs( 'func10()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  return _m.popbuftext()

# ---- Global Functions

def func1() :  
  _m.pushbuf()
  pass
  return _m.popbuftext()


def func2( a=':' ) :  
  _m.pushbuf()
  pass
  return _m.popbuftext()


def func3() :  
  _m.pushbuf()
  _m.extend( ['Google will join its biggest mobile rival, Apple, on the space trip as well.', '\n  ', 'Apple\'s iPhone 4 will join a crew running an app, called "SpaceLab for iOS."', '\n'] )
  return _m.popbuftext()


def func4() :  
  _m.pushbuf()
  _m.extend( ['The program, designed by Odyssey Space Research, will allow crew members to', '\n  ', "conduct several experiments with the phones' cameras, gyroscopes and other", '\n'] )
  return _m.popbuftext()


def func5(z=10):  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<html #std1 .testcase.sample { color: red; font-size : '] )
  _m.append(_m.evalexprs( 'z*2', '', globals(), locals()) )
  _m.extend( ['px }\n        title="hello world">'] )
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
  _m.extend( [' WHO', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  
  def nestedfunc() :    
    _m.pushbuf()
    _m.pushbuf()
    _m.extend( ['<b>'] )
    _m.pushbuf()
    _m.extend( [' this is nested function', '\n        '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    
    def nestednestedfunc() :      
      _m.pushbuf()
      _m.pushbuf()
      _m.extend( ['<em>'] )
      _m.pushbuf()
      _m.extend( [' this is nested nested function', '\n        '] )
      _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
      return _m.popbuftext()    
    
    _m.extend( [''] )
    _m.append(_m.evalexprs( 'nestednestedfunc()', '', globals(), locals()) )
    _m.extend( ['\n      '] )
    return _m.popbuftext()  
  
  _m.pushbuf()
  _m.extend( ['<button #id_ reset disabled makefriend "button value">'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'nestedfunc()', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()


def func6 () :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '"hello " + str([ str(10) ]) + \' world\'', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  _m.pushbuf()
  _m.extend( ['<a #'] )
  _m.append(_m.evalexprs( "'idname  \\ '", '', globals(), locals()) )
  _m.extend( [' .'] )
  _m.append(_m.evalexprs( "'cls' 'name'", '', globals(), locals()) )
  _m.extend( [' \n       "'] )
  _m.append(_m.evalexprs( '"http://" \'google.com\'', '', globals(), locals()) )
  _m.extend( ['" { '] )
  _m.append(_m.evalexprs( "'color : '", '', globals(), locals()) )
  _m.extend( ['\n                               '] )
  _m.append(_m.evalexprs( '"red;"', '', globals(), locals()) )
  _m.extend( [' } \n                               '] )
  _m.append(_m.evalexprs( '"title"', '', globals(), locals()) )
  _m.extend( ['="'] )
  _m.append(_m.evalexprs( '"sun is " " shining"', '', globals(), locals()) )
  _m.extend( [' brightly">'] )
  _m.pushbuf()
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()


def func7() :  
  _m.pushbuf()
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
  _m.extend( [' hello {world} /> ', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()


def func8( a=10, b=12.2, c="string" ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  b = 'hello'   
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'a+2', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  _m.pushbuf()
  _m.extend( ['<head #headid .cls1.'] )
  _m.append(_m.evalexprs( 'c.strip(\n        )', '', globals(), locals()) )
  _m.extend( [' "title" {color:red} lang="en"\n     data="hello">'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  _m.pushbuf()
  _m.extend( ['<title #titleid .cls1 "title \n        string">'] )
  _m.pushbuf()
  _m.extend( [' hello '] )
  _m.append(_m.evalexprs( 'c', '', globals(), locals()) )
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
  _m.extend( [' Sign my guestbook', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()


def func10():  
  _m.pushbuf()
  world = 10
  _m.pushbuf()
  _m.extend( ['<form #idname formname "', 'http://\n  google.com" >'] )
  _m.pushbuf()
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '"hello " + str(10) + \' world\'', '', globals(), locals()) )
  _m.extend( ['\n      '] )
  _m.pushbuf()
  _m.extend( ["<input text  =$_0(*&^%%$#@!@~}= world }$ {' title= hello "] )
  _m.append(_m.evalexprs( 'world', '', globals(), locals()) )
  _m.extend( ['}>'] )
  _m.pushbuf()
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '././test/stdttl/funcblock.ttl' 