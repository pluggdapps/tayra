
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin



def body(  ) :  
  _m.pushbuf()
  _m.extend( ['<!DOCTYPE html>\n'] )
  _m.extend( [u'<!--', u"\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\nCopyright (c) 2009 SKR Farms (P) LTD.\n", u'-->', u'\n\n'] )
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
  # Let us experiment with different ways of using attributes.
  _m.extend( [u'Let us experiment with different ways of using attributes.', u'\n'] )
  # Note that attributes always follow `specifiers` and `styles`
  _m.extend( [u'Note that attributes always follow `specifiers` and `styles`', u'\n'] )
  # <div title="hello world"> attribute value is provided as a string.
  _m.pushbuf()
  _m.extend( [u'div', u'<div   title="hello world"> ', u'</div>'] )
  _m.pushbuf()
  _m.extend( [u'attribute value is provided as a string.'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  # <div disabled=disabled> attribute value is provided as an atom.
  _m.pushbuf()
  _m.extend( [u'div', u'<div   disabled=disabled> ', u'</div>'] )
  _m.pushbuf()
  _m.extend( [u'attribute value is provided as an atom.'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=False, nl='' )
  _m.extend( [u'\n'] )
  # <div#specid.floatr.fgblue dummy spec disabled=disabled>
  _m.pushbuf()
  _m.extend( [u'div', u'<div  id="specid" class="floatr fgblue"  disabled=disabled>', u'</div>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # attribute value is provided as an atom, along with specifiers
  _m.extend( [u'attribute value is provided as an atom, along with specifiers', u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  # <div#specid.floatr.fgblue dummy spec {background-color : crimson;}     disabled=disabled>
  _m.pushbuf()
  _m.extend( [u'div', u'<div  id="specid" class="floatr fgblue"  style="background-color : crimson;" disabled=disabled>', u'</div>'] )
  _m.pushbuf()
  _m.extend( [u'\n'] )
  # attribute value is provided as an atom, along with specifiers and styling
  _m.extend( [u'attribute value is provided as an atom, along with specifiers and styling', u'\n'] )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  _m.handletag( _m.popbuf(), _m.popbuf(), indent=True, nl='\n' )
  return _m.popbuftext()

# ---- Global Functions
# ---- Interface functions
# ---- Footer

_ttlhash = None
_ttlfile = '/home/pratap/mybzr/pratap/dev/tayra/tayra/test/stdttl/attributes.ttl'
