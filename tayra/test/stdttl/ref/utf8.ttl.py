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
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  # lineno:4
  _m.pushbuf()
  _m.extend( ['<head>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:5
  _m.pushbuf()
  _m.extend( ['<meta http-equiv="content-type" content="text/html; charset=UTF-8">'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:6
  _m.pushbuf()
  _m.extend( ['<body title="ユニコードとは何か？in Japanese">'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:7
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:8
  _m.extend( ['Translations', '\n      '] )
  # lineno:9
  _m.pushbuf()
  _m.extend( ['<b>'] )
  _m.pushbuf()
  # lineno:9
  _m.extend( [' 什麽是Unicode', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:10
  _m.pushbuf()
  _m.extend( ['<a "http://統一碼/標準萬國碼">'] )
  _m.pushbuf()
  # lineno:10
  _m.extend( [' in Chinese', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:11
  _m.extend( ["Qu'est ce qu'Unicode? in French", '\n      '] )
  # lineno:12
  _m.extend( ['Was ist Unicode? in German', '\n      '] )
  # lineno:13
  _m.extend( ['Τι είναι το Unicode; in Greek (Monotonic)', '\n      '] )
  # lineno:14
  _m.extend( ["Cos'è Unicode? in Italian", '\n      '] )
  # lineno:15
  _m.extend( ['ユニコードとは何か？in Japanese', '\n      '] )
  # lineno:16
  _m.extend( ['유니코드에 대해? in Korean', '\n      '] )
  # lineno:17
  _m.extend( ['O que é Unicode? in Portuguese', '\n      '] )
  # lineno:18
  _m.extend( ['Что такое Unicode? in Russian', '\n      '] )
  # lineno:19
  _m.extend( ['¿Qué es Unicode? in Spanish', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
