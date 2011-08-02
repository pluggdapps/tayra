
_m.setencoding( u'utf-8 ' )
from   StringIO             import StringIO
from   zope.interface       import implements
import tayra


import re 

def body(  ) :  
  _m.pushbuf()
  _m.extend( [u'<!--', u"\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\n          Copyright (c) 2009 SKR Farms (P) LTD.\n"] )
  _m.extend( [u'-->', u'\n\n'] )
  html = '<div title="hello"> div block </div>'
  url  = 'http://pluggdapps.com/hello world'
  text = '  hello world \t'
  unitext = 'ما هي الشفرة الموحدة "يونِكود" ؟ in Arabicc'
  # <html>
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<html', '', '', '', u'>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  _m.upindent( up='  ' )
  # <head>
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<head', '', '', '', u'>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  _m.upindent( up='  ' )
  # <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<meta ', '', ''] )
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( [u'http-equiv', u'='] )
  _m.pushbuf()
  _m.extend( [u'"', u'content-type', u'"'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [u'content', u'='] )
  _m.pushbuf()
  _m.extend( [u'"', u'text', u'/', u'html', u';', u' ', u'charset', u'=', u'UTF-8', u'"'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuf() )
  _m.extend( [u'>'] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( [u'\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  # <body>
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<body', '', '', '', u'>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  _m.upindent( up='  ' )
  # ${ html | h }
  _m.indent()
  _m.append( _m.evalexprs( html , u' h ') )
  _m.extend( [u'\n'] )
  # ${ html }
  _m.indent()
  _m.append( _m.evalexprs( html , '') )
  _m.extend( [u'\n'] )
  # ${ url | u }
  _m.indent()
  _m.append( _m.evalexprs( url , u' u ') )
  _m.extend( [u'\n'] )
  # ${ text | t }
  _m.indent()
  _m.append( _m.evalexprs( text , u' t ') )
  _m.extend( [u'\n'] )
  # ${ unitext }
  _m.indent()
  _m.append( _m.evalexprs( unitext , '') )
  _m.extend( [u'\n'] )
  # ${ unitext | uni.latin_1 }
  _m.indent()
  _m.append( _m.evalexprs( unitext , u' uni.latin_1 ') )
  _m.extend( [u'\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = 'e4e86ae9f608c0bcfba341068e142109c211f5aa'
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/escfilters.ttl'
