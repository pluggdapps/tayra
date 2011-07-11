# -*- encoding:utf-8 -*-

from   StringIO             import StringIO
from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager
import tayra
from   tayra.ttl.runtime    import StackMachine



__m.extend( ['\n'] )
def body( a=10, x=10, y=10, z=10, s='hello ' ) :  
  # if a == 'pass' :
  if a == 'pass' :    
    __m.extend( ['   \n'] )
    pass
    __m.extend( ['    \n'] )  
  # elif a == ':' : 
  elif a == ':' :     
    pass  
  # elif a == 1 :
  elif a == 1 :    
    # Google will join its biggest mobile rival, Apple, on the space trip as well.
    __m.indent()
    __m.extend( ['Google will join its biggest mobile rival, Apple, on the space trip as well.', '\n'] )
    # Apple's iPhone 4 will join a crew running an app, called "SpaceLab for iOS."
    __m.indent()
    __m.extend( ['Apple\'s iPhone 4 will join a crew running an app, called "SpaceLab for iOS."', '\n'] )  
  # elif a== 2 :
  elif a== 2 :    
    # The program, designed by Odyssey Space Research, will allow crew members to
    __m.indent()
    __m.extend( ['The program, designed by Odyssey Space Research, will allow crew members to', '\n'] )
    # conduct several experiments with the phones' cameras, gyroscopes and other
    __m.indent()
    __m.extend( ["conduct several experiments with the phones' cameras, gyroscopes and other", '\n'] )  
  # elif a == 3 : 
  elif a == 3 :     
    # <html#std1.testcase.sample { color: red; font-size : ${z*2}px } title="hello world">
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<html'] )
    __m.pushbuf()
    __m.extend( ['#std1.testcase.sample'] )
    __m.append( __m.popbuftext() )
    __m.pushbuf()
    __m.extend( [' color: red; font-size : '] )
    __m.append( str(z*2) )
    __m.extend( ['px '] )
    __m.append( __m.popbuftext() )
    __m.pushbuf()
    __m.pushbuf()
    __m.extend( ['title', '='] )
    __m.pushbuf()
    __m.extend( ['"', 'hello', ' ', 'world', '"'] )
    __m.append( __m.popbuftext() )
    __m.append( __m.popbuftext() )
    __m.append( __m.popbuf() )
    __m.extend( ['>'] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['\n'] )
    __m.upindent( up='  ' )
    # <head/>
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<head', '', '', '', '/>'] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['\n'] )
    # <body>
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<body', '', '', '', '>'] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['\n'] )
    __m.upindent( up='  ' )
    # <abbr "World Health Organization"> WHO   
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<abbr '] )
    __m.pushbuf()
    __m.pushbuf()
    __m.extend( ['"', 'World', ' ', 'Health', ' ', 'Organization', '"'] )
    __m.append( __m.popbuftext() )
    __m.append( __m.popbuftext() )
    __m.extend( ['', '', '> '] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['WHO', '\n', '  \n'] )
    __m.indent()
    __m.extend( ['</abbr>\n'] )
    # <button#id_ reset disabled makefriend "button value"/>
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<button'] )
    __m.pushbuf()
    __m.extend( ['#id_', ' ', 'reset', ' ', 'disabled', ' ', 'makefriend', ' '] )
    __m.pushbuf()
    __m.extend( ['"', 'button', ' ', 'value', '"'] )
    __m.append( __m.popbuftext() )
    __m.append( __m.popbuftext() )
    __m.extend( ['', '', '/>'] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['\n\n'] )
    __m.downindent( down='  ' )
    __m.indent()
    __m.extend( ['</body>\n'] )
    __m.downindent( down='  ' )
    __m.indent()
    __m.extend( ['</html>\n'] )  
  # elif a == 4 :
  elif a == 4 :    
    __m.extend( ['   \n'] )
    # <div> ${ "hello {}" + str([     str(10) ]) +     ' world' }
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<div', '', '', '', '> '] )
    __m.handletag( *__m.popbuf() )
    __m.append( str( "hello {}" + str([    str(10) ]) +     ' world' ) )
    __m.extend( ['\n'] )
    __m.upindent( up='  ' )
    # <a#${'idname       '}.${'cls'       'name'} "${"http://"               'google.com'}" { ${'color : ' }                                ${ "red;" } } ${"title"}="${"sun is "                                                     " shining"} brightly">
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<a'] )
    __m.pushbuf()
    __m.extend( ['#'] )
    __m.append( str('idname       ') )
    __m.extend( ['.'] )
    __m.append( str('cls'      'name') )
    __m.extend( [' '] )
    __m.pushbuf()
    __m.extend( ['"'] )
    __m.append( str("http://"              'google.com') )
    __m.extend( ['"'] )
    __m.append( __m.popbuftext() )
    __m.append( __m.popbuftext() )
    __m.pushbuf()
    __m.extend( [' '] )
    __m.append( str('color : ' ) )
    __m.extend( ['\n                               '] )
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
    __m.extend( ['>'] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['\n'] )
    __m.indent()
    __m.extend( ['</a>\n'] )
    __m.downindent( down='  ' )
    __m.indent()
    __m.extend( ['</div>\n'] )  
  # elif a == 5 : 
  elif a == 5 :     
    # <div {} >
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<div ', ''] )
    __m.pushbuf()
    __m.append( __m.popbuftext() )
    __m.extend( ['', '>'] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['\n\n'] )
    __m.upindent( up='  ' )
    # <a#${'idname'}.${'cls'}           "http://pluggdapps.com"       { ${'color : ' } ${ "red;"  } ' style with line         break' } /> hello {world} /> 
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<a'] )
    __m.pushbuf()
    __m.extend( ['#'] )
    __m.append( str('idname') )
    __m.extend( ['.'] )
    __m.append( str('cls') )
    __m.extend( ['\n', '   ', '\n', '      '] )
    __m.pushbuf()
    __m.extend( ['"', 'http', ':', '/', '/', 'pluggdapps.com', '"'] )
    __m.append( __m.popbuftext() )
    __m.append( __m.popbuftext() )
    __m.pushbuf()
    __m.extend( [' '] )
    __m.append( str('color : ' ) )
    __m.extend( [' '] )
    __m.append( str( "red;"  ) )
    __m.extend( [" ' style with line\n        break' "] )
    __m.append( __m.popbuftext() )
    __m.extend( ['', '/> '] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['hello {world} /> ', '\n'] )
    __m.downindent( down='  ' )
    __m.indent()
    __m.extend( ['</div>\n'] )  
  # elif a == 6 :
  elif a == 6 :    
    # <html>
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<html', '', '', '', '>'] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['\n'] )
    __m.upindent( up='  ' )
    b = 'hello'   
    # ${x+y}
    __m.indent()
    __m.append( str(x+y) )
    __m.extend( ['\n'] )
    # <head#headid.cls1.${s.strip(     )} "title" {color:red} lang="en"      data="hello">
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<head'] )
    __m.pushbuf()
    __m.extend( ['#headid.cls1.'] )
    __m.append( str(s.strip(    )) )
    __m.extend( [' '] )
    __m.pushbuf()
    __m.extend( ['"', 'title', '"'] )
    __m.append( __m.popbuftext() )
    __m.append( __m.popbuftext() )
    __m.pushbuf()
    __m.extend( ['color:red'] )
    __m.append( __m.popbuftext() )
    __m.pushbuf()
    __m.pushbuf()
    __m.extend( ['lang', '='] )
    __m.pushbuf()
    __m.extend( ['"', 'en', '"'] )
    __m.append( __m.popbuftext() )
    __m.append( __m.popbuftext() )
    __m.pushbuf()
    __m.extend( ['data', '='] )
    __m.pushbuf()
    __m.extend( ['"', 'hello', '"'] )
    __m.append( __m.popbuftext() )
    __m.append( __m.popbuftext() )
    __m.append( __m.popbuf() )
    __m.extend( ['>'] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['\n'] )
    __m.upindent( up='  ' )
    # <title#titleid .cls1 "title          string"> hello ${s} @ ! # "helo" 'world "ok
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<title'] )
    __m.pushbuf()
    __m.extend( ['#titleid', ' ', '.cls1', ' '] )
    __m.pushbuf()
    __m.extend( ['"', 'title', ' ', '\n', '        ', 'string', '"'] )
    __m.append( __m.popbuftext() )
    __m.append( __m.popbuftext() )
    __m.extend( ['', '', '> '] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['hello ${s} @ ! # "helo" \'world "ok', '\n'] )
    __m.indent()
    __m.extend( ['</title>\n'] )
    __m.downindent( down='  ' )
    __m.indent()
    __m.extend( ['</head>\n'] )
    # <body>
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<body', '', '', '', '>'] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['\n'] )
    __m.upindent( up='  ' )
    # <h1 { color : red;   border : 1px solid gray;       }/> I am the space station ${ "These "} seven cameras       <!-- comment1      comment -->
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<h1 ', ''] )
    __m.pushbuf()
    __m.extend( [' color : red;\n  border : 1px solid gray;\n      '] )
    __m.append( __m.popbuftext() )
    __m.extend( ['', '/> '] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['I am the space station ${ "These "} seven cameras', '\n', '      <!--', ' comment1\n     comment ', '-->\n'] )
    # have a zoom range 
    __m.indent()
    __m.extend( ['have a zoom range ', '\n'] )
    # <p first       second> of any 12x or more,       <!-- comment1          comment -->
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<p '] )
    __m.pushbuf()
    __m.extend( ['first', '\n', '      ', 'second'] )
    __m.append( __m.popbuftext() )
    __m.extend( ['', '', '> '] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['of any 12x or more,', '\n', '      <!--', ' comment1\n         comment ', '-->\n'] )
    __m.indent()
    __m.extend( ['</p>\n'] )
    # and some of the wide-angle view 
    __m.indent()
    __m.extend( ['and some of the wide-angle view ', '\n'] )
    # <div> of good. They also have a
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<div', '', '', '', '> '] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['of good. They also have a', '\n'] )
    __m.upindent( up='  ' )
    # lot of image stabilization (either optical or mechanical), which is 
    __m.indent()
    __m.extend( ['lot of image stabilization (either optical or mechanical), which is ', '\n'] )
    # important for people who are with a powerful zoom lens. Some other
    __m.indent()
    __m.extend( ['important for people who are with a powerful zoom lens. Some other', '\n'] )
    __m.downindent( down='  ' )
    __m.indent()
    __m.extend( ['</div>\n'] )
    # important features thatThese cameras contain electronic viewfinder,         <!-- comment1 comment -->   
    __m.indent()
    __m.extend( ['important features thatThese cameras contain electronic viewfinder,', '\n', '        <!--', ' comment1 comment ', '-->\n'] )
    __m.extend( ['  \n'] )
    __m.downindent( down='  ' )
    __m.indent()
    __m.extend( ['</body>\n'] )
    # full control while shooting. In general, these cameras are all seem 
    __m.indent()
    __m.extend( ['full control while shooting. In general, these cameras are all seem ', '\n'] )
    __m.upindent( up='  ' )
    # very similar.     
    __m.indent()
    __m.extend( ['very similar.', '\n', '    \n'] )
    # <p#${b}> Sign my guestbook
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<p'] )
    __m.pushbuf()
    __m.extend( ['#'] )
    __m.append( str(b) )
    __m.append( __m.popbuftext() )
    __m.extend( ['', '', '> '] )
    __m.handletag( *__m.popbuf() )
    __m.extend( ['Sign my guestbook', '\n'] )
    __m.indent()
    __m.extend( ['</p>\n'] )
    __m.downindent( down='  ' )
    __m.downindent( down='  ' )
    __m.indent()
    __m.extend( ['</html>\n'] )  
  # elif a == 7 :
  elif a == 7 :    
    world = 10
    __m.extend( ['  \n'] )
    # <form#idname   formname "${}http://   google.com" > ${ "hello " + str(10) +     ' world' }
    __m.indent()
    __m.pushbuf()
    __m.extend( ['<form'] )
    __m.pushbuf()
    __m.extend( ['#idname', '\n', '  ', 'formname', ' '] )
    __m.pushbuf()
    __m.extend( ['"', 'http', ':', '/', '/', '\n', '  ', 'google.com', '"'] )
    __m.append( __m.popbuftext() )
    __m.append( __m.popbuftext() )
    __m.extend( ['', '', ' > '] )
    __m.handletag( *__m.popbuf() )
    __m.append( str( "hello " + str(10) +     ' world' ) )
    __m.extend( ['\n'] )
    __m.upindent( up='    ' )
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
    __m.extend( ['\n'] )
    __m.indent()
    __m.extend( ['</input>\n'] )
    __m.downindent( down='    ' )
    __m.indent()
    __m.extend( ['</form>\n'] )  
  # else :
  else :    
    # sensors. Each device will include step-by-step directions for the astronauts,
    __m.indent()
    __m.extend( ['sensors. Each device will include step-by-step directions for the astronauts,', '\n'] )
    # eliminating the need for printed instructions.
    __m.indent()
    __m.extend( ['eliminating the need for printed instructions.', '\n'] )  
  return __m.popbuftext()

__ttlhash = '00c7ea37a3e50d7736b83fad6cb5086f2410cd23'
__ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/ifblock.ttl'
