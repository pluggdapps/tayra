import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin

def __traceback_decorator__( frames ):
    from copy    import deepcopy
    from os.path import basename

    def _map2ttl( frame ):
        filename = frame.filename
        lineno = frame.lineno
        lines = open(filename).readlines()[:lineno]
        lines.reverse()
        rc = {}
        for l in lines :
            if l.strip().startswith('# lineno') :
                _, ttl_lineno = l.split(':', 1)
                ttl_lineno = int( ttl_lineno )
                ttl_text = open( _ttlfile ).readlines()[ ttl_lineno-1 ]
                return ttl_lineno, ttl_text
        return None, None

    newframes = []
    for frame in frames :
        newframes.append( frame )
        frameadded = getattr( frame, '_ttlframeadded', False )

        basen = basename( frame.filename )
        if basen.endswith( '.ttl.py' )              and basen == (basename( _ttlfile ) + '.py')              and frameadded == False :
            newframe = deepcopy( frame )
            frame._ttlframeadded = True
            try :
                newframe.lineno, newframe.linetext = _map2ttl( newframe )
                if newframe.lineno :
                    newframe.filename = _ttlfile
                    newframes.append( newframe )
            except :
                raise
                continue
    return newframes



def body( *args, **kwargs ) :  
  _m.pushbuf()
  # lineno:83
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func1()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:84
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func2()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:85
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func3()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:86
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func4()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:87
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func5()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:88
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func6()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:89
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func7()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:90
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func8()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:91
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func10()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  return _m.popbuftext()

# ---- Global Functions

# lineno:1
def func1() :  
  _m.pushbuf()
  # lineno:2
  pass
  return _m.popbuftext()


# lineno:4
def func2( a=':' ) :  
  _m.pushbuf()
  # lineno:6
  pass
  return _m.popbuftext()


# lineno:8
def func3() :  
  _m.pushbuf()
  # lineno:9
  _m.extend( ['Google will join its biggest mobile rival, Apple, on the space trip as well.', '\n  '] )
  # lineno:10
  _m.extend( ['Apple\'s iPhone 4 will join a crew running an app, called "SpaceLab for iOS."', '\n'] )
  return _m.popbuftext()


# lineno:11
def func4() :  
  _m.pushbuf()
  # lineno:12
  _m.extend( ['The program, designed by Odyssey Space Research, will allow crew members to', '\n  '] )
  # lineno:13
  _m.extend( ["conduct several experiments with the phones' cameras, gyroscopes and other", '\n'] )
  return _m.popbuftext()


