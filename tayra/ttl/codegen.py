# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

from   os.path      import join, splitext, isfile, abspath, basename
from   StringIO     import StringIO
from   copy         import deepcopy
from   hashlib      import sha1

prolog = """# -*- encoding:utf-8 -*-

from   StringIO             import StringIO
from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager
import tayra
from   tayra.ttl.runtime    import StackMachine

"""

footer = """
__ttlhash = %r
__ttlfile = %r
"""

interfaceClass = """
class %s( object ):
    implements(%s)
%s_obj = %s()
"""

class InstrGen( object ) :
    machname = '__m'

    def __init__( self ):
        self.outfd = StringIO()
        self.pyindent = ''
        self.optimaltext = []
        self.pytext = None
        # prolog for python translated template
        self.initialize( prolog )

    def __call__( self ):
        clone = InstrGen()
        return clone

    def initialize( self, prolog ):
        self.outfd.write( prolog )
        self.cr()

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

    def indent( self ):
        self.flushtext()
        self.cr()
        self.outfd.write( '__m.indent()' )

    def upindent( self, up='' ):
        self.flushtext()
        self.cr()
        self.outfd.write( '__m.upindent( up=%r )' % up )

    def downindent( self, down='' ):
        self.flushtext()
        self.cr()
        self.outfd.write( '__m.downindent( down=%r )' % down )

    def comment( self, comment ) :
        self.flushtext()
        self.cr()
        self.outfd.write( '# ' + ' '.join(comment.rstrip('\r\n').splitlines()) )

    def flushtext( self ) :
        if self.optimaltext :
            self.cr()
            self.outfd.write( '__m.extend( %s )' % self.optimaltext )
            self.optimaltext = []

    def puttext( self, text, force=False ) :
        self.optimaltext.append( text )
        if force or sum(map( lambda x : len(x), self.optimaltext)) > 100 :
            self.flushtext()

    def putvar( self, var ) :
        self.flushtext()
        self.cr()
        self.outfd.write( '__m.append( %s )' % var )

    def putstatement( self, stmt ):
        self.flushtext()
        self.cr()
        self.outfd.write( stmt.rstrip('\r\n') )

    def putblock( self, codeblock, indent=True ):
        [ self.putstatement(line) for line in codeblock.splitlines() ]

    def evalexprs( self, code ) :
        self.flushtext()
        self.cr()
        self.outfd.write( '__m.append( str(%s) )' % code )

    def pushbuf( self ):
        self.flushtext()
        self.cr()
        self.outfd.write( '__m.pushbuf()' )

    def popcompute( self, astext=True ):
        self.flushtext()
        self.cr()
        if astext == True :
            self.outfd.write( '__m.append( __m.popbuftext() )' )
        else :
            self.outfd.write( '__m.append( __m.popbuf() )' )

    def popreturn( self, astext=True ):
        self.flushtext()
        self.cr()
        if astext == True :
            self.outfd.write( 'return __m.popbuftext()' )
        else :
            self.outfd.write( 'return __m.popbuf()' )

    def computetag( self ):
        self.flushtext()
        self.cr()
        self.outfd.write( '__m.handletag( *__m.popbuf() )' )

    def putimport( self, ttlloc, modname ):
        self.cr()
        line = '%s = __m.importas( %r, %r )' % (modname, ttlloc, modname)
        self.outfd.write( line )

    def putinherit( self, ttlloc ):
        self.cr()
        self.outfd.write( '__m.inherit( %r, globals() )' % ttlloc, )

    def importinterface( self, interface ):
        self.putstatement( 'import %s' % interface )

    def implement_interface( self, implements, interfaces ):
        interfaces = {}
        [ interfaces.setdefault( ifname, [] ).append( method ) 
          for ifname, method in interfaces ]
        # Define interface class, hitch the methods and register the plugin
        for i in range(implements) :
            # Define interface implementer class
            interface, pluginname = implements[i]
            infcls = '__Interface' + str(i+1)
            codeblock = interfaceClass % ( infcls, interface, infcls, infcls )
            self.putblock( codeblock )
            # hitch methods with interface class
            for method in interfaces.get( interface, [] ) :
                line = '__m.hitch( %s_obj, %s, %s )' % (infcls, infcls, method)
                self.putstatement( line )
            # register the interface providing object
            line = '__m.register( %s_obj, %s, %r )' % ( infcls, interface,
                   pluginname )
            self.putstatement(line)

    def useinterface( self, interface, pluginname, importname ):
        line = '%s = __m.use( %s, %s )' % ( importname, interface, pluginname )
        self.putstatement(line)

    def footer( self, ttlhash, ttlfile ):
        self.cr()
        self.outfd.write( footer % (ttlhash, ttlfile) )

    def finish( self ):
        self.pytext = self.outfd.getvalue()
