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
  _m.extend( ["<!--\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\nCopyright (c) 2011 R Pratap Chakravarthy\n-->\n\n"] )
  _m.extend( ['<!DOCTYPE html>\n    \n'] )
  # lineno:9
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  # lineno:10
  _m.pushbuf()
  _m.extend( ['<head>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:11
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:12
  _m.extend( ['Let us experiment with different ways of using attributes.', '\n    '] )
  # lineno:13
  _m.extend( ['Note that attributes always follow `specifiers` and `styles`', '\n    '] )
  # lineno:14
  _m.pushbuf()
  _m.extend( ['<div title="hello world">'] )
  _m.pushbuf()
  # lineno:14
  _m.extend( [' attribute value is provided as a string.', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:15
  _m.pushbuf()
  _m.extend( ['<div disabled="disabled">'] )
  _m.pushbuf()
  # lineno:15
  _m.extend( [' attribute value is provided as an atom.', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:16
  _m.pushbuf()
  _m.extend( ['<div #specid .floatr.fgblue dummy spec disabled>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:17
  _m.extend( ['attribute value is provided as an atom, along with specifiers', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:18
  _m.pushbuf()
  _m.extend( ['<a>'] )
  _m.pushbuf()
  # lineno:18
  _m.extend( [' fine clause', '\n      \n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:20
  _m.pushbuf()
  _m.extend( ['<div #spcid .floatr.fgblue dummy {background-color : crimson;}\n         disabled>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:22
  _m.extend( ['attribute value is provided as an atom, along with specifiers and styling', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:23
  _m.pushbuf()
  _m.extend( ['<a>'] )
  _m.pushbuf()
  # lineno:23
  _m.extend( [' hello world', '\n      \n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
