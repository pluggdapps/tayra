# -*- encoding:utf-8 -*-

from   StringIO             import StringIO
from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager
import tayra
from   tayra.ttl.runtime    import StackMachine



__m.extend( ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.0//EN" "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd">\n'] )
__m.extend( ['<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.2//EN" "http://www.openmobilealliance.org/tech/DTD/xhtml-mobile12.dtd">\n'] )
__m.extend( ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML Basic 1.1//EN" "http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">\n'] )
__m.extend( ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'] )
__m.extend( ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">\n'] )
__m.extend( ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'] )
__m.extend( ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'] )
__m.extend( ['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">\n'] )
__m.extend( ['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'] )
__m.extend( ['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n'] )
__m.extend( ['\n'] )
def body( z=10 ) :  
  # <html#std1.testcase.sample { color: red; font-size : ${z*2}px } title="hello world">
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<html'] )
  __m.pushbuf()
  __m.extend( ['#std1.testcase.sample'] )
  __m.append( __m.popbuftext() )
  __m.pushbuf()
  __m.extend( [' color: red; font-size : '] )
  __m.append( str(z*2) )
  __m.extend( ['px '] )
  __m.append( __m.popbuftext() )
  __m.pushbuf()
  __m.pushbuf()
  __m.extend( ['title', '='] )
  __m.pushbuf()
  __m.extend( ['"', 'hello', ' ', 'world', '"'] )
  __m.append( __m.popbuftext() )
  __m.append( __m.popbuftext() )
  __m.append( __m.popbuf() )
  __m.extend( ['>'] )
  __m.handletag( *__m.popbuf() )
  __m.extend( ['\n'] )
  __m.upindent( up='  ' )
  # <head/>
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<head', '', '', '', '/>'] )
  __m.handletag( *__m.popbuf() )
  __m.extend( ['\n'] )
  # <body>
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<body', '', '', '', '>'] )
  __m.handletag( *__m.popbuf() )
  __m.extend( ['\n'] )
  __m.upindent( up='  ' )
  # <abbr "World Health Organization"> WHO
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<abbr '] )
  __m.pushbuf()
  __m.pushbuf()
  __m.extend( ['"', 'World', ' ', 'Health', ' ', 'Organization', '"'] )
  __m.append( __m.popbuftext() )
  __m.append( __m.popbuftext() )
  __m.extend( ['', '', '> '] )
  __m.handletag( *__m.popbuf() )
  __m.extend( ['WHO', '\n'] )
  __m.indent()
  __m.extend( ['</abbr>\n'] )
  # <button#id_ reset disabled makefriend "button value"/>
  __m.indent()
  __m.pushbuf()
  __m.extend( ['<button'] )
  __m.pushbuf()
  __m.extend( ['#id_', ' ', 'reset', ' ', 'disabled', ' ', 'makefriend', ' '] )
  __m.pushbuf()
  __m.extend( ['"', 'button', ' ', 'value', '"'] )
  __m.append( __m.popbuftext() )
  __m.append( __m.popbuftext() )
  __m.extend( ['', '', '/>'] )
  __m.handletag( *__m.popbuf() )
  __m.extend( ['\n'] )
  __m.downindent( down='  ' )
  __m.indent()
  __m.extend( ['</body>\n'] )
  __m.downindent( down='  ' )
  __m.indent()
  __m.extend( ['</html>\n'] )
  return __m.popbuftext()

__ttlhash = '65b2c0e032eebaef7f4dd2e1629d4cb2baba66fb'
__ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/ttl/test/stdttl/doctype.ttl'
