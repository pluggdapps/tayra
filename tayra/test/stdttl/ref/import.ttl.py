
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin


f = _m.importas( u'tayra:test/stdttl/funcblock.ttl', u'f', globals() )
import os, sys



def body_leftpane() :  
  _m.pushbuf()
  _m.append( _m.evalexprs(f.func3(), []) )
  _m.extend( [u'\n'] )
  return _m.popbuftext()

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/import.ttl'
