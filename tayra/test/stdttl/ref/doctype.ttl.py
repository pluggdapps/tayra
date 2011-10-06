
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body( z=10 ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.0//EN" "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd">\n'] )
  _m.extend( ['<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.2//EN" "http://www.openmobilealliance.org/tech/DTD/xhtml-mobile12.dtd">\n'] )
  _m.extend( ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML Basic 1.1//EN" "http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">\n'] )
  _m.extend( ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'] )
  _m.extend( ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">\n'] )
  _m.extend( ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'] )
  _m.extend( ['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'] )
  _m.extend( ['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">\n'] )
  _m.extend( ['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'] )
  _m.extend( ['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n'] )
  # <html#std1.testcase.sample { color: red; font-size : ${z*2}px } title="hello world">
  _m.pushbuf()
  _m.extend( [u'html', u'<html'] )
  _m.pushbuf()
  _m.append( _m.Attributes( _attrstext=u' id="std1" class="testcase sample" ' ))
  _m.append( _m.popbuf() )
  _m.pushbuf()
  _m.extend( [u' color: red; font-size : '] )
  _m.append( _m.evalexprs(z*2, '') )
  _m.extend( [u'px '] )
  _m.append( _m.popbuftext() )
  _m.pushbuf()
  _m.extend( [u'title="hello world"'] )
  _m.append( _m.popbuf() )
  _m.extend( [u'>', u'</html>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # <head/>
  _m.pushbuf()
  _m.extend( [u'head', u'<head  />', ''] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  # <body>
  _m.pushbuf()
  _m.extend( [u'body', u'<body  >', u'</body>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # <abbr "World Health Organization"> WHO
  _m.pushbuf()
  _m.extend( [u'abbr', u'<abbr  title="World Health Organization"> ', u'</abbr>'] )
  _m.pushbuf()
  _m.extend( [u'WHO'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  # <button#id_ reset disabled makefriend "button value"/>
  _m.pushbuf()
  _m.extend( [u'button', u'<button  id="id_"   formaction="button value"  type="reset"/>', ''] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/doctype.ttl'
