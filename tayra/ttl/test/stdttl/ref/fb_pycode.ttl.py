
# -*- coding: utf-8  -*-
_m.setencoding( 'utf-8 ' )
a = 'empty'
def insideroot_butglobal():
  return '<div> insideroot_butglobal </div>'
a = 'empty'
def insidediv_butglobal():
  return '<div> insidediv_butglobal </div>'

from   StringIO             import StringIO
from   zope.interface       import implements
import tayra


import re 

_m.extend( ['\n'] )
def body(  ) :  
  _m.extend( ['<!--', "\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\n          Copyright (c) 2009 SKR Farms (P) LTD.\n"] )
  _m.extend( ['-->\n\n'] )
  b = '<div> insideroot_insidebody </div>'
  # ${ a } ${ insideroot_butglobal() }
  _m.indent()
  _m.append( _m.evalexprs( a , '') )
  _m.extend( [' '] )
  _m.append( _m.evalexprs( insideroot_butglobal() , '') )
  _m.extend( ['\n'] )
  # ${ b }
  _m.indent()
  _m.append( _m.evalexprs( b , '') )
  _m.extend( ['\n\n'] )
  # <html>
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<html', '', '', '', '>'] )
  _m.pushbuf()
  _m.extend( ['\n'] )
  _m.upindent( up='  ' )
  b = 'hello'   
  # <head#headid.cls1.${a.strip()} "title" {color:red} lang="en" data="hello">
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<head'] )
  _m.pushbuf()
  _m.extend( ['#headid.cls1.'] )
  _m.append( _m.evalexprs(a.strip(), '') )
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
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( ['\n'] )
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
  _m.append( _m.evalexprs( "These ", '') )
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
  _m.append( _m.evalexprs(20, '') )
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
  # ${ helloworld() }
  _m.indent()
  _m.append( _m.evalexprs( helloworld() , '') )
  _m.extend( ['\n'] )
  # <p#${b}> Sign my guestbook
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<p'] )
  _m.pushbuf()
  _m.extend( ['#'] )
  _m.append( _m.evalexprs(b, '') )
  _m.append( _m.popbuftext() )
  _m.extend( ['', '', '> '] )
  _m.pushbuf()
  _m.extend( ['Sign my guestbook'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, newline='' )
  _m.extend( ['\n'] )
  # ${ insideroot_butglobal() }
  _m.indent()
  _m.append( _m.evalexprs( insideroot_butglobal() , '') )
  _m.extend( ['\n\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  return _m.popbuftext()

# #---- Global Functions

# def helloworld( x=10, y=20, a='wer', b='ehl' ) :
def helloworld( x=10, y=20, a='wer', b='ehl' ) :  
  _m.pushbuf()
  # <div>
  _m.indent()
  _m.pushbuf()
  _m.extend( ['<div', '', '', '', '>'] )
  _m.pushbuf()
  _m.extend( ['\n'] )
  _m.upindent( up='  ' )
  a = '<div> insidediv_insidebody </div>'
  
  # ${ a }
  _m.indent()
  _m.append( _m.evalexprs( a , '') )
  _m.extend( ['\n'] )
  # ${ insidediv_butglobal() }
  _m.indent()
  _m.append( _m.evalexprs( insidediv_butglobal() , '') )
  _m.extend( ['\n'] )
  _m.downindent( down='  ' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, newline='\n' )
  return _m.popbuftext()
# #---- Interface functions
# #---- Footer

_ttlhash = '9bcb09e70af084269e0ca31f6a161e65b04d8b4f'
_ttlfile = 'stdttl/fb_pycode.ttl'
