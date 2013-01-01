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
  _m.extend( ['<meta http-equiv="content-type" content="text/html; charset=UTF-8">'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<body title="ユニコードとは何か？in Japanese">'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  _m.pushbuf()
  _m.extend( ['<div>'] )
  _m.pushbuf()
  _m.extend( ['\n      ', 'Translations', '\n      '] )
  _m.pushbuf()
  _m.extend( ['<b>'] )
  _m.pushbuf()
  _m.extend( [' 什麽是Unicode', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.pushbuf()
  _m.extend( ['<a "http://統一碼/標準萬國碼">'] )
  _m.pushbuf()
  _m.extend( [' in Chinese', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.extend( ["Qu'est ce qu'Unicode? in French", '\n      ', 'Was ist Unicode? in German', '\n      ', 'Τι είναι το Unicode; in Greek (Monotonic)', '\n      ', "Cos'è Unicode? in Italian", '\n      ', 'ユニコードとは何か？in Japanese', '\n      ', '유니코드에 대해? in Korean', '\n      ', 'O que é Unicode? in Portuguese', '\n      ', 'Что такое Unicode? in Russian', '\n      ', '¿Qué es Unicode? in Spanish', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions

# ---- Footer
_ttlhash = ''
_ttlfile = '/home/pratap/dev/tayra/tayra/test/stdttl/utf8.ttl' 