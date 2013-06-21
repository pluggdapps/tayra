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
  world = 'jasper'
  # lineno:3
  _m.pushbuf()
  _m.extend( ['<form #idname\nformname "', 'http://\ngoogle.com" >'] )
  _m.pushbuf()
  # lineno:5
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '', '"hello " + str(10) + \' world\'', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:6
  _m.pushbuf()
  _m.extend( ['<input>'] )
  _m.pushbuf()
  _m.extend( ['\n\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.extend( ['<!--', ' Comment\n    ', '-->', '\n    '] )
  # lineno:10
  _m.pushbuf()
  _m.extend( ['<input>'] )
  _m.pushbuf()
  _m.extend( ['\n       ', '<!--', ' Comment\n       ', '-->', '\n   \n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:14
  _m.pushbuf()
  _m.extend( ["<input text  =$_0(*&^%%$#@!@~}= world }$ {' title= hello "] )
  _m.append(_m.evalexprs( '', 'world', '', globals(), locals()) )
  _m.extend( ['}>'] )
  _m.pushbuf()
  _m.extend( ['\n      \n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
