import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra                import BaseTTLPlugin


def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n\n'] )
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
  _m.extend( ['<meta http-equiv="content-type" content="text/html; charset=latin1">'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<body>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  _m.pushbuf()
  _m.extend( ['<em>'] )
  _m.pushbuf()
  _m.extend( [' Wikipédia est un projet dencyclopédie collective établie sur', '\n           ', 'Internet,', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ['universelle, multilingue et fonctionnant sur le principe du wiki.', '\n      ', 'Wikipédia a pour objectif doffrir un contenu librement réutilisable,', '\n      ', 'objectif et vérifiable, que chacun peut modifier et améliorer.', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/latin1.ttl' 