# lineno:14
def func5(z=10):  
  _m.pushbuf()
  # lineno:16
  _m.pushbuf()
  _m.extend( ['<html #std1 .testcase.sample { color: red; font-size : '] )
  _m.append(_m.evalexprs( '', 'z*2', '', globals(), locals()) )
  _m.extend( ['px }\n        title="hello world">'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:18
  _m.pushbuf()
  _m.extend( ['<head>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:19
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:20
  _m.pushbuf()
  _m.extend( ['<abbr "World Health Organization">'] )
  _m.pushbuf()
  # lineno:20
  _m.extend( [' WHO', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  
  # lineno:21
  def nestedfunc() :    
    _m.pushbuf()
    # lineno:22
    _m.pushbuf()
    _m.extend( ['<b>'] )
    _m.pushbuf()
    # lineno:22
    _m.extend( [' this is nested function', '\n        '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    
    # lineno:23
    def nestednestedfunc() :      
      _m.pushbuf()
      # lineno:24
      _m.pushbuf()
      _m.extend( ['<em>'] )
      _m.pushbuf()
      # lineno:24
      _m.extend( [' this is nested nested function', '\n        '] )
      _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
      return _m.popbuftext()    
    
    # lineno:25
    _m.extend( [''] )
    _m.append(_m.evalexprs( '', 'nestednestedfunc()', '', globals(), locals()) )
    _m.extend( ['\n      '] )
    return _m.popbuftext()  
  
  # lineno:26
  _m.pushbuf()
  _m.extend( ['<button #id_ reset disabled makefriend "button value">'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:27
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'nestedfunc()', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()


# lineno:29
def func6 () :  
  _m.pushbuf()
  # lineno:31
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  # lineno:31
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '', '"hello " + str([ str(10) ]) + \' world\'', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:32
  _m.pushbuf()
  _m.extend( ['<a #'] )
  _m.append(_m.evalexprs( '', "'idname  \\ '", '', globals(), locals()) )
  _m.extend( [' .'] )
  _m.append(_m.evalexprs( '', "'cls' 'name'", '', globals(), locals()) )
  _m.extend( [' \n       "'] )
  _m.append(_m.evalexprs( '', '"http://" \'google.com\'', '', globals(), locals()) )
  _m.extend( ['" { '] )
  _m.append(_m.evalexprs( '', "'color : '", '', globals(), locals()) )
  _m.extend( ['\n                               '] )
  _m.append(_m.evalexprs( '', '"red;"', '', globals(), locals()) )
  _m.extend( [' } \n                               '] )
  _m.append(_m.evalexprs( '', '"title"', '', globals(), locals()) )
  _m.extend( ['="'] )
  _m.append(_m.evalexprs( '', '"sun is " " shining"', '', globals(), locals()) )
  _m.extend( [' brightly">'] )
  _m.pushbuf()
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()


# lineno:36
def func7() :  
  _m.pushbuf()
  # lineno:38
  _m.pushbuf()
  _m.extend( ['<div {} >'] )
  _m.pushbuf()
  _m.extend( ['\n\n    '] )
  # lineno:40
  _m.pushbuf()
  _m.extend( ['<a #'] )
  _m.append(_m.evalexprs( '', "'idname'", '', globals(), locals()) )
  _m.extend( [' .'] )
  _m.append(_m.evalexprs( '', "'cls'", '', globals(), locals()) )
  _m.extend( ['\n   \n      "http://pluggdapps.com"\n      { '] )
  _m.append(_m.evalexprs( '', "'color : '", '', globals(), locals()) )
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '', '"red;"', '', globals(), locals()) )
  _m.extend( [" ' style with line\n        break' } >"] )
  _m.pushbuf()
  # lineno:44
  _m.extend( [' hello {world} /> ', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()


# lineno:45
def func8( a=10, b=12.2, c="string" ) :  
  _m.pushbuf()
  # lineno:46
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:47
  b = 'hello'   
  # lineno:48
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'a+2', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:49
  _m.pushbuf()
  _m.extend( ['<head #headid .cls1.'] )
  _m.append(_m.evalexprs( '', 'c.strip(\n        )', '', globals(), locals()) )
  _m.extend( [' "title" {color:red} lang="en"\n     data="hello">'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:52
  _m.pushbuf()
  _m.extend( ['<title #titleid .cls1 "title \n        string">'] )
  _m.pushbuf()
  # lineno:53
  _m.extend( [' hello '] )
  _m.append(_m.evalexprs( '', 'c', '', globals(), locals()) )
  _m.extend( [' @ ! # "helo" \'world "ok', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:54
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:55
  _m.pushbuf()
  _m.extend( ['<h1 { color : red;\n  border : 1px solid gray;\n      }>'] )
  _m.pushbuf()
  # lineno:57
  _m.extend( [' I am the space station '] )
  _m.append(_m.evalexprs( '', '"These "', '', globals(), locals()) )
  _m.extend( [' seven cameras', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.extend( ['<!--', ' comment1\n     comment ', '-->', '\n      '] )
  # lineno:60
  _m.extend( ['have a zoom range ', '\n      '] )
  # lineno:61
  _m.pushbuf()
  _m.extend( ['<p first\n      second>'] )
  _m.pushbuf()
  # lineno:62
  _m.extend( [' of any 12x or more,', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.extend( ['<!--', ' comment1\n         comment ', '-->', '\n      '] )
  # lineno:65
  _m.extend( ['and some of the wide-angle view ', '\n      '] )
  # lineno:66
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  # lineno:66
  _m.extend( [' of good. They also have a', '\n        '] )
  # lineno:67
  _m.extend( ['lot of image stabilization (either optical or mechanical), which is ', '\n        '] )
  # lineno:68
  _m.extend( ['important for people who are with a powerful zoom lens. Some other', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:69
  _m.extend( ['important features thatThese cameras contain electronic viewfinder,', '\n        ', '<!--', ' comment1 comment ', '-->', '\n  \n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:72
  _m.extend( ['full control while shooting. In general, these cameras are all seem ', '\n      '] )
  # lineno:73
  _m.extend( ['very similar.', '\n    \n      '] )
  # lineno:75
  _m.pushbuf()
  _m.extend( ['<p #'] )
  _m.append(_m.evalexprs( '', 'b', '', globals(), locals()) )
  _m.extend( ['>'] )
  _m.pushbuf()
  # lineno:75
  _m.extend( [' Sign my guestbook', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()


# lineno:76
def func10():  
  _m.pushbuf()
  # lineno:77
  world = 10
  # lineno:79
  _m.pushbuf()
  _m.extend( ['<form #idname formname "', 'http://\n  google.com" >'] )
  _m.pushbuf()
  # lineno:80
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '', '"hello " + str(10) + \' world\'', '', globals(), locals()) )
  _m.extend( ['\n      '] )
  # lineno:81
  _m.pushbuf()
  _m.extend( ["<input text  =$_0(*&^%%$#@!@~}= world }$ {' title= hello "] )
  _m.append(_m.evalexprs( '', 'world', '', globals(), locals()) )
  _m.extend( ['}>'] )
  _m.pushbuf()
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
