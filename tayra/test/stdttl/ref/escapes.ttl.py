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
  _m.extend( ['<!DOCTYPE html>\n\n'] )
  # lineno:3
  _m.extend( ['@body any directive', '\n\n'] )
  # lineno:5
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  # lineno:6
  _m.pushbuf()
  _m.extend( ['<head>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:7
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:8
  _m.extend( ['  Escaping the indent', '\n    '] )
  # lineno:9
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:10
  _m.extend( ['Escaping newlines       across textblocks, all of this belongs to body content.', '\n      '] )
  # lineno:16
  _m.extend( ['@def escapedfunction():', '\n        '] )
  # lineno:17
  _m.extend( ['@@pass', '\n      '] )
  # lineno:18
  _m.extend( ['\\${ this expresion is also escaped } and displayed as text', '\n      '] )
  # lineno:19
  _m.extend( ['@if so is this if block :', '\n      '] )
  # lineno:20
  _m.extend( ['@elif block :', '\n      '] )
  # lineno:21
  _m.extend( ['@else block :', '\n      '] )
  # lineno:22
  _m.extend( ['@for block :', '\n      '] )
  # lineno:23
  _m.extend( ['@while block :', '\n      '] )
  # lineno:24
  _m.extend( ['all of them are interpreted as text.', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:25
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'willbecomeglobal()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions

# lineno:11
def willbecomeglobal( *args ):  
  _m.pushbuf()
  # lineno:12
  _m.pushbuf()
  _m.extend( ['<b>'] )
  _m.pushbuf()
  # lineno:12
  _m.extend( [' Ghost', '\n        '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  
  # lineno:13
  def nestedfunc():    
    _m.pushbuf()
    # lineno:14
    _m.pushbuf()
    _m.extend( ['<em>'] )
    _m.pushbuf()
    # lineno:14
    _m.extend( [' Rider', '\n        '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    return _m.popbuftext()  
  
  # lineno:15
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'nestedfunc()', '', globals(), locals()) )
  _m.extend( ['\n      '] )
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
