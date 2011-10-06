
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body( a=10, x=10, y=10, z=10, s='hello ' ) :  
  _m.pushbuf()
  # if a == 'pass' :
  if a == 'pass' :    
    pass  
  # elif a == ':' : 
  elif a == ':' :     
    pass  
  # elif a == 1 :
  elif a == 1 :    
    # Google will join its biggest mobile rival, Apple, on the space trip as well.
    _m.extend( [u'Google will join its biggest mobile rival, Apple, on the space trip as well.', u'\n'] )
    # Apple's iPhone 4 will join a crew running an app, called "SpaceLab for iOS."
    _m.extend( [u'Apple\'s iPhone 4 will join a crew running an app, called "SpaceLab for iOS."', u'\n'] )  
  # elif a== 2 :
  elif a== 2 :    
    # The program, designed by Odyssey Space Research, will allow crew members to
    _m.extend( [u'The program, designed by Odyssey Space Research, will allow crew members to', u'\n'] )
    # conduct several experiments with the phones' cameras, gyroscopes and other
    _m.extend( [u"conduct several experiments with the phones' cameras, gyroscopes and other", u'\n'] )  
  # elif a == 3 : 
  elif a == 3 :     
    # <html#std1.testcase.sample { color: red; font-size : ${z*2}px } title="hello world">
    _m.pushbuf()
    _m.extend( [u'html', u'<html'] )
    _m.pushbuf()
    _m.append( _m.Attributes( _attrstext=u' id="std1" class="testcase sample" ' ))
    _m.append( _m.popbuf() )
    _m.pushbuf()
    _m.extend( [u' color: red; font-size : '] )
    _m.append( _m.evalexprs(z*2, '') )
    _m.extend( [u'px '] )
    _m.append( _m.popbuftext() )
    _m.pushbuf()
    _m.extend( [u'title="hello world"'] )
    _m.append( _m.popbuf() )
    _m.extend( [u'>', u'</html>'] )
    _m.pushbuf()
    _m.extend( [u'\n'] )
    # <head/>
    _m.pushbuf()
    _m.extend( [u'head', u'<head  />', ''] )
    _m.pushbuf()
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
    _m.extend( [u'\n'] )
    # <body>
    _m.pushbuf()
    _m.extend( [u'body', u'<body  >', u'</body>'] )
    _m.pushbuf()
    _m.extend( [u'\n'] )
    # <abbr "World Health Organization"> WHO   
    _m.pushbuf()
    _m.extend( [u'abbr', u'<abbr  title="World Health Organization"> ', u'</abbr>'] )
    _m.pushbuf()
    _m.extend( [u'WHO'] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
    _m.extend( [u'\n'] )
    # <button#id_ reset disabled makefriend "button value"/>
    _m.pushbuf()
    _m.extend( [u'button', u'<button  id="id_"   formaction="button value"  type="reset"/>', ''] )
    _m.pushbuf()
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
    _m.extend( [u'\n\n'] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )  
  # elif a == 4 :
  elif a == 4 :    
    # <div> ${ "hello {}" + str([     str(10) ]) +     ' world' }
    _m.pushbuf()
    _m.extend( [u'div', u'<div  > ', u'</div>'] )
    _m.pushbuf()
    _m.append( _m.evalexprs("hello {}" + str([    str(10) ]) +     ' world', '') )
    _m.extend( [u'\n'] )
    # <a#${'idname \       '}.${'cls'       'name'} "${"http://"               'google.com'}" { ${'color : ' }                                ${ "red;" } } ${"title"}="${"sun is "                                                     " shining"} brightly">
    _m.pushbuf()
    _m.extend( [u'a', u'<a'] )
    _m.pushbuf()
    _m.extend( [u'#'] )
    _m.append( _m.evalexprs('idname \
      ', '') )
    _m.extend( [u'.'] )
    _m.append( _m.evalexprs('cls'      'name', '') )
    _m.extend( [u' '] )
    _m.pushbuf()
    _m.extend( [u'"'] )
    _m.append( _m.evalexprs("http://"              'google.com', '') )
    _m.extend( [u'"'] )
    _m.append( _m.popbuftext() )
    _m.append( _m.popbuftext() )
    _m.pushbuf()
    _m.extend( [u' '] )
    _m.append( _m.evalexprs('color : ', '') )
    _m.extend( [u'\n                               '] )
    _m.append( _m.evalexprs("red;", '') )
    _m.extend( [u' '] )
    _m.append( _m.popbuftext() )
    _m.pushbuf()
    _m.pushbuf()
    _m.append( _m.evalexprs("title", '') )
    _m.extend( [u'='] )
    _m.pushbuf()
    _m.extend( [u'"'] )
    _m.append( _m.evalexprs("sun is "                                                    " shining", '') )
    _m.extend( [u' ', u'brightly', u'"'] )
    _m.append( _m.popbuftext() )
    _m.append( _m.popbuftext() )
    _m.append( _m.popbuf() )
    _m.extend( [u'>', u'</a>'] )
    _m.pushbuf()
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
    _m.extend( [u'\n'] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )  
  # elif a == 5 : 
  elif a == 5 :     
    # <div {} >
    _m.pushbuf()
    _m.extend( [u'div', u'<div '] )
    _m.pushbuf()
    _m.extend( [' '] )
    _m.append( _m.popbuftext() )
    _m.pushbuf()
    _m.append( _m.popbuftext() )
    _m.pushbuf()
    _m.extend( [''] )
    _m.append( _m.popbuf() )
    _m.extend( [u'>', u'</div>'] )
    _m.pushbuf()
    _m.extend( [u'\n\n'] )
    # <a#${'idname'}.${'cls'}           "http://pluggdapps.com"       { ${'color : ' } ${ "red;"  } ' style with line         break' } /> hello {world} /> 
    _m.pushbuf()
    _m.extend( [u'a', u'<a'] )
    _m.pushbuf()
    _m.extend( [u'#'] )
    _m.append( _m.evalexprs('idname', '') )
    _m.extend( [u'.'] )
    _m.append( _m.evalexprs('cls', '') )
    _m.extend( [u'\n', u'   ', u'\n', u'      '] )
    _m.pushbuf()
    _m.extend( [u'"', u'http', u':', u'/', u'/', u'pluggdapps.com', u'"'] )
    _m.append( _m.popbuftext() )
    _m.append( _m.popbuftext() )
    _m.pushbuf()
    _m.extend( [u' '] )
    _m.append( _m.evalexprs('color : ', '') )
    _m.extend( [u' '] )
    _m.append( _m.evalexprs("red;", '') )
    _m.extend( [u" ' style with line\n        break' "] )
    _m.append( _m.popbuftext() )
    _m.pushbuf()
    _m.extend( [''] )
    _m.append( _m.popbuf() )
    _m.extend( [u'/> ', ''] )
    _m.pushbuf()
    _m.extend( [u'hello ', u'{', u'world} /> '] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
    _m.extend( [u'\n'] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )  
  # elif a == 6 :
  elif a == 6 :    
    # <html>
    _m.pushbuf()
    _m.extend( [u'html', u'<html  >', u'</html>'] )
    _m.pushbuf()
    _m.extend( [u'\n'] )
    b = 'hello'   
    # ${x+y}
    _m.append( _m.evalexprs(x+y, '') )
    _m.extend( [u'\n'] )
    # <head#headid.cls1.${s.strip(     )} "title" {color:red} lang="en"      data="hello">
    _m.pushbuf()
    _m.extend( [u'head', u'<head'] )
    _m.pushbuf()
    _m.extend( [u'#headid.cls1.'] )
    _m.append( _m.evalexprs(s.strip(    ), '') )
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
    # <title#titleid .cls1 "title          string"> hello ${s} @ ! # "helo" 'world "ok
    _m.pushbuf()
    _m.extend( [u'title', u'<title  id="titleid"   "title \n        string"> ', u'</title>'] )
    _m.pushbuf()
    _m.extend( [u'hello '] )
    _m.append( _m.evalexprs(s, '') )
    _m.extend( [u' @ ! # "helo" \'world "ok'] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
    _m.extend( [u'\n'] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
    # <body>
    _m.pushbuf()
    _m.extend( [u'body', u'<body  >', u'</body>'] )
    _m.pushbuf()
    _m.extend( [u'\n'] )
    # <h1 { color : red;   border : 1px solid gray;       }/> I am the space station ${ "These "} seven cameras       <!-- comment1      comment -->
    _m.pushbuf()
    _m.extend( [u'h1', u'<h1   style=" color : red;\n  border : 1px solid gray;\n      "/> ', ''] )
    _m.pushbuf()
    _m.extend( [u'I am the space station '] )
    _m.append( _m.evalexprs("These ", '') )
    _m.extend( [u' seven cameras'] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
    _m.extend( [u'\n', u'      <!--', u' comment1\n     comment ', u'-->', u'\n'] )
    # have a zoom range 
    _m.extend( [u'have a zoom range ', u'\n'] )
    # <p first       second> of any 12x or more,       <!-- comment1          comment -->
    _m.pushbuf()
    _m.extend( [u'p', u'<p  > ', u'</p>'] )
    _m.pushbuf()
    _m.extend( [u'of any 12x or more,'] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
    _m.extend( [u'\n', u'      <!--', u' comment1\n         comment ', u'-->', u'\n'] )
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
    _m.extend( [u'important for people who are with a powerful zoom lens. Some other', u'\n'] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
    # important features thatThese cameras contain electronic viewfinder,         <!-- comment1 comment -->   
    _m.extend( [u'important features thatThese cameras contain electronic viewfinder,', u'\n', u'        <!--', u' comment1 comment ', u'-->', u'\n'] )
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
    _m.extend( [u'\n'] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )  
  # elif a == 7 :
  elif a == 7 :    
    world = 10
    # <form#idname   formname "${}http://   google.com" > ${ "hello " + str(10) +     ' world' }
    _m.pushbuf()
    _m.extend( [u'form', u'<form  id="idname"   action="${}http://\n  google.com" > ', u'</form>'] )
    _m.pushbuf()
    _m.append( _m.evalexprs("hello " + str(10) +     ' world', '') )
    _m.extend( [u'\n'] )
    # <input text  =$_0(*&^%%$#@!@~}= world }$ {' title= hello ${world}}>
    _m.pushbuf()
    _m.extend( [u'input', u'<input '] )
    _m.pushbuf()
    _m.append( _m.Attributes( _attrstext=' ' ))
    _m.append( _m.popbuf() )
    _m.pushbuf()
    _m.extend( [u"' title= hello "] )
    _m.append( _m.evalexprs(world, '') )
    _m.append( _m.popbuftext() )
    _m.pushbuf()
    _m.extend( [''] )
    _m.append( _m.popbuf() )
    _m.extend( [u'>', u'</input>'] )
    _m.pushbuf()
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
    _m.extend( [u'\n'] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )  
  # else :
  else :    
    # sensors. Each device will include step-by-step directions for the astronauts,
    _m.extend( [u'sensors. Each device will include step-by-step directions for the astronauts,', u'\n'] )
    # eliminating the need for printed instructions.
    _m.extend( [u'eliminating the need for printed instructions.', u'\n'] )  
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/ifblock.ttl'
