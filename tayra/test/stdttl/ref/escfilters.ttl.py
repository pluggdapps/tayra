import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *

import re

def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ["<!--\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\nCopyright (c) 2011 R Pratap Chakravarthy\n-->\n\n"] )
  html = '<div title="hello"> div block </div>'
  url  = 'http://pluggdapps.com/hello world'
  text = '  hello world \t'
  unitext = 'ما هي الشفرة الموحدة "يونِكود" ؟ in Arabicc'
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.pushbuf()
  _m.extend( ['<head>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  _m.pushbuf()
  _m.extend( ['<meta http-equiv="content-type" content="text/html; charset=UTF-8">'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( ['\n    ', ''] )
  _m.append(_m.evalexprs( 'html', 'h', globals(), locals()) )
  _m.extend( ['\n    ', ''] )
  _m.append(_m.evalexprs( 'html', '', globals(), locals()) )
  _m.extend( ['\n    ', ''] )
  _m.append(_m.evalexprs( 'url', 'u', globals(), locals()) )
  _m.extend( ['\n    ', ''] )
  _m.append(_m.evalexprs( 'text', 't', globals(), locals()) )
  _m.extend( ['\n    ', ''] )
  _m.append(_m.evalexprs( 'unitext', '', globals(), locals()) )
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '././test/stdttl/escfilters.ttl' 