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
  # lineno:10
  html = '<div title="hello"> div block </div>'
  # lineno:11
  url  = 'http://pluggdapps.com/hello world'
  # lineno:12
  text = '  hello world \t'
  # lineno:13
  unitext = 'ما هي الشفرة الموحدة "يونِكود" ؟ in Arabicc'
  # lineno:15
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  # lineno:16
  _m.pushbuf()
  _m.extend( ['<head>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:17
  _m.pushbuf()
  _m.extend( ['<meta http-equiv="content-type" content="text/html; charset=UTF-8">'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:18
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:19
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'html', 'h', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:20
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'html', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:21
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'url', 'u', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:22
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'text', 't', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:23
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'unitext', '', globals(), locals()) )
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
