import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra                import BaseTTLPlugin


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( [' <!-- Trying to inline a comment --> fair enough', '\n  '] )
  _m.pushbuf()
  _m.extend( ['<head>'] )
  _m.pushbuf()
  _m.extend( [' <!-- An inline comment spanning multiple', '\n    ', 'lines -->', '\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( ['\n    ', 'try inline <!-- comments inside text-lines -->', '\n    ', 'again <!-- spanning across multiple', '\n    ', 'lines', '\n      ', 'with indentation --> and finally finish it with text.', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/comments.ttl' 