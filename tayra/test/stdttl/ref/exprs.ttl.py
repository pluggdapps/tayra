# -*- encoding:utf-8 -*-

from   StringIO             import StringIO
from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager
import tayra
from   tayra.ttl.runtime    import StackMachine



def body(  ) :  
  # <div> ${ "hello {}" + str([   str(10) ]) +   ' world' }
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<div', '', '', '', '> '] )
  __m.handletag( *__m.popbuf() )
  __m.append( str( "hello {}" + str([  str(10) ]) +   ' world' ) )
  __m.extend( ['\n'] )
  __m.upindent( up='  ' )
  # <a#${'idname'}.${'cls'     'name'} "${"http://"             'google.com'}" { ${'color : ' }                              ${ "red;" } } ${"title"}="${"sun is "                                                     " shining"} brightly"/>
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<a'] )
  __m.pushbuf()
  __m.extend( ['#'] )
  __m.append( str('idname') )
  __m.extend( ['.'] )
  __m.append( str('cls'    'name') )
  __m.extend( [' '] )
  __m.pushbuf()
  __m.extend( ['"'] )
  __m.append( str("http://"            'google.com') )
  __m.extend( ['"'] )
  __m.append( __m.popbuftext() )
  __m.append( __m.popbuftext() )
  __m.pushbuf()
  __m.extend( [' '] )
  __m.append( str('color : ' ) )
  __m.extend( ['\n                             '] )
  __m.append( str( "red;" ) )
  __m.extend( [' '] )
  __m.append( __m.popbuftext() )
  __m.pushbuf()
  __m.pushbuf()
  __m.append( str("title") )
  __m.extend( ['='] )
  __m.pushbuf()
  __m.extend( ['"'] )
  __m.append( str("sun is "                                                    " shining") )
  __m.extend( [' ', 'brightly', '"'] )
  __m.append( __m.popbuftext() )
  __m.append( __m.popbuftext() )
  __m.append( __m.popbuf() )
  __m.extend( ['/>'] )
  __m.handletag( *__m.popbuf() )
  __m.extend( ['\n'] )
  __m.downindent( down='  ' )
  __m.indent()
  __m.extend( ['</div>\n'] )
  return __m.popbuftext()

__ttlhash = '4f7bcd65555681aa5e8fabea6bed87f52a1d3d3a'
__ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/exprs.ttl'
