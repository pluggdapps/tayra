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



def body( x=10, y=10, a="cls2 ", b="cls3", *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ["<!--\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\nCopyright (c) 2011 R Pratap Chakravarthy\n-->\n\n"] )
  # lineno:12
  m = 10
  # lineno:15
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  # lineno:16
  b = 'hello'   
  # lineno:17
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'x+y', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  # lineno:18
  _m.pushbuf()
  _m.extend( ['<head #headid .cls1.'] )
  _m.append(_m.evalexprs( '', 'a.strip()', '', globals(), locals()) )
  _m.extend( [' "title" {color:red} lang="en"\n   data="hello">'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:20
  _m.pushbuf()
  _m.extend( ['<title #titleid .cls1 "title \n      string">'] )
  _m.pushbuf()
  # lineno:21
  _m.extend( [' hello '] )
  _m.append(_m.evalexprs( '', 'a', '', globals(), locals()) )
  _m.extend( [' @ ! # "helo" \'world "ok', '\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:22
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:23
  _m.pushbuf()
  _m.extend( ['<h1 { color : red; border : 1px solid gray;\n    }>'] )
  _m.pushbuf()
  # lineno:24
  _m.extend( [' I am the space station '] )
  _m.append(_m.evalexprs( '', '"These "', '', globals(), locals()) )
  _m.extend( [' seven cameras', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['<!--', ' comment1\n   comment ', '-->', '\n    '] )
  # lineno:27
  _m.extend( ['have a zoom range ', '\n    '] )
  # lineno:28
  _m.pushbuf()
  _m.extend( ['<p first\n    second>'] )
  _m.pushbuf()
  # lineno:29
  _m.extend( [' of any 12x or more,', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['<!--', ' comment1\n       comment ', '-->', '\n    '] )
  # lineno:32
  _m.extend( ['and some of the wide-angle view ', '\n    '] )
  # lineno:33
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  # lineno:33
  _m.extend( [' of good. They also have a', '\n      '] )
  # lineno:34
  _m.extend( ['lot of image stabilization (either optical or mechanical), which is ', '\n      '] )
  # lineno:35
  _m.extend( ['important for people who are with a powerful zoom lens. Some other', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:36
  _m.extend( ['important features thatThese cameras contain electronic viewfinder,', '\n      ', '<!--', ' comment1 comment ', '-->', '\n\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:39
  _m.extend( ['full control while shooting. In general, these cameras are all seem ', '\n    '] )
  # lineno:40
  _m.extend( ['very similar.', '\n  \n    '] )
  # lineno:42
  _m.pushbuf()
  _m.extend( ['<p #'] )
  _m.append(_m.evalexprs( '', 'b', '', globals(), locals()) )
  _m.extend( ['>'] )
  _m.pushbuf()
  # lineno:42
  _m.extend( [' Sign my guestbook', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
