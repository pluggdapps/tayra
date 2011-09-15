# -*- encoding:utf-8 -*-

from   StringIO             import StringIO
from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager
import tayra
from   tayra.ttl.runtime    import StackMachine



def body(  ) :  
  world = 'jasper'
  # <form#idname formname "${}http:// google.com" > ${ "hello " + str(10) +   ' world' }
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<form'] )
  __m.pushbuf()
  __m.extend( ['#idname', '\n', 'formname', ' '] )
  __m.pushbuf()
  __m.extend( ['"', 'http', ':', '/', '/', '\n', 'google.com', '"'] )
  __m.append( __m.popbuftext() )
  __m.append( __m.popbuftext() )
  __m.extend( ['', '', ' > '] )
  __m.handletag( *__m.popbuf() )
  __m.append( str( "hello " + str(10) +   ' world' ) )
  __m.extend( ['\n'] )
  __m.upindent( up='    ' )
  # <input>   <!-- Comment  -->
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<input', '', '', '', '>'] )
  __m.handletag( *__m.popbuf() )
  __m.extend( ['\n\n', ' <!--', ' Comment\n ', '-->\n'] )
  __m.upindent( up='  ' )
  # <input>          <!-- Comment          -->    
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<input', '', '', '', '>'] )
  __m.handletag( *__m.popbuf() )
  __m.extend( ['\n', '         <!--', ' Comment\n         ', '-->\n', '   \n'] )
  __m.indent()
  __m.extend( ['</input>\n'] )
  __m.downindent( down='  ' )
  __m.indent()
  __m.extend( ['</input>\n'] )
  # <input text  =$_0(*&^%%$#@!@~}= world }$ {' title= hello ${world}}>       
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<input '] )
  __m.pushbuf()
  __m.extend( ['text', '  ', '=', '$', '_0', '(*&^%%', '$', '#', '@!@~}', '=', ' ', 'world', ' ', '}', '$'] )
  __m.append( __m.popbuftext() )
  __m.pushbuf()
  __m.extend( ["' title= hello "] )
  __m.append( str(world) )
  __m.append( __m.popbuftext() )
  __m.extend( ['', '>'] )
  __m.handletag( *__m.popbuf() )
  __m.extend( ['\n', '      \n'] )
  __m.indent()
  __m.extend( ['</input>\n'] )
  __m.downindent( down='    ' )
  __m.indent()
  __m.extend( ['</form>\n'] )
  return __m.popbuftext()

__ttlhash = 'a5bd1b7ff84a721a4384241d3754d443d3e73a9f'
__ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/tag.ttl'
