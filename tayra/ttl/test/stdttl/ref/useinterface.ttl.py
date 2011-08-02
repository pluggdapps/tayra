
from   StringIO             import StringIO
from   zope.interface       import implements
import tayra


from  tayra.ttl.interfaces import ITestInterface
iface = _m.use( ITestInterface, _m.evalexprs(plugin, '') )

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
  # ${ iface.render() }
  _m.indent()
  _m.append( _m.evalexprs( iface.render() , '') )
  _m.extend( [u'\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = '014764abf77b6bb7626428383f84f90118f5b99b'
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/useinterface.ttl'
