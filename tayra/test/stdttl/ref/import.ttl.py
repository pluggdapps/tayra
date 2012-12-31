import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *

import os, sys

def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'body_leftpane()', '', globals(), locals()) )
  _m.extend( ['\n'] )
  return _m.popbuftext()

# ---- Global Functions

def body_leftpane() :  
  _m.pushbuf()
  _m.extend( [''] )
  _m.append(_m.evalexprs( 'f.func3()', '', globals(), locals()) )
  _m.extend( ['\n  ', ''] )
  _m.append(_m.evalexprs( 'f.func4()', '', globals(), locals()) )
  _m.extend( ['\n  ', ''] )
  _m.append(_m.evalexprs( 'f.func5()', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '././test/stdttl/import.ttl' 