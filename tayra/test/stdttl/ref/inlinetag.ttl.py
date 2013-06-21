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
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  # lineno:2
  _m.pushbuf()
  _m.extend( ['<head>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:3
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  # lineno:3
  _m.extend( [' ', '\n    '] )
  # lineno:4
  _m.pushbuf()
  _m.extend( ['<p>'] )
  _m.pushbuf()
  # lineno:4
  _m.extend( [' '] )
  _m.pushbuf()
  _m.extend( ['<span>'] )
  _m.pushbuf()
  # lineno:4
  _m.extend( [' '] )
  _m.pushbuf()
  _m.extend( ['<a>'] )
  _m.pushbuf()
  # lineno:4
  _m.extend( [' hello world'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.extend( ['\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:5
  _m.pushbuf()
  _m.extend( ['<div #'] )
  _m.append(_m.evalexprs( '', "'idname'", '', globals(), locals()) )
  _m.extend( [' .metanav-pa :some-name>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:6
  _m.extend( ['hello world how are you', '\n      '] )
  # lineno:7
  _m.extend( ['so this how it goes', '\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
