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



def body( a=10, x=10, y=10, z=10, s='hello ', *args, **kwargs ) :  
  _m.pushbuf()
  # lineno:86
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', "func( 'pass', x, y, z, s )", '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:87
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', "func( ':', x, y, z, s )", '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:88
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func( 1, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:89
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func( 2, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:90
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func( 3, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:91
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func( 4, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:92
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func( 5, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:93
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func( 6, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:94
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func( 7, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n'] )
  # lineno:95
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'func( 10, x, y, z, s )', '', globals(), locals()) )
  _m.extend( ['\n'] )
  return _m.popbuftext()

# ---- Global Functions

# lineno:3
def func( a, x, y, z, s ) :  
  _m.pushbuf()
  # lineno:4
  if a == 'pass' :    
    # lineno:6
    pass  
  # lineno:8
  elif a == ':' :    
    # lineno:10
    pass  
  # lineno:12
  elif a == 1 :    
    # lineno:13
    _m.extend( ['Google will join its biggest mobile rival, Apple, on the space trip as', '\n    '] )
    # lineno:14
    _m.extend( ["well.  Apple's iPhone 4 will join a crew running an app, called", '\n    '] )
    # lineno:15
    _m.extend( ['"SpaceLab for iOS."', '\n  '] )  
  # lineno:16
  elif a== 2 :    
    # lineno:17
    _m.extend( ['The program, designed by Odyssey Space Research, will allow crew members', '\n    '] )
    # lineno:18
    _m.extend( ["to conduct several experiments with the phones' cameras, gyroscopes and", '\n    '] )
    # lineno:19
    _m.extend( ['other', '\n  '] )  
  # lineno:20
  elif a == 3 :    
    # lineno:22
    _m.pushbuf()
    _m.extend( ['<html #std1 .testcase.sample { color: red; font-size : '] )
    _m.append(_m.evalexprs( '', 'z*2', '', globals(), locals()) )
    _m.extend( ['px }\n          title="hello world">'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    # lineno:24
    _m.pushbuf()
    _m.extend( ['<head>'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    # lineno:25
    _m.pushbuf()
    _m.extend( ['<body>'] )
    _m.pushbuf()
    _m.extend( ['\n        '] )
    # lineno:26
    _m.pushbuf()
    _m.extend( ['<abbr "World Health Organization">'] )
    _m.pushbuf()
    # lineno:26
    _m.extend( [' WHO', '\n    \n        '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    # lineno:28
    _m.pushbuf()
    _m.extend( ['<button #id_ reset disabled makefriend "button value">'] )
    _m.pushbuf()
    _m.extend( ['\n\n  '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )  
  # lineno:30
  elif a == 4 :    
    # lineno:32
    _m.pushbuf()
    _m.extend( ['<div>'] )
    _m.pushbuf()
    # lineno:32
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '', '"hello " + str([ str(10) ]) + \' world\'', '', globals(), locals()) )
    _m.extend( ['\n      '] )
    # lineno:33
    _m.pushbuf()
    _m.extend( ['<a #'] )
    _m.append(_m.evalexprs( '', "'idname \\ '", '', globals(), locals()) )
    _m.extend( [' .'] )
    _m.append(_m.evalexprs( '', "'cls' 'name'", '', globals(), locals()) )
    _m.extend( [' \n         "'] )
    _m.append(_m.evalexprs( '', '"http://" \'google.com\'', '', globals(), locals()) )
    _m.extend( ['" { '] )
    _m.append(_m.evalexprs( '', "'color : '", '', globals(), locals()) )
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '', '"red;"', '', globals(), locals()) )
    _m.extend( [' } \n         '] )
    _m.append(_m.evalexprs( '', '"title"', '', globals(), locals()) )
    _m.extend( ['="'] )
    _m.append(_m.evalexprs( '', '"sun is " " shining"', '', globals(), locals()) )
    _m.extend( [' brightly">'] )
    _m.pushbuf()
    _m.extend( ['\n  '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )  
  # lineno:36
  elif a == 5 :    
    # lineno:38
    _m.pushbuf()
    _m.extend( ['<div {} >'] )
    _m.pushbuf()
    _m.extend( ['\n\n      '] )
    # lineno:40
    _m.pushbuf()
    _m.extend( ['<a #'] )
    _m.append(_m.evalexprs( '', "'idname'", '', globals(), locals()) )
    _m.extend( [' .'] )
    _m.append(_m.evalexprs( '', "'cls'", '', globals(), locals()) )
    _m.extend( ['\n     \n        "http://pluggdapps.com"\n        { '] )
    _m.append(_m.evalexprs( '', "'color : '", '', globals(), locals()) )
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '', '"red;"', '', globals(), locals()) )
    _m.extend( [" ' style with line\n          break' } >"] )
    _m.pushbuf()
    # lineno:44
    _m.extend( [' hello {world} /> ', '\n  '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )  
  # lineno:45
  elif a == 6 :    
    # lineno:46
    _m.pushbuf()
    _m.extend( ['<html>'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    # lineno:47
    b = 'hello'   
    # lineno:48
    _m.extend( [''] )
    _m.append(_m.evalexprs( '', 'x+y', '', globals(), locals()) )
    _m.extend( ['\n      '] )
    # lineno:49
    _m.pushbuf()
    _m.extend( ['<head #headid .cls1.'] )
    _m.append(_m.evalexprs( '', 's.strip()', '', globals(), locals()) )
    _m.extend( [' "title" {color:red} lang="en"\n       data="hello">'] )
    _m.pushbuf()
    _m.extend( ['\n        '] )
    # lineno:51
    _m.pushbuf()
    _m.extend( ['<title #titleid .cls1 "title \n          string">'] )
    _m.pushbuf()
    # lineno:52
    _m.extend( [' hello '] )
    _m.append(_m.evalexprs( '', 's', '', globals(), locals()) )
    _m.extend( [' @ ! # "helo" \'world "ok', '\n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    # lineno:53
    _m.pushbuf()
    _m.extend( ['<body>'] )
    _m.pushbuf()
    _m.extend( ['\n        '] )
    # lineno:54
    _m.pushbuf()
    _m.extend( ['<h1 { color : red;\n    border : 1px solid gray;\n        }>'] )
    _m.pushbuf()
    # lineno:56
    _m.extend( [' I am the space station '] )
    _m.append(_m.evalexprs( '', '"These "', '', globals(), locals()) )
    _m.extend( [' seven cameras', '\n        '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.extend( ['<!--', ' comment1\n       comment ', '-->', '\n        '] )
    # lineno:59
    _m.extend( ['have a zoom range ', '\n        '] )
    # lineno:60
    _m.pushbuf()
    _m.extend( ['<p first\n        second>'] )
    _m.pushbuf()
    # lineno:61
    _m.extend( [' of any 12x or more,', '\n        '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.extend( ['<!--', ' comment1\n           comment ', '-->', '\n        '] )
    # lineno:64
    _m.extend( ['and some of the wide-angle view ', '\n        '] )
    # lineno:65
    _m.pushbuf()
    _m.extend( ['<div>'] )
    _m.pushbuf()
    # lineno:65
    _m.extend( [' of good. They also have a', '\n          '] )
    # lineno:66
    _m.extend( ['lot of image stabilization (either optical or mechanical), which is ', '\n          '] )
    # lineno:67
    _m.extend( ['important for people who are with a powerful zoom lens. Some other', '\n        '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    # lineno:68
    _m.extend( ['important features thatThese cameras contain electronic viewfinder,', '\n          ', '<!--', ' comment1 comment ', '-->', '\n    \n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    # lineno:71
    _m.extend( ['full control while shooting. In general, these cameras are all seem ', '\n        '] )
    # lineno:72
    _m.extend( ['very similar.', '\n      \n        '] )
    # lineno:74
    _m.pushbuf()
    _m.extend( ['<p #'] )
    _m.append(_m.evalexprs( '', 'b', '', globals(), locals()) )
    _m.extend( ['>'] )
    _m.pushbuf()
    # lineno:74
    _m.extend( [' Sign my guestbook', '\n  '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )  
  # lineno:75
  elif a == 7 :    
    # lineno:76
    world = 10
    # lineno:78
    _m.pushbuf()
    _m.extend( ['<form #idname\n    formname "', 'http://\n    google.com" >'] )
    _m.pushbuf()
    # lineno:80
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '', '"hello " + str(10) + \' world\'', '', globals(), locals()) )
    _m.extend( ['\n        '] )
    # lineno:81
    _m.pushbuf()
    _m.extend( ["<input text  =$_0(*&^%%$#@!@~}= world }$ {' title= hello "] )
    _m.append(_m.evalexprs( '', 'world', '', globals(), locals()) )
    _m.extend( ['}>'] )
    _m.pushbuf()
    _m.extend( ['\n  '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )  
  # lineno:82
  else :    
    # lineno:83
    _m.extend( ['sensors. Each device will include step-by-step directions for the', '\n    '] )
    # lineno:84
    _m.extend( ['astronauts, eliminating the need for printed instructions.', '\n\n'] )  
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
