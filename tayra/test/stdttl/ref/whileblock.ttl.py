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
  # lineno:1
  a = x = y = z = 10;  s='hello '
  # lineno:3
  _m.pushbuf()
  _m.extend( ['<table>'] )
  _m.pushbuf()
  _m.extend( ['\n  ', '\n    '] )
  # lineno:4
  for i in range(100):    
    # lineno:5
    _m.pushbuf()
    _m.extend( ['<tr>'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    # lineno:6
    j = 0
    _m.extend( ['\n        '] )
    # lineno:7
    while j < 4 :      
      # lineno:8
      _m.pushbuf()
      _m.extend( ['<td>'] )
      _m.pushbuf()
      # lineno:8
      _m.extend( [' sample text', '\n        '] )
      _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
      # lineno:9
      j += 1    
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')  
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['\n     \n  '] )
  # lineno:11
  while False :    
    # lineno:13
    pass
    _m.extend( ['<!--', '  comment ', '--> ', '\n    \n'] )  
  # lineno:17
  i = 1
  _m.extend( ['\n  '] )
  # lineno:18
  while i :    
    # lineno:19
    i -= 1  
  # lineno:21
  i = 1
  _m.extend( ['\n  '] )
  # lineno:22
  while i :    
    _m.extend( ['<!--', '  comment ', '--> ', '\n  '] )
    # lineno:24
    i -= 1  
  # lineno:27
  i = 1
  _m.extend( ['\n  '] )
  # lineno:28
  while i :    
    # lineno:29
    _m.extend( ['Google will join its biggest mobile rival, Apple, on the space trip as well.', '\n  '] )
    # lineno:30
    _m.extend( ['Apple\'s iPhone 4 will join a crew running an app, called "SpaceLab for iOS."', '\n  '] )
    # lineno:31
    i -= 1  
  _m.extend( ['\n  '] )
  # lineno:33
  while i :    
    # lineno:34
    _m.pushbuf()
    _m.extend( ['<html #std1 .testcase.sample { color: red; font-size : '] )
    _m.append(_m.evalexprs( '', 'z*2', '', globals(), locals()) )
    _m.extend( ['px }\n        title="hello world">'] )
    _m.pushbuf()
    _m.extend( ['\n    '] )
    # lineno:36
    _m.pushbuf()
    _m.extend( ['<head>'] )
    _m.pushbuf()
    _m.extend( ['\n    '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    # lineno:37
    _m.pushbuf()
    _m.extend( ['<body>'] )
    _m.pushbuf()
    _m.extend( ['\n      '] )
    # lineno:38
    i -= 1
    # lineno:39
    _m.pushbuf()
    _m.extend( ['<abbr "World Health Organization">'] )
    _m.pushbuf()
    # lineno:39
    _m.extend( [' WHO', '\n  \n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    # lineno:41
    _m.pushbuf()
    _m.extend( ['<button #id_ reset disabled makefriend "button value">'] )
    _m.pushbuf()
    _m.extend( ['\n\n'] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')  
  # lineno:43
  i = 1
  _m.extend( ['\n   \n  '] )
  # lineno:44
  while i :    
    # lineno:46
    _m.pushbuf()
    _m.extend( ['<div>'] )
    _m.pushbuf()
    # lineno:46
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '', '"hello " + str([ str(10) ]) + \' world\'', '', globals(), locals()) )
    _m.extend( ['\n    '] )
    # lineno:47
    i -= 1
    # lineno:48
    j = 1
    # lineno:49
    _m.pushbuf()
    _m.extend( ['<a #'] )
    _m.append(_m.evalexprs( '', "'idname'", '', globals(), locals()) )
    _m.extend( [' .'] )
    _m.append(_m.evalexprs( '', "'cls' 'name'", '', globals(), locals()) )
    _m.extend( [' "'] )
    _m.append(_m.evalexprs( '', '"http://" \'google.com\'', '', globals(), locals()) )
    _m.extend( ['"\n       { '] )
    _m.append(_m.evalexprs( '', "'color : '", '', globals(), locals()) )
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '', '"red;"', '', globals(), locals()) )
    _m.extend( [' } \n       '] )
    _m.append(_m.evalexprs( '', '"title"', '', globals(), locals()) )
    _m.extend( ['="'] )
    _m.append(_m.evalexprs( '', '"sun is " " shining"', '', globals(), locals()) )
    _m.extend( [' brightly">'] )
    _m.pushbuf()
    _m.extend( ['\n  '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.extend( ['\n\n    '] )
    # lineno:52
    while j :      
      # lineno:54
      _m.pushbuf()
      _m.extend( ['<div {} >'] )
      _m.pushbuf()
      _m.extend( ['\n      '] )
      # lineno:55
      j -= 1
      # lineno:56
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
      # lineno:60
      _m.extend( [' hello {world} /> ', '\n\n  '] )
      _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
      _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')    
    _m.extend( ['\n    '] )
    # lineno:62
    for i in range(1) :      
      # lineno:63
      _m.pushbuf()
      _m.extend( ['<html>'] )
      _m.pushbuf()
      _m.extend( ['\n      '] )
      # lineno:64
      b = 'hello'   
      # lineno:65
      _m.extend( [''] )
      _m.append(_m.evalexprs( '', 'x+y', '', globals(), locals()) )
      _m.extend( ['\n      '] )
      # lineno:66
      _m.pushbuf()
      _m.extend( ['<head #headid .cls1.'] )
      _m.append(_m.evalexprs( '', 's.strip()', '', globals(), locals()) )
      _m.extend( [' "title" {color:red} lang="en"\n            data="hello">'] )
      _m.pushbuf()
      _m.extend( ['\n        '] )
      # lineno:68
      _m.pushbuf()
      _m.extend( ['<title #titleid .cls1 "title \n          string">'] )
      _m.pushbuf()
      # lineno:69
      _m.extend( [' hello '] )
      _m.append(_m.evalexprs( '', 's', '', globals(), locals()) )
      _m.extend( [' @ ! # "helo" \'world "ok', '\n      '] )
      _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
      _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
      # lineno:70
      _m.pushbuf()
      _m.extend( ['<body>'] )
      _m.pushbuf()
      _m.extend( ['\n        '] )
      # lineno:71
      _m.pushbuf()
      _m.extend( ['<h1 { color : red; border : 1px solid gray;\n        }>'] )
      _m.pushbuf()
      # lineno:72
      _m.extend( [' I am the space station '] )
      _m.append(_m.evalexprs( '', '"These "', '', globals(), locals()) )
      _m.extend( [' seven cameras', '\n        '] )
      _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
      _m.extend( ['<!--', ' comment1\n       comment ', '-->', '\n        '] )
      # lineno:75
      _m.extend( ['have a zoom range ', '\n        '] )
      # lineno:76
      _m.pushbuf()
      _m.extend( ['<p first\n        second>'] )
      _m.pushbuf()
      # lineno:77
      _m.extend( [' of any 12x or more,', '\n        '] )
      _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
      _m.extend( ['<!--', ' comment1\n           comment ', '-->', '\n        '] )
      # lineno:80
      _m.extend( ['and some of the wide-angle view ', '\n        '] )
      # lineno:81
      _m.pushbuf()
      _m.extend( ['<div>'] )
      _m.pushbuf()
      # lineno:81
      _m.extend( [' of good. They also have a', '\n          '] )
      # lineno:82
      _m.extend( ['lot of image stabilization (either optical or mechanical), which is ', '\n          '] )
      # lineno:83
      _m.extend( ['important for people who are with a powerful zoom lens. Some other', '\n        '] )
      _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
      # lineno:84
      _m.extend( ['important features thatThese cameras contain electronic viewfinder,', '\n          ', '<!--', ' comment1 comment ', '-->', '\n    \n      '] )
      _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
      # lineno:87
      _m.extend( ['full control while shooting. In general, these cameras are all seem ', '\n        '] )
      # lineno:88
      _m.extend( ['very similar.', '\n      \n        '] )
      # lineno:90
      _m.pushbuf()
      _m.extend( ['<p #'] )
      _m.append(_m.evalexprs( '', 'b', '', globals(), locals()) )
      _m.extend( ['>'] )
      _m.pushbuf()
      # lineno:90
      _m.extend( [' Sign my guestbook', '\n\n        '] )
      _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
      _m.extend( ['\n          '] )
      # lineno:92
      for i in range(1) :        
        # lineno:93
        world = 10
        # lineno:95
        _m.pushbuf()
        _m.extend( ['<form #idname formname "', 'http:// google.com" >'] )
        _m.pushbuf()
        # lineno:95
        _m.extend( [' ', '\n            '] )
        # lineno:96
        _m.extend( [''] )
        _m.append(_m.evalexprs( '', '"hello " + str(10) + \' world\'', '', globals(), locals()) )
        _m.extend( ['\n              '] )
        # lineno:97
        _m.pushbuf()
        _m.extend( ["<input text  =$_0(*&^%%$#@!@~}= world }$ {' title= hello "] )
        _m.append(_m.evalexprs( '', 'world', '', globals(), locals()) )
        _m.extend( ['}>'] )
        _m.pushbuf()
        _m.extend( ['\n\n'] )
        _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
        _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')      
      _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')      
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
