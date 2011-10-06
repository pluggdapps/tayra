
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body(  ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n'] )
  # <html> <!-- Trying to inline a comment --> fair enough
  _m.pushbuf()
  _m.extend( [u'html', u'<html  > ', u'</html>'] )
  _m.pushbuf()
  _m.extend( [u'<!--', u' Trying to inline a comment ', u'--> ', u'fair enough', u'\n'] )
  # <head> <!-- An inline comment spanning multiple     lines -->
  _m.pushbuf()
  _m.extend( [u'head', u'<head  > ', u'</head>'] )
  _m.pushbuf()
  _m.extend( [u'<!--', u' An inline comment spanning multiple\n    lines ', u'-->'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  # <body>
  _m.pushbuf()
  _m.extend( [u'body', u'<body  >', u'</body>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # try inline <!-- comments inside text-lines -->
  _m.extend( [u'try inline ', u'<!--', u' comments inside text-lines ', u'-->', u'\n'] )
  # again <!-- spanning across multiple     lines       with indentation --> and finally finish it with text.
  _m.extend( [u'again ', u'<!--', u' spanning across multiple\n    lines\n      with indentation ', u'--> ', u'and finally finish it with text.', u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/comments.ttl'
