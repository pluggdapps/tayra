
from   StringIO             import StringIO
from   zope.interface       import implements
import tayra



def body(  ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n'] )
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
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( [u'\n'] )
  # <body>
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<body', '', '', '', u'>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  _m.upindent( up='  ' )
  # <div>
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<div', '', '', '', u'>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  _m.upindent( up='  ' )
  # 什麽是Unicode(統一碼/標準萬國碼)
  _m.indent()
  _m.extend( [u'\u4ec0\u9ebd\u662fUnicode(\u7d71\u4e00\u78bc/\u6a19\u6e96\u842c\u570b\u78bc)', u'\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  return _m.popbuftext()

# #---- Global Functions
# #---- Interface functions
# #---- Footer

_ttlhash = '0d62f7e8f79d246ba3666f1ffe21a5b7f757a8a0'
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/unicode.ttl'
