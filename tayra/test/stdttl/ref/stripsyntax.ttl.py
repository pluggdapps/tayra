
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body(  ) :  
  _m.pushbuf()
  _m.extend( [u'<!--', u"\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\nCopyright (c) 2009 SKR Farms (P) LTD.\n", u'-->', u'\n\n'] )
  # <pre>
  _m.pushbuf()
  _m.extend( [u'pre', u'<pre  >', u'</pre>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # int foo( int a, int b  ){
  _m.extend( [u'int foo( int a, int b  )', u'{', u'\n'] )
  # printf( 'helloworld' )
  _m.extend( [u"printf( 'helloworld' )", u'\n'] )
  # }
  _m.extend( [u'}', u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  # ${helloword()}
  _m.append( _m.evalexprs(helloword(), '') )
  _m.extend( [u'\n'] )
  return _m.popbuftext()

# ---- Global Functions

# def helloword( x=10, y=20, a='wer', b='ehl' ) :
def helloword( x=10, y=20, a='wer', b='ehl' ) :  
  _m.pushbuf()
  # <html>
  _m.pushbuf()
  _m.extend( [u'html', u'<html  >', u'</html>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  b = 'hello'   
  # ${x+y}
  _m.append( _m.evalexprs(x+y, '') )
  _m.extend( [u'\n'] )
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
  _m.extend( [u'\n'] )
  # <title#titleid .cls1 "title string"> hello ${a} @ ! # "helo" 'world "ok
  _m.pushbuf()
  _m.extend( [u'title', u'<title  id="titleid"   "title string"> ', u'</title>'] )
  _m.pushbuf()
  _m.extend( [u'hello '] )
  _m.append( _m.evalexprs(a, '') )
  _m.extend( [u' @ ! # "helo" \'world "ok'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
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
  # important features thatThese cameras contain electronic viewfinder,
  _m.extend( [u'important features thatThese cameras contain electronic viewfinder,', u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  # full control while shooting. In general, these cameras are all seem 
  _m.extend( [u'full control while shooting. In general, these cameras are all seem ', u'\n'] )
  # very similar.     
  _m.extend( [u'very similar.', u'\n'] )
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
  _m.extend( [u'\n\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  return _m.popbuftext()
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/stripsyntax.ttl'
