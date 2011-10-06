
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body(  ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n'] )
  # !!! escaping doctypes ;
  _m.extend( [u'!', u'!! escaping doctypes ;', u'\n'] )
  # @charset escaping directives;
  _m.extend( [u'@', u'charset escaping directives;', u'\n'] )
  # @body any directive;
  _m.extend( [u'@', u'body any directive;', u'\n\n'] )
  # <html>
  _m.pushbuf()
  _m.extend( [u'html', u'<html  >', u'</html>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # <head>
  _m.pushbuf()
  _m.extend( [u'head', u'<head  >', u'</head>'] )
  _m.pushbuf()
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  # <body>
  _m.pushbuf()
  _m.extend( [u'body', u'<body  >', u'</body>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  #   Escaping the indent
  _m.extend( [u' ', u' ', u'Escaping the indent', u'\n'] )
  # <div>
  _m.pushbuf()
  _m.extend( [u'div', u'<div  >', u'</div>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # Escaping newlines across textblocks, all of this belongs to body content.
  _m.extend( [u'Escaping newlines ', u'across textblocks, all of this belongs to body content.', u'\n'] )
  # @function escapedfunction():
  _m.extend( [u'@', u'function escapedfunction():', u'\n'] )
  # @@pass
  _m.extend( [u'@', u'@', u'pass', u'\n'] )
  # ${ this expresion is also escaped } and displayed as text
  _m.extend( [u'$', u'{', u' this expresion is also escaped } and displayed as text', u'\n'] )
  # @if so is this if block :
  _m.extend( [u'@', u'if so is this if block :', u'\n'] )
  # @elif block :
  _m.extend( [u'@', u'elif block :', u'\n'] )
  # @else block :
  _m.extend( [u'@', u'else block :', u'\n'] )
  # @for block :
  _m.extend( [u'@', u'for block :', u'\n'] )
  # @while block :
  _m.extend( [u'@', u'while block :', u'\n'] )
  # all of them are interpreted as text.
  _m.extend( [u'all of them are interpreted as text.', u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  # ${ willbecomeglobal() }
  _m.append( _m.evalexprs(willbecomeglobal(), '') )
  _m.extend( [u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  return _m.popbuftext()

# ---- Global Functions

# def willbecomeglobal( *args ):
def willbecomeglobal( *args ):  
  _m.pushbuf()
  # <b> Ghost
  _m.pushbuf()
  _m.extend( [u'b', u'<b  > ', u'</b>'] )
  _m.pushbuf()
  _m.extend( [u'Ghost'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  
  _m.extend( [u'\n'] )
  # def nestedfunc():
  def nestedfunc():    
    _m.pushbuf()
    # <em> Rider
    _m.pushbuf()
    _m.extend( [u'em', u'<em  > ', u'</em>'] )
    _m.pushbuf()
    _m.extend( [u'Rider'] )
    _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
    _m.extend( [u'\n'] )
    return _m.popbuftext()  
  # ${ nestedfunc() }
  _m.append( _m.evalexprs(nestedfunc(), '') )
  _m.extend( [u'\n'] )
  return _m.popbuftext()
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/escapes.ttl'
