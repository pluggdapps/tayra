# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

from   os.path      import join, splitext, isfile, abspath, basename
from   StringIO     import StringIO
from   copy         import deepcopy
from   hashlib      import sha1

prolog = """
from   StringIO             import StringIO
from   zope.interface       import implements
import tayra
"""

footer = """
_ttlhash = %r
_ttlfile = %r
"""

interfaceClass = """
class %s( object ):
  implements(%s)
%s = %s()
"""

class InstrGen( object ) :
    machname = '_m'

    def __init__( self, compiler, ttlconfig={} ):
        from   tayra.ttl        import DEFAULT_ENCODING
        self.compiler = compiler
        self.ttlconfig = ttlconfig
        self.devmod = self.ttlconfig.get( 'devmod', True )
        self.outfd = StringIO()
        self.pyindent = ''
        self.optimaltext = []
        self.pytext = None
        # prolog for python translated template
        self.encoding = ttlconfig.get( 'input_encoding', DEFAULT_ENCODING )

    def __call__( self ):
        clone = InstrGen( self.compiler, ttlconfig=self.ttlconfig )
        return clone

    def cr( self, count=1 ) :
        self.outfd.write( '\n'*count )
        self.outfd.write( self.pyindent )

    def codeindent( self, up=None, down=None, indent=True ):
        self.flushtext()
        if up != None :
            self.pyindent += up
        if down != None :
            self.pyindent = self.pyindent[:-len(down)]
        if indent : 
            self.outfd.write( self.pyindent )

    def codetext( self ) :
        return self.pytext

    #---- Generate Instructions

    def initialize( self ):
        self.outfd.write( prolog )
        self.cr()

    def indent( self ):
        self.flushtext()
        self.cr()
        self.outfd.write( '_m.indent()' )

    def upindent( self, up='' ):
        self.flushtext()
        self.cr()
        self.outfd.write( '_m.upindent( up=%r )' % up )

    def downindent( self, down='' ):
        self.flushtext()
        self.cr()
        self.outfd.write( '_m.downindent( down=%r )' % down )

    def comment( self, comment ) :
        if self.devmod :
            self.flushtext()
            self.cr()
            self.outfd.write( '# ' + ' '.join(comment.rstrip('\r\n').splitlines()) )

    def flushtext( self ) :
        if self.optimaltext :
            self.cr()
            self.outfd.write( '_m.extend( %s )' % self.optimaltext )
            self.optimaltext = []

    def puttext( self, text, force=False ) :
        self.optimaltext.append( text )
        if force or sum(map( lambda x : len(x), self.optimaltext)) > 100 :
            self.flushtext()

    def putstatement( self, stmt ):
        self.flushtext()
        self.cr()
        self.outfd.write( stmt.rstrip('\r\n') )

    def putblock( self, codeblock, indent=True ):
        [ self.putstatement(line) for line in codeblock.splitlines() ]

    def evalexprs( self, code, filters ) :
        self.flushtext()
        self.cr()
        self.outfd.write('_m.append( _m.evalexprs(%s, %r) )' % (code, filters))

    def pushbuf( self ):
        self.flushtext()
        self.cr()
        self.outfd.write( '_m.pushbuf()' )

    def popcompute( self, astext=True ):
        self.flushtext()
        self.cr()
        if astext == True :
            self.outfd.write( '_m.append( _m.popbuftext() )' )
        else :
            self.outfd.write( '_m.append( _m.popbuf() )' )

    def popreturn( self, astext=True ):
        self.flushtext()
        self.cr()
        if astext == True :
            self.outfd.write( 'return _m.popbuftext()' )
        else :
            self.outfd.write( 'return _m.popbuf()' )

    def handletag( self, indent=False, newline='' ):
        self.flushtext()
        self.cr()
        # first arg is `content` and second arg is `tag`
        self.outfd.write(
            '_m.handletag( _m.popbuf(), _m.popbuf(), indent=%s, newline=%r )'%(
                indent, newline
            )
        )

    def putimport_ttl( self, ttlloc, modname ):
        self.cr()
        line = '%s = _m.importas( %r, %r, globals() )' % (modname, ttlloc, modname)
        self.outfd.write( line )

    def putimport( self, modnames ):
        self.cr()
        self.outfd.write( 'import %s' % modnames )

    def putinherit( self, ttlloc ):
        self.cr()
        self.outfd.write( '_m.inherit( %r, globals() )' % ttlloc, )

    def importinterface( self, interface ):
        self.putstatement( 'import %s' % interface )

    def implement_interface( self, implements, interfaces ):
        interfaces_ = {}
        [ interfaces_.setdefault( ifname, [] ).append( method ) 
          for ifname, method in interfaces ]
        # Define interface class, hitch the methods and register the plugin
        for i in range(len(implements)) :
            # Define interface implementer class
            interface, pluginname = implements[i]
            infcls = 'Interface_' + str(i+1)
            infobj = '%s_obj' % infcls
            codeblock = interfaceClass % ( infcls, interface, infobj, infcls )
            self.putblock( codeblock )
            # hitch methods with interface class
            for method in interfaces_.get( interface, [] ) :
                line = '%s.%s = _m.hitch( %s, %s, %s )' % (
                            infobj, method, infobj, infcls, method )
                self.putstatement( line )
            # register the interface providing object
            line = '_m.register( %s_obj, %s, %r )' % ( infcls, interface,
                   pluginname )
            self.putstatement(line)

    def useinterface( self, interface, pluginname, name ):
        line = '%s = _m.use( %s, %r )' % ( name, interface, pluginname )
        self.putstatement(line)

    def footer( self, ttlhash, ttlfile ):
        self.cr()
        self.outfd.write( footer % (ttlhash, ttlfile) )

    def finish( self ):
        self.pytext = self.outfd.getvalue()
