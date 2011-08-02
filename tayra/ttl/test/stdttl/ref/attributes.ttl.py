
from   StringIO             import StringIO
from   zope.interface       import implements
import tayra



def body(  ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n'] )
  _m.extend( [u'<!--', u"\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\nCopyright (c) 2009 SKR Farms (P) LTD.\n"] )
  _m.extend( [u'-->', u'\n\n'] )
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
  # Let us experiment with different ways of using attributes.
  _m.indent()
  _m.extend( [u'Let us experiment with different ways of using attributes.', u'\n'] )
  # Note that attributes always follow `specifiers` and `styles`
  _m.indent()
  _m.extend( [u'Note that attributes always follow `specifiers` and `styles`', u'\n'] )
  # <div title="hello world"> attribute value is provided as a string.
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<div ', '', ''] )
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( [u'title', u'='] )
  _m.pushbuf()
  _m.extend( [u'"', u'hello', u' ', u'world', u'"'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuf() )
  _m.extend( [u'> '] )
  _m.pushbuf()
  _m.extend( [u'attribute value is provided as a string.'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( [u'\n'] )
  # <div disabled=disabled> attribute value is provided as an atom.
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<div ', '', ''] )
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( [u'disabled', u'=', u'disabled'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuf() )
  _m.extend( [u'> '] )
  _m.pushbuf()
  _m.extend( [u'attribute value is provided as an atom.'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( [u'\n'] )
  # <div#specid.floatr.fgblue dummy spec disabled=disabled>
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<div'] )
  _m.pushbuf()
  _m.extend( [u'#specid.floatr.fgblue', u' ', u'dummy', u' ', u'spec'] )
  _m.append( _m.popbuftext() )
  _m.extend( [''] )
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( [u'disabled', u'=', u'disabled'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuf() )
  _m.extend( [u'>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  _m.upindent( up='  ' )
  # attribute value is provided as an atom, along with specifiers
  _m.indent()
  _m.extend( [u'attribute value is provided as an atom, along with specifiers', u'\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  # <div#specid.floatr.fgblue dummy spec {background-color : crimson;}     disabled=disabled>
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<div'] )
  _m.pushbuf()
  _m.extend( [u'#specid.floatr.fgblue', u' ', u'dummy', u' ', u'spec'] )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [u'background-color : crimson;'] )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( [u'disabled', u'=', u'disabled'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuf() )
  _m.extend( [u'>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  _m.upindent( up='  ' )
  # attribute value is provided as an atom, along with specifiers and styling
  _m.indent()
  _m.extend( [u'attribute value is provided as an atom, along with specifiers and styling', u'\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = '0be5992ae4e4c148746d808f2678429660a6c844'
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/attributes.ttl'
