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


import re

def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ["<!--\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\nCopyright (c) 2011 R Pratap Chakravarthy\n-->\n\n"] )
  # lineno:16
  _m.pushbuf()
  _m.extend( ['<global>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  # lineno:17
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'a', '', globals(), locals()) )
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '', 'insideroot_butglobal()', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  # lineno:18
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'b', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:20
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  # lineno:21
  b = 'hello'   
  # lineno:22
  c = '10px'
  # lineno:23
  _m.pushbuf()
  _m.extend( ['<head #headid .cls1.'] )
  _m.append(_m.evalexprs( '', 'a.strip()', '', globals(), locals()) )
  _m.extend( [' "title" {color:red;} lang="en" data="hello">'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:24
  _m.pushbuf()
  _m.extend( ['<body {margin : '] )
  _m.append(_m.evalexprs( '', 'c', '', globals(), locals()) )
  _m.extend( ['} >'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:28
  _m.pushbuf()
  _m.extend( ['<h1 { color : red; border : 1px solid gray; }>'] )
  _m.pushbuf()
  # lineno:28
  _m.extend( [' ', '\n      '] )
  # lineno:29
  _m.extend( ['I am the space station '] )
  _m.append(_m.evalexprs( '', '"These "', '', globals(), locals()) )
  _m.extend( [' seven cameras have a zoom range ', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:30
  _m.pushbuf()
  _m.extend( ['<p first second>'] )
  _m.pushbuf()
  # lineno:30
  _m.extend( [' of any 12x or more, '] )
  _m.append(_m.evalexprs( '', '20', '', globals(), locals()) )
  _m.extend( [' and some of the wide-angle view ', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:31
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  # lineno:31
  _m.extend( [' of good. They also have a', '\n      '] )
  # lineno:32
  _m.extend( ['lot of image stabilization (either optical or mechanical), which is ', '\n      '] )
  # lineno:33
  _m.extend( ['important for people who are with a powerful zoom lens. Some other        ', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:34
  _m.pushbuf()
  _m.extend( ['<p #'] )
  _m.append(_m.evalexprs( '', 'b', '', globals(), locals()) )
  _m.extend( ['>'] )
  _m.pushbuf()
  # lineno:34
  _m.extend( [' Sign my guestbook', '\n      '] )
  # lineno:35
  _m.pushbuf()
  _m.extend( ['<abbr>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:36
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'helloworld()', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:37
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'insideroot_butglobal()', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# lineno:11
a = 'empty'
# lineno:12
def insideroot_butglobal():
# lineno:13
  return '<div> insideroot_butglobal </div>'
_m.extend( ['\n\n'] )
# lineno:26
b = '<div> insidebody </div>'

_m.extend( ['\n    '] )
# lineno:39
def helloworld( x=10, y=20, a='wer', b='ehl' ) :  
  _m.pushbuf()
  # lineno:40
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:42
  a = '<div> inside function </div>'
  _m.extend( ['\n\n    '] )
  # lineno:45
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'a', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:46
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'insideroot_butglobal()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
