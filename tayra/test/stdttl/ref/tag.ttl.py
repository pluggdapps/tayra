
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body(  ) :  
  _m.pushbuf()
  world = 'jasper'
  # <form#idname formname "${}http:// google.com" > ${ "hello " + str(10) +   ' world' }
  _m.pushbuf()
  _m.extend( [u'form', u'<form  id="idname"   action="${}http://\ngoogle.com" > ', u'</form>'] )
  _m.pushbuf()
  _m.append( _m.evalexprs("hello " + str(10) +   ' world', '') )
  _m.extend( [u'\n'] )
  # <input>   <!-- Comment  -->
  _m.pushbuf()
  _m.extend( [u'input', u'<input  >', u'</input>'] )
  _m.pushbuf()
  _m.extend( [u'\n\n', u' <!--', u' Comment\n ', u'-->', u'\n'] )
  # <input>          <!-- Comment          -->    
  _m.pushbuf()
  _m.extend( [u'input', u'<input  >', u'</input>'] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n', u'         <!--', u' Comment\n         ', u'-->', u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
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
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/tag.ttl'
