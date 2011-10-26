
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body(  ) :  
  _m.pushbuf()
  world = 'world'
  _m.pushbuf()
  _m.extend( [u'div', u'<div'] )
  _m.pushbuf()
  _m.append( _m.Attributes( _attrstext=u'id="id"  ' ))
  _m.append( _m.popbuf() )
  _m.pushbuf()
  _m.extend( [u"' title= hello "] )
  _m.append( _m.evalexprs(world, []) )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [u''] )
  _m.append( _m.popbuf() )
  _m.extend( [u'>', u'</div>'] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl=u'' )
  _m.extend( [u'\n'] )
  _m.pushbuf()
  _m.extend( [u'input', u'<input '] )
  _m.pushbuf()
  
  _m.append( _m.popbuf() )
  _m.pushbuf()
  _m.extend( [u"' title= hello "] )
  _m.append( _m.evalexprs(world, []) )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [u''] )
  _m.append( _m.popbuf() )
  _m.extend( [u'>', u'</input>'] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl=u'' )
  _m.extend( [u'\n'] )
  return _m.popbuftext()


_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/obfus1.ttl'
