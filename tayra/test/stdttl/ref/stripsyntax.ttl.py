# -*- coding: utf-8 -*-

from   StringIO             import StringIO
from   zope.interface       import implements
import tayra

_m.setencoding( 'utf-8' )


def body(  ) :  
  _m.extend( ['<!--', "\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\nCopyright (c) 2009 SKR Farms (P) LTD.\n"] )
  _m.extend( ['-->\n\n'] )
  # <pre>
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<pre', '', '', '', '>'] )
  _m.pushbuf()
  _m.extend( [''] )
  # int foo( int a, int b  ){
  _m.indent()
  _m.extend( ['int foo( int a, int b  )', '{', '\n'] )
  _m.upindent( up='  ' )
  # printf( 'helloworld' )
  _m.indent()
  _m.extend( ["printf( 'helloworld' )", '\n'] )
  _m.downindent( down='  ' )
  # }
  _m.indent()
  _m.extend( ['}', ''] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='\n' )
  # ${helloword()}
  _m.indent()
  _m.append( _m.evalexprs(helloword()) )
  _m.extend( ['\n'] )
  return _m.popbuftext()
# #---- Global Functions

# def helloword( x=10, y=20, a='wer', b='ehl' ) :
def helloword( x=10, y=20, a='wer', b='ehl' ) :  
  _m.pushbuf()
  # <html>
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<html', '', '', '', '>'] )
  _m.pushbuf()
  _m.extend( ['\n'] )
  _m.upindent( up='  ' )
  b = 'hello'   
  # ${x+y}
  _m.indent()
  _m.append( _m.evalexprs(x+y) )
  _m.extend( ['\n'] )
  # <head#headid.cls1.${a.strip()} "title" {color:red} lang="en" data="hello">
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<head'] )
  _m.pushbuf()
  _m.extend( ['#headid.cls1.'] )
  _m.append( _m.evalexprs(a.strip()) )
  _m.extend( [' '] )
  _m.pushbuf()
  _m.extend( ['"', 'title', '"'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( ['color:red'] )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['lang', '='] )
  _m.pushbuf()
  _m.extend( ['"', 'en', '"'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( ['data', '='] )
  _m.pushbuf()
  _m.extend( ['"', 'hello', '"'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuf() )
  _m.extend( ['>'] )
  _m.pushbuf()
  _m.extend( ['\n'] )
  _m.upindent( up='  ' )
  # <title#titleid .cls1 "title string"> hello ${a} @ ! # "helo" 'world "ok
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<title'] )
  _m.pushbuf()
  _m.extend( ['#titleid', ' ', '.cls1', ' '] )
  _m.pushbuf()
  _m.extend( ['"', 'title', ' ', 'string', '"'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuftext() )
  _m.extend( ['', '', '> '] )
  _m.pushbuf()
  _m.extend( ['hello '] )
  _m.append( _m.evalexprs(a) )
  _m.extend( [' @ ! # "helo" \'world "ok'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( ['\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  # <body>
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<body', '', '', '', '>'] )
  _m.pushbuf()
  _m.extend( ['\n'] )
  _m.upindent( up='  ' )
  # <h1 { color : red; border : 1px solid gray; }/> I am the space station ${ "These "} seven cameras
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<h1 ', ''] )
  _m.pushbuf()
  _m.extend( [' color : red; border : 1px solid gray; '] )
  _m.append( _m.popbuftext() )
  _m.extend( ['', '/> '] )
  _m.pushbuf()
  _m.extend( ['I am the space station '] )
  _m.append( _m.evalexprs( "These ") )
  _m.extend( [' seven cameras'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( ['\n'] )
  # have a zoom range 
  _m.indent()
  _m.extend( ['have a zoom range ', '\n'] )
  # <p first second>of any 12x or more,  ${20}
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<p '] )
  _m.pushbuf()
  _m.extend( ['first', ' ', 'second'] )
  _m.append( _m.popbuftext() )
  _m.extend( ['', '', '>'] )
  _m.pushbuf()
  _m.extend( ['of any 12x or more,  '] )
  _m.append( _m.evalexprs(20) )
  _m.extend( [''] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( ['\n'] )
  # and some of the wide-angle view 
  _m.indent()
  _m.extend( ['and some of the wide-angle view ', '\n'] )
  # <div>of good. They also have a
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<div', '', '', '', '>'] )
  _m.pushbuf()
  _m.extend( ['of good. They also have a', '\n'] )
  # lot of image stabilization (either optical or mechanical), which is 
  _m.indent()
  _m.extend( ['lot of image stabilization (either optical or mechanical), which is ', '\n'] )
  # important for people who are with a powerful zoom lens. Some other
  _m.indent()
  _m.extend( ['important for people who are with a powerful zoom lens. Some other', ''] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='\n' )
  # important features thatThese cameras contain electronic viewfinder,
  _m.indent()
  _m.extend( ['important features thatThese cameras contain electronic viewfinder,', '\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  # full control while shooting. In general, these cameras are all seem 
  _m.indent()
  _m.extend( ['full control while shooting. In general, these cameras are all seem ', '\n'] )
  _m.upindent( up='  ' )
  # very similar.     
  _m.indent()
  _m.extend( ['very similar.', '\n'] )
  # <p#${b}> Sign my guestbook
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<p'] )
  _m.pushbuf()
  _m.extend( ['#'] )
  _m.append( _m.evalexprs(b) )
  _m.append( _m.popbuftext() )
  _m.extend( ['', '', '> '] )
  _m.pushbuf()
  _m.extend( ['Sign my guestbook'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( ['\n\n'] )
  _m.downindent( down='  ' )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  return _m.popbuftext()
# #---- Interface functions
# #---- Footer

_ttlhash = 'c985297273aedd93e3b18ad56d1cb0b9bbc85636'
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/stripsyntax.ttl'
