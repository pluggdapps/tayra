import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra                import BaseTTLPlugin


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ["<!--\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\n    Copyright (c) 2010 SKR Farms (P) LTD.\n-->\n\n"] )
  return _m.popbuftext()

# ---- Global Functions

def _toc( level, heads ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<ul>'] )
  _m.pushbuf()
  _m.extend( ['\n    ', '\n      '] )
  # for href, text, children in heads :
  for href, text, children in heads :    
    _m.pushbuf()
    _m.extend( ['<li>'] )
    _m.pushbuf()
    _m.extend( ['\n        '] )
    _m.pushbuf()
    _m.extend( ['<a .level'] )
    _m.append(_m.evalexprs( 'level', '', globals(), locals()) )
    _m.extend( [' "'] )
    _m.append(_m.evalexprs( 'href', '', globals(), locals()) )
    _m.extend( ['">'] )
    _m.pushbuf()
    _m.extend( [' '] )
    _m.append(_m.evalexprs( 'text', '', globals(), locals()) )
    _m.extend( ['\n      '] )
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
    _m.extend( [''] )
    _m.append(_m.evalexprs( "children and _toc( level+1, children ) or ''", '', globals(), locals()) )
    _m.extend( ['\n\n'] )  
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()


def toc( details, heads ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<details .toc>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  _m.pushbuf()
  _m.extend( ['<summary>'] )
  _m.pushbuf()
  _m.extend( [' '] )
  _m.append(_m.evalexprs( 'details', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( [''] )
  _m.append(_m.evalexprs( '_toc( 1, heads )', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()


def papowered( pcount, icount ) :  
  _m.pushbuf()
  _m.pushbuf()
  _m.extend( ['<div .papowered>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  _m.pushbuf()
  _m.extend( ['<div .stmt>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  _m.pushbuf()
  _m.extend( ['<span .prop>'] )
  _m.pushbuf()
  _m.extend( [' On', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['pluggdapps', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<div .counts>'] )
  _m.pushbuf()
  _m.extend( [' '] )
  _m.append(_m.evalexprs( 'pcount', '', globals(), locals()) )
  _m.extend( [' plugins via '] )
  _m.append(_m.evalexprs( 'icount', '', globals(), locals()) )
  _m.extend( [' interface', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/element.ttl' 