import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
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
  l = [1,2,3]
  # lineno:3
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  # lineno:3
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '', '"hello עברית" + str([ str(10) ]) + \' world\'', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  # lineno:4
  _m.pushbuf()
  _m.extend( ['<a #'] )
  _m.append(_m.evalexprs( '', "'idname'", '', globals(), locals()) )
  _m.extend( [' .'] )
  _m.append(_m.evalexprs( '', "'cls' 'name'", '', globals(), locals()) )
  _m.extend( [' \n     "'] )
  _m.append(_m.evalexprs( '', "'http://' 'google.com'", '', globals(), locals()) )
  _m.extend( ['" \n     { '] )
  _m.append(_m.evalexprs( '', "'color : '", '', globals(), locals()) )
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '', '"red;"', '', globals(), locals()) )
  _m.extend( [' }\n     '] )
  _m.append(_m.evalexprs( '', '"title"', '', globals(), locals()) )
  _m.extend( ['="'] )
  _m.append(_m.evalexprs( '', "'sun is ' ' shining'", '', globals(), locals()) )
  _m.extend( [' brightly">'] )
  _m.pushbuf()
  _m.extend( ['\n\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:10
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'tayraexpressionevalpy', 'l.append(10)', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  # lineno:11
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'tayraexpressionpy', 'l', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  # lineno:12
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'tayraexpressionevalpy', 'l.pop(0)', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  # lineno:13
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'l', '', globals(), locals()) )
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/exprs.ttl' 