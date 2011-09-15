
from   StringIO             import StringIO
from   zope.interface       import implements
import tayra



def body(  ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n'] )
  # !!! escaping doctypes ;
  _m.indent()
  _m.extend( [u'!', u'!! escaping doctypes ;', u'\n'] )
  # @charset escaping directives;
  _m.indent()
  _m.extend( [u'@', u'charset escaping directives;', u'\n'] )
  # @body any directive;
  _m.indent()
  _m.extend( [u'@', u'body any directive;', u'\n\n'] )
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
  #   Escaping the indent
  _m.indent()
  _m.extend( [u' ', u' ', u'Escaping the indent', u'\n'] )
  # <div>
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<div', '', '', '', u'>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  _m.upindent( up='  ' )
  # Escaping newlines across textblocks, all of this belongs to body content.
  _m.indent()
  _m.extend( [u'Escaping newlines ', u'across textblocks, all of this belongs to body content.', u'\n'] )
  # @function escapedfunction():
  _m.indent()
  _m.extend( [u'@', u'function escapedfunction():', u'\n'] )
  _m.upindent( up='  ' )
  # @@pass
  _m.indent()
  _m.extend( [u'@', u'@', u'pass', u'\n'] )
  _m.downindent( down='  ' )
  # ${ this expresion is also escaped } and displayed as text
  _m.indent()
  _m.extend( [u'$', u'{', u' this expresion is also escaped } and displayed as text', u'\n'] )
  # @if so is this if block :
  _m.indent()
  _m.extend( [u'@', u'if so is this if block :', u'\n'] )
  # @elif block :
  _m.indent()
  _m.extend( [u'@', u'elif block :', u'\n'] )
  # @else block :
  _m.indent()
  _m.extend( [u'@', u'else block :', u'\n'] )
  # @for block :
  _m.indent()
  _m.extend( [u'@', u'for block :', u'\n'] )
  # @while block :
  _m.indent()
  _m.extend( [u'@', u'while block :', u'\n'] )
  # all of them are interpreted as text.
  _m.indent()
  _m.extend( [u'all of them are interpreted as text.', u'\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  # ${ willbecomeglobal() }
  _m.indent()
  _m.append( _m.evalexprs( willbecomeglobal() , '') )
  _m.extend( [u'\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  return _m.popbuftext()

# #---- Global Functions

# def willbecomeglobal( *args ):
def willbecomeglobal( *args ):  
  _m.pushbuf()
  # <b> Ghost
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<b', '', '', '', u'> '] )
  _m.pushbuf()
  _m.extend( [u'Ghost'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( [u'\n'] )
  # ${ nestedfunc() }
  _m.indent()
  _m.append( _m.evalexprs( nestedfunc() , '') )
  _m.extend( [u'\n'] )
  return _m.popbuftext()

# def nestedfunc():
def nestedfunc():  
  _m.pushbuf()
  # <em> Rider
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<em', '', '', '', u'> '] )
  _m.pushbuf()
  _m.extend( [u'Rider'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( [u'\n'] )
  return _m.popbuftext()
# #---- Interface functions
# #---- Footer

_ttlhash = 'bf7b8c3322e5cec7ad9390c60689abc4db1998b2'
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/escapes.ttl'
