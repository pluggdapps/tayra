
_m.setencoding( u'utf-8 ' )
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin


import re 

def body(  ) :  
  _m.pushbuf()
  _m.extend( [u'<!--', u"\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\n          Copyright (c) 2009 SKR Farms (P) LTD.\n", u'-->', u'\n\n'] )
  html = '<div title="hello"> div block </div>'
  url  = 'http://pluggdapps.com/hello world'
  text = '  hello world \t'
  unitext = 'ما هي الشفرة الموحدة "يونِكود" ؟ in Arabicc'
  # <html>
  _m.pushbuf()
  _m.extend( [u'html', u'<html  >', u'</html>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # <head>
  _m.pushbuf()
  _m.extend( [u'head', u'<head  >', u'</head>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  _m.pushbuf()
  _m.extend( [u'meta', u'<meta   http-equiv="content-type" content="text/html; charset=UTF-8">', u'</meta>'] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  # <body>
  _m.pushbuf()
  _m.extend( [u'body', u'<body  >', u'</body>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # ${ html | h }
  _m.append( _m.evalexprs(html, u' h ') )
  _m.extend( [u'\n'] )
  # ${ html }
  _m.append( _m.evalexprs(html, '') )
  _m.extend( [u'\n'] )
  # ${ url | u }
  _m.append( _m.evalexprs(url, u' u ') )
  _m.extend( [u'\n'] )
  # ${ text | t }
  _m.append( _m.evalexprs(text, u' t ') )
  _m.extend( [u'\n'] )
  # ${ unitext }
  _m.append( _m.evalexprs(unitext, '') )
  _m.extend( [u'\n'] )
  # ${ unitext | uni.latin_1 }
  _m.append( _m.evalexprs(unitext, u' uni.latin_1 ') )
  _m.extend( [u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/escfilters.ttl'
