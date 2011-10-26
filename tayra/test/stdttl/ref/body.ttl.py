
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body( id, cls, style='color: red;' ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( [u'div', u'<div'] )
  _m.pushbuf()
  _m.extend( [u'#'] )
  _m.append( _m.evalexprs(id, []) )
  _m.extend( [u'.'] )
  _m.append( _m.evalexprs(cls, []) )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [u''] )
  _m.append( _m.evalexprs(style, []) )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [u''] )
  _m.append( _m.popbuf() )
  _m.extend( [u'>', u'</div>'] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl=u'' )
  _m.extend( [u'\n'] )
  return _m.popbuftext()


_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/body.ttl'
