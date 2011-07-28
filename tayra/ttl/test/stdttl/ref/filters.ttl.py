
# -*- coding: utf-8  -*-
_m.setencoding( 'utf-8 ' )
from   StringIO             import StringIO
from   zope.interface       import implements
import tayra


import re 

_m.extend( ['\n'] )
def body(  ) :  
  _m.extend( ['<!--', "\nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\n          Copyright (c) 2009 SKR Farms (P) LTD.\n"] )
  _m.extend( ['-->\n\n'] )
  html = '<div title="hello"> div block </div>'
  url  = 'http://pluggdapps.com/hello world'
  text = '  hello world \t'
  # ${ html | h }
  _m.indent()
  _m.append( _m.evalexprs( html , ' h ') )
  _m.extend( ['\n'] )
  # ${ url | u }
  _m.indent()
  _m.append( _m.evalexprs( url , ' u ') )
  _m.extend( ['\n'] )
  # ${ text | t }
  _m.indent()
  _m.append( _m.evalexprs( text , ' t ') )
  _m.extend( ['\n'] )
  return _m.popbuftext()

# #---- Global Functions
# #---- Interface functions
# #---- Footer

_ttlhash = 'bf8cbf1dd06ad18580d7c6a6d0983dc72bac93ec'
_ttlfile = 'stdttl/filters.ttl'
