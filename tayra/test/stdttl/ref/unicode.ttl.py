
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body(  ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n'] )
  # <html>
  _m.pushbuf()
  _m.extend( [u'html', u'<html  >', u'</html>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # <head>
  _m.pushbuf()
  _m.extend( [u'head', u'<head  >', u'</head>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  _m.pushbuf()
  _m.extend( [u'meta', u'<meta   http-equiv="content-type" content="text/html; charset=UTF-8">', u'</meta>'] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  # <body>
  _m.pushbuf()
  _m.extend( [u'body', u'<body  >', u'</body>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # <div>
  _m.pushbuf()
  _m.extend( [u'div', u'<div  >', u'</div>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # Translations
  _m.extend( [u'Translations', u'\n'] )
  # ما هي الشفرة الموحدة "يونِكود" ؟ in Arabic
  _m.extend( [u'\u0645\u0627 \u0647\u064a \u0627\u0644\u0634\u0641\u0631\u0629 \u0627\u0644\u0645\u0648\u062d\u062f\u0629 "\u064a\u0648\u0646\u0650\u0643\u0648\u062f" \u061f in Arabic', u'\n'] )
  # ইউনিকোড কী? in Bangla
  _m.extend( [u'\u0987\u0989\u09a8\u09bf\u0995\u09cb\u09a1 \u0995\u09c0? in Bangla', u'\n'] )
  # 什麽是Unicode(統一碼/標準萬國碼)? in Trad'l Chinese
  _m.extend( [u"\u4ec0\u9ebd\u662fUnicode(\u7d71\u4e00\u78bc/\u6a19\u6e96\u842c\u570b\u78bc)? in Trad'l Chinese", u'\n'] )
  # Qu'est ce qu'Unicode? in French
  _m.extend( [u"Qu'est ce qu'Unicode? in French", u'\n'] )
  # Was ist Unicode? in German
  _m.extend( [u'Was ist Unicode? in German', u'\n'] )
  # Τι είναι το Unicode; in Greek (Monotonic)
  _m.extend( [u'\u03a4\u03b9 \u03b5\u03af\u03bd\u03b1\u03b9 \u03c4\u03bf Unicode; in Greek (Monotonic)', u'\n'] )
  # מה זה יוניקוד (Unicode)? in Hebrew
  _m.extend( [u'\u05de\u05d4 \u05d6\u05d4 \u05d9\u05d5\u05e0\u05d9\u05e7\u05d5\u05d3 (Unicode)? in Hebrew', u'\n'] )
  # यूनिकोड क्या है? in Hindi
  _m.extend( [u'\u092f\u0942\u0928\u093f\u0915\u094b\u0921 \u0915\u094d\u092f\u093e \u0939\u0948? in Hindi', u'\n'] )
  # Cos'è Unicode? in Italian
  _m.extend( [u"Cos'\xe8 Unicode? in Italian", u'\n'] )
  # ユニコードとは何か？in Japanese
  _m.extend( [u'\u30e6\u30cb\u30b3\u30fc\u30c9\u3068\u306f\u4f55\u304b\uff1fin Japanese', u'\n'] )
  # 유니코드에 대해? in Korean
  _m.extend( [u'\uc720\ub2c8\ucf54\ub4dc\uc5d0 \ub300\ud574? in Korean', u'\n'] )
  # O que é Unicode? in Portuguese
  _m.extend( [u'O que \xe9 Unicode? in Portuguese', u'\n'] )
  # Что такое Unicode? in Russian
  _m.extend( [u'\u0427\u0442\u043e \u0442\u0430\u043a\u043e\u0435 Unicode? in Russian', u'\n'] )
  # ¿Qué es Unicode? in Spanish
  _m.extend( [u'\xbfQu\xe9 es Unicode? in Spanish', u'\n'] )
  # யூனிக்கோடு என்றால் என்ன?, in Tamil
  _m.extend( [u'\u0baf\u0bc2\u0ba9\u0bbf\u0b95\u0bcd\u0b95\u0bcb\u0b9f\u0bc1 \u0b8e\u0ba9\u0bcd\u0bb1\u0bbe\u0bb2\u0bcd \u0b8e\u0ba9\u0bcd\u0ba9?, in Tamil', u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/unicode.ttl'
