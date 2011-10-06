
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body(  ) :  
  _m.pushbuf()
  # <div#_id.cls {color: red} a="b">
  _m.pushbuf()
  _m.extend( [u'div', u'<div  id="_id" class="cls"  style="color: red" a="b">', u'</div>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # <a#${'idname'}.${'cls'}     "http://pluggdapps.com"     { ${'color : ' } ${ "red;"  } ' style with line       break' } /> hello {world}
  _m.pushbuf()
  _m.extend( [u'a', u'<a'] )
  _m.pushbuf()
  _m.extend( [u'#'] )
  _m.append( _m.evalexprs('idname', '') )
  _m.extend( [u'.'] )
  _m.append( _m.evalexprs('cls', '') )
  _m.extend( [u'\n', u'    '] )
  _m.pushbuf()
  _m.extend( [u'"', u'http', u':', u'/', u'/', u'pluggdapps.com', u'"'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [u' '] )
  _m.append( _m.evalexprs('color : ', '') )
  _m.extend( [u' '] )
  _m.append( _m.evalexprs("red;", '') )
  _m.extend( [u" ' style with line\n      break' "] )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [''] )
  _m.append( _m.popbuf() )
  _m.extend( [u'/> ', ''] )
  _m.pushbuf()
  _m.extend( [u'hello ', u'{', u'world}'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/style.ttl'
