# -*- encoding:utf-8 -*-

from   StringIO             import StringIO
from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager
import tayra
from   tayra.ttl.runtime    import StackMachine



def body(  ) :  
  # <div {} >
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<div ', ''] )
  __m.pushbuf()
  __m.append( __m.popbuftext() )
  __m.extend( ['', '>'] )
  __m.handletag( *__m.popbuf() )
  __m.extend( ['\n'] )
  __m.upindent( up='  ' )
  # <a#${'idname'}.${'cls'}     "http://pluggdapps.com"     { ${'color : ' } ${ "red;"  } ' style with line       break' } /> hello {world} /> 
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<a'] )
  __m.pushbuf()
  __m.extend( ['#'] )
  __m.append( str('idname') )
  __m.extend( ['.'] )
  __m.append( str('cls') )
  __m.extend( ['\n', '    '] )
  __m.pushbuf()
  __m.extend( ['"', 'http', ':', '/', '/', 'pluggdapps.com', '"'] )
  __m.append( __m.popbuftext() )
  __m.append( __m.popbuftext() )
  __m.pushbuf()
  __m.extend( [' '] )
  __m.append( str('color : ' ) )
  __m.extend( [' '] )
  __m.append( str( "red;"  ) )
  __m.extend( [" ' style with line\n      break' "] )
  __m.append( __m.popbuftext() )
  __m.extend( ['', '/> '] )
  __m.handletag( *__m.popbuf() )
  __m.extend( ['hello {world} /> ', '\n'] )
  __m.downindent( down='  ' )
  __m.indent()
  __m.extend( ['</div>\n'] )
  return __m.popbuftext()

__ttlhash = '32f009f5dcc730eeae0cff71543d624ee663ca4b'
__ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/style.ttl'
