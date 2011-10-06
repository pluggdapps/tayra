
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body(  ) :  
  _m.pushbuf()
  # <div> ${ "hello {}" + str([   str(10) ]) +    ' world' }
  _m.pushbuf()
  _m.extend( [u'div', u'<div  > ', u'</div>'] )
  _m.pushbuf()
  _m.append( _m.evalexprs("hello {}" + str([  str(10) ]) +   ' world', '') )
  _m.extend( [u'\n'] )
  # <a#${'idname'}.${'cls'     'name'} "${"http://"             'google.com'}" { ${'color : ' }                              ${ "red;" } } ${"title"}="${"sun is "                                                     " shining"} brightly"/>
  _m.pushbuf()
  _m.extend( [u'a', u'<a'] )
  _m.pushbuf()
  _m.extend( [u'#'] )
  _m.append( _m.evalexprs('idname', '') )
  _m.extend( [u'.'] )
  _m.append( _m.evalexprs('cls'    'name', '') )
  _m.extend( [u' '] )
  _m.pushbuf()
  _m.extend( [u'"'] )
  _m.append( _m.evalexprs("http://"            'google.com', '') )
  _m.extend( [u'"'] )
  _m.append( _m.popbuftext() )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [u' '] )
  _m.append( _m.evalexprs('color : ', '') )
  _m.extend( [u'\n                             '] )
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
  _m.extend( [u'/>', ''] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/exprs.ttl'
