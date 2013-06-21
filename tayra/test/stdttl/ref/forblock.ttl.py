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
  _m.extend( ['<!-- comment1 comment -->\n\n'] )
  # lineno:3
  a = x = y = z = 10;  s='hello '
  _m.extend( ['\n  '] )
  # lineno:5
  for i in range(1) :    
    # lineno:6
    pass  
  _m.extend( ['\n\n  '] )
  # lineno:8
  for i in range(1):    
    # lineno:10
    pass  
  _m.extend( ['\n    \n  '] )
  # lineno:13
  for i in range(1):    
    # lineno:15
    pass  
  _m.extend( ['\n  '] )
  # lineno:17
  for i in range(2) :    
    # lineno:18
    _m.extend( ['Google will join its biggest mobile rival, Apple, on the space trip as well.', '\n  '] )
    # lineno:19
    _m.extend( ['Apple\'s iPhone 4 will join a crew running an app, called "SpaceLab for iOS."', '\n\n'] )  
  _m.extend( ['\n  '] )
  # lineno:21
  for i in range(1):    
    # lineno:22
    _m.pushbuf()
    _m.extend( ['<html #std1 .testcase.sample \n        { color: red; font-size : '] )
    _m.append(_m.evalexprs( '', 'z*2', '', globals(), locals()) )
    _m.extend( ['px } title="hello world">'] )
    _m.pushbuf()
    _m.extend( ['\n    '] )
    # lineno:24
    _m.pushbuf()
    _m.extend( ['<head>'] )
    _m.pushbuf()
    _m.extend( ['\n    '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    # lineno:25
    _m.pushbuf()
    _m.extend( ['<body>'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    # lineno:26
    _m.pushbuf()
    _m.extend( ['<abbr "World Health Organization">'] )
    _m.pushbuf()
    # lineno:26
    _m.extend( [' WHO', '\n  \n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    # lineno:28
    _m.pushbuf()
    _m.extend( ['<button #id_ reset disabled makefriend "button value">'] )
    _m.pushbuf()
    _m.extend( ['\n\n'] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )  
  _m.extend( ['\n   \n  '] )
  # lineno:30
  for i in range(2):    
    # lineno:32
    _m.pushbuf()
    _m.extend( ['<div>'] )
    _m.pushbuf()
    # lineno:32
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '', '"hello " + str([ str(10) ]) + \' world\'', '', globals(), locals()) )
    _m.extend( ['\n    '] )
    # lineno:33
    _m.pushbuf()
    _m.extend( ['<a #'] )
    _m.append(_m.evalexprs( '', "'idname \\ '", '', globals(), locals()) )
    _m.extend( [' .'] )
    _m.append(_m.evalexprs( '', "'cls' 'name'", '', globals(), locals()) )
    _m.extend( [' "'] )
    _m.append(_m.evalexprs( '', '"http://" \'google.com\'', '', globals(), locals()) )
    _m.extend( ['" \n       { '] )
    _m.append(_m.evalexprs( '', "'color : '", '', globals(), locals()) )
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '', '"red;"', '', globals(), locals()) )
    _m.extend( [' } \n       '] )
    _m.append(_m.evalexprs( '', '"title"', '', globals(), locals()) )
    _m.extend( ['="'] )
    _m.append(_m.evalexprs( '', '"sun is " " shining"', '', globals(), locals()) )
    _m.extend( [' brightly">'] )
    _m.pushbuf()
    _m.extend( ['\n\n'] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )  
  _m.extend( ['\n\n  '] )
  # lineno:37
  for i in range(1) :    
    # lineno:39
    _m.pushbuf()
    _m.extend( ['<div {} >'] )
    _m.pushbuf()
    _m.extend( ['\n\n    '] )
    # lineno:41
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
    # lineno:45
    _m.extend( [' hello {world} /> ', '\n\n'] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )  
  _m.extend( ['\n  '] )
  # lineno:47
  for i in range(1) :    
    # lineno:48
    _m.pushbuf()
    _m.extend( ['<html>'] )
    _m.pushbuf()
    _m.extend( ['\n    '] )
    # lineno:49
    b = 'hello'   
    # lineno:50
    _m.extend( [''] )
    _m.append(_m.evalexprs( '', 'x+y', '', globals(), locals()) )
    _m.extend( ['\n    '] )
    # lineno:51
    _m.pushbuf()
    _m.extend( ['<head #headid .cls1.'] )
    _m.append(_m.evalexprs( '', 's.strip(\n    )', '', globals(), locals()) )
    _m.extend( [' "title" {color:red} lang="en"\n     data="hello">'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    # lineno:54
    _m.pushbuf()
    _m.extend( ['<title #titleid .cls1 "title \n        string">'] )
    _m.pushbuf()
    # lineno:55
    _m.extend( [' hello '] )
    _m.append(_m.evalexprs( '', 's', '', globals(), locals()) )
    _m.extend( [' @ ! # "helo" \'world "ok', '\n    '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    # lineno:56
    _m.pushbuf()
    _m.extend( ['<body>'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    # lineno:57
    _m.pushbuf()
    _m.extend( ['<h1 { color : red;\n  border : 1px solid gray;\n      }>'] )
    _m.pushbuf()
    # lineno:59
    _m.extend( [' I am the space station '] )
    _m.append(_m.evalexprs( '', '"These "', '', globals(), locals()) )
    _m.extend( [' seven cameras', '\n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.extend( ['<!--', ' comment1\n     comment ', '-->', '\n      '] )
    # lineno:62
    _m.extend( ['have a zoom range ', '\n      '] )
    # lineno:63
    _m.pushbuf()
    _m.extend( ['<p first\n      second>'] )
    _m.pushbuf()
    # lineno:64
    _m.extend( [' of any 12x or more,', '\n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.extend( ['<!--', ' comment1\n         comment ', '-->', '\n      '] )
    # lineno:67
    _m.extend( ['and some of the wide-angle view ', '\n      '] )
    # lineno:68
    _m.pushbuf()
    _m.extend( ['<div>'] )
    _m.pushbuf()
    # lineno:68
    _m.extend( [' of good. They also have a', '\n        '] )
    # lineno:69
    _m.extend( ['lot of image stabilization (either optical or mechanical), which is ', '\n        '] )
    # lineno:70
    _m.extend( ['important for people who are with a powerful zoom lens. Some other', '\n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    # lineno:71
    _m.extend( ['important features thatThese cameras contain electronic viewfinder,', '\n        ', '<!--', ' comment1 comment ', '-->', '\n  \n    '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    # lineno:74
    _m.extend( ['full control while shooting. In general, these cameras are all seem ', '\n      '] )
    # lineno:75
    _m.extend( ['very similar.', '\n    \n      '] )
    # lineno:77
    _m.pushbuf()
    _m.extend( ['<p #'] )
    _m.append(_m.evalexprs( '', 'b', '', globals(), locals()) )
    _m.extend( ['>'] )
    _m.pushbuf()
    # lineno:77
    _m.extend( [' Sign my guestbook', '\n\n'] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )  
  _m.extend( ['\n  '] )
  # lineno:79
  for i in range(1) :    
    # lineno:80
    world = 10
    # lineno:82
    _m.pushbuf()
    _m.extend( ['<form #idname\n  formname "', 'http://\n  google.com" >'] )
    _m.pushbuf()
    # lineno:84
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '', '"hello " + str(10) +     \' world\'', '', globals(), locals()) )
    _m.extend( ['\n      '] )
    # lineno:85
    _m.pushbuf()
    _m.extend( ["<input text  =$_0(*&^%%$#@!@~}= world }$ {' title= hello "] )
    _m.append(_m.evalexprs( '', 'world', '', globals(), locals()) )
    _m.extend( ['}>'] )
    _m.pushbuf()
    _m.extend( ['\n'] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )  
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
