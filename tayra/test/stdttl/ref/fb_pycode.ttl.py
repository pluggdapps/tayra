
_m.setencoding( u'utf-8 ' )
a = 'empty'
def insideroot_butglobal():
  return '<div> insideroot_butglobal </div>'
a = 'empty'
def insidediv_butglobal():
  return '<div> insidediv_butglobal </div>'

from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin


import re 
a = 'empty'
def insidediv_butglobal():
  return '<div> insidediv_butglobal </div>'


def body(  ) :  
  _m.pushbuf()
  _m.extend( [u'<!--', u"\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\n          Copyright (c) 2009 SKR Farms (P) LTD.\n", u'-->', u'\n\n'] )
  b = '<div> insideroot_insidebody </div>'
  # ${ a } ${ insideroot_butglobal() }
  _m.append( _m.evalexprs(a, '') )
  _m.extend( [u' '] )
  _m.append( _m.evalexprs(insideroot_butglobal(), '') )
  _m.extend( [u'\n'] )
  # ${ b }
  _m.append( _m.evalexprs(b, '') )
  _m.extend( [u'\n\n'] )
  # <html>
  _m.pushbuf()
  _m.extend( [u'html', u'<html  >', u'</html>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  b = 'hello'   
  # <head#headid.cls1.${a.strip()} "title" {color:red} lang="en" data="hello">
  _m.pushbuf()
  _m.extend( [u'head', u'<head'] )
  _m.pushbuf()
  _m.extend( [u'#headid.cls1.'] )
  _m.append( _m.evalexprs(a.strip(), '') )
  _m.extend( [u' '] )
  _m.pushbuf()
  _m.extend( [u'"', u'title', u'"'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [u'style="color:red"'] )
  _m.append( _m.popbuf() )
  _m.pushbuf()
  _m.extend( [u'lang="en" data="hello"'] )
  _m.append( _m.popbuf() )
  _m.extend( [u'>', u'</head>'] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  # <body>
  _m.pushbuf()
  _m.extend( [u'body', u'<body  >', u'</body>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # <h1 { color : red; border : 1px solid gray; }/> I am the space station ${ "These "} seven cameras
  _m.pushbuf()
  _m.extend( [u'h1', u'<h1   style=" color : red; border : 1px solid gray; "/> ', ''] )
  _m.pushbuf()
  _m.extend( [u'I am the space station '] )
  _m.append( _m.evalexprs("These ", '') )
  _m.extend( [u' seven cameras'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  # have a zoom range 
  _m.extend( [u'have a zoom range ', u'\n'] )
  # <p first second> of any 12x or more,  ${20}  
  _m.pushbuf()
  _m.extend( [u'p', u'<p  > ', u'</p>'] )
  _m.pushbuf()
  _m.extend( [u'of any 12x or more,  '] )
  _m.append( _m.evalexprs(20, '') )
  _m.extend( [u'  '] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  # and some of the wide-angle view 
  _m.extend( [u'and some of the wide-angle view ', u'\n'] )
  # <div> of good. They also have a
  _m.pushbuf()
  _m.extend( [u'div', u'<div  > ', u'</div>'] )
  _m.pushbuf()
  _m.extend( [u'of good. They also have a', u'\n'] )
  # lot of image stabilization (either optical or mechanical), which is 
  _m.extend( [u'lot of image stabilization (either optical or mechanical), which is ', u'\n'] )
  # important for people who are with a powerful zoom lens. Some other        
  _m.extend( [u'important for people who are with a powerful zoom lens. Some other        ', u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  # ${ helloworld() }
  _m.append( _m.evalexprs(helloworld(), '') )
  _m.extend( [u'\n'] )
  # <p#${b}> Sign my guestbook
  _m.pushbuf()
  _m.extend( [u'p', u'<p'] )
  _m.pushbuf()
  _m.extend( [u'#'] )
  _m.append( _m.evalexprs(b, '') )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [''] )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [''] )
  _m.append( _m.popbuf() )
  _m.extend( [u'> ', u'</p>'] )
  _m.pushbuf()
  _m.extend( [u'Sign my guestbook'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  # ${ insideroot_butglobal() }
  _m.append( _m.evalexprs(insideroot_butglobal(), '') )
  _m.extend( [u'\n\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  return _m.popbuftext()

# ---- Global Functions

# def helloworld( x=10, y=20, a='wer', b='ehl' ) :
def helloworld( x=10, y=20, a='wer', b='ehl' ) :  
  _m.pushbuf()
  # <div>
  _m.pushbuf()
  _m.extend( [u'div', u'<div  >', u'</div>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  a = '<div> insidediv_insidebody </div>'
  
  # ${ a }
  _m.append( _m.evalexprs(a, '') )
  _m.extend( [u'\n'] )
  # ${ insidediv_butglobal() }
  _m.append( _m.evalexprs(insidediv_butglobal(), '') )
  _m.extend( [u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  return _m.popbuftext()
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/fb_pycode.ttl'
