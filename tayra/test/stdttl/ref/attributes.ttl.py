import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra                import BaseTTLPlugin


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ["<!--\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\nCopyright (c) 2011 R Pratap Chakravarthy\n-->\n\n"] )
  _m.extend( ['<!DOCTYPE html>\n    \n'] )
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.pushbuf()
  _m.extend( ['<head>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( ['\n    ', 'Let us experiment with different ways of using attributes.', '\n    ', 'Note that attributes always follow `specifiers` and `styles`', '\n    '] )
  _m.pushbuf()
  _m.extend( ['<div title="hello world">'] )
  _m.pushbuf()
  _m.extend( [' attribute value is provided as a string.', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<div disabled="disabled">'] )
  _m.pushbuf()
  _m.extend( [' attribute value is provided as an atom.', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<div #specid .floatr.fgblue dummy spec disabled>'] )
  _m.pushbuf()
  _m.extend( ['\n      ', 'attribute value is provided as an atom, along with specifiers', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<a>'] )
  _m.pushbuf()
  _m.extend( [' fine clause', '\n      \n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<div #spcid .floatr.fgblue dummy {background-color : crimson;}\n         disabled>'] )
  _m.pushbuf()
  _m.extend( ['\n      ', 'attribute value is provided as an atom, along with specifiers and styling', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<a>'] )
  _m.pushbuf()
  _m.extend( [' hello world', '\n      \n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/attributes.ttl' 