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
  _m.extend( ["<!--\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\n    Copyright (c) 2010 SKR Farms (P) LTD.\n-->\n\n"] )
  return _m.popbuftext()

# ---- Global Functions

# lineno:7
def _toc( level, heads ) :  
  _m.pushbuf()
  # lineno:8
  _m.pushbuf()
  _m.extend( ['<ul>'] )
  _m.pushbuf()
  _m.extend( ['\n    ', '\n      '] )
  # lineno:9
  for href, text, children in heads :    
    # lineno:10
    _m.pushbuf()
    _m.extend( ['<li>'] )
    _m.pushbuf()
    _m.extend( ['\n        '] )
    # lineno:11
    _m.pushbuf()
    _m.extend( ['<a .level'] )
    _m.append(_m.evalexprs( '', 'level', '', globals(), locals()) )
    _m.extend( [' "'] )
    _m.append(_m.evalexprs( '', 'href', '', globals(), locals()) )
    _m.extend( ['">'] )
    _m.pushbuf()
    # lineno:11
    _m.extend( [' '] )
    _m.append(_m.evalexprs( '', 'text', '', globals(), locals()) )
    _m.extend( ['\n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
    # lineno:12
    _m.extend( [''] )
    _m.append(_m.evalexprs( '', "children and _toc( level+1, children ) or ''", '', globals(), locals()) )
    _m.extend( ['\n\n'] )  
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()


# lineno:14
def toc( details, heads ) :  
  _m.pushbuf()
  # lineno:15
  _m.pushbuf()
  _m.extend( ['<details .toc>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:16
  _m.pushbuf()
  _m.extend( ['<summary>'] )
  _m.pushbuf()
  # lineno:16
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '', 'details', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:17
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', '_toc( 1, heads )', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()


# lineno:19
def papowered( pcount, icount ) :  
  _m.pushbuf()
  # lineno:20
  _m.pushbuf()
  _m.extend( ['<div .papowered>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:21
  _m.pushbuf()
  _m.extend( ['<div .stmt>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:22
  _m.pushbuf()
  _m.extend( ['<span .prop>'] )
  _m.pushbuf()
  # lineno:22
  _m.extend( [' On', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:23
  _m.extend( ['pluggdapps', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:24
  _m.pushbuf()
  _m.extend( ['<div .counts>'] )
  _m.pushbuf()
  # lineno:24
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '', 'pcount', '', globals(), locals()) )
  _m.extend( [' plugins via '] )
  _m.append(_m.evalexprs( '', 'icount', '', globals(), locals()) )
  _m.extend( [' interface', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
