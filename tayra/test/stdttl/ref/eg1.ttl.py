
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body(  ) :  
  _m.pushbuf()
  # <html>
  _m.pushbuf()
  _m.extend( [u'html', u'<html  >', u'</html>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # <head>
  _m.pushbuf()
  _m.extend( [u'head', u'<head  >', u'</head>'] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  # <body>
  _m.pushbuf()
  _m.extend( [u'body', u'<body  >', u'</body>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # <p> hello world
  _m.pushbuf()
  _m.extend( [u'p', u'<p  > ', u'</p>'] )
  _m.pushbuf()
  _m.extend( [u'hello world'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/eg1.ttl'
