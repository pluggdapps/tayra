
from   StringIO             import StringIO
from   zope.interface       import implements
import tayra



def body(  ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n'] )
  # <html> <!-- Trying to inline a comment --> fair enough
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<html', '', '', '', u'> '] )
  _m.pushbuf()
  _m.extend( [u'<!--', u' Trying to inline a comment ', u'--> ', u'fair enough', u'\n'] )
  _m.upindent( up='  ' )
  # <head> <!-- An inline comment spanning multiple     lines -->
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<head', '', '', '', u'> '] )
  _m.pushbuf()
  _m.extend( [u'<!--', u' An inline comment spanning multiple\n    lines ', u'-->'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( [u'\n'] )
  # <body>
  _m.indent()
  _m.pushbuf()
  _m.extend( [u'<body', '', '', '', u'>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  _m.upindent( up='  ' )
  # try inline <!-- comments inside text-lines -->
  _m.indent()
  _m.extend( [u'try inline ', u'<!--', u' comments inside text-lines ', u'-->', u'\n'] )
  # again <!-- spanning across multiple     lines       with indentation --> and finally finish it with text.
  _m.indent()
  _m.extend( [u'again ', u'<!--', u' spanning across multiple\n    lines\n      with indentation ', u'--> ', u'and finally finish it with text.'] )
  _m.extend( [u'\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  return _m.popbuftext()

# #---- Global Functions
# #---- Interface functions
# #---- Footer

_ttlhash = 'bf9be7365944916cf3e9607fb9d30d152385882d'
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/comments.ttl'
