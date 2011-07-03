# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

from   os.path      import basename
from   StringIO     import StringIO
from   copy         import deepcopy

prolog = """# -*- encoding:utf-8 -*-

from   StringIO             import StringIO
from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager
import tayra
from   tayra.ttl.runtime    import StackMachine

#UNDEFINED = runtime.UNDEFINED
#__M_dict_builtin = dict
#__M_locals_builtin = locals
#_magic_number = 6
#_template_filename=u'/home/pratap/mybzr/pratap/dev/pluggdapps/bootstrap/bootstrap/templates/_base/base.mak'
#_template_uri=u'bootstrap:templates/_base/base.mak'
#_template_cache=cache.Cache(__name__, _modified_time)
#_source_encoding='utf-8'
#_exports = []
"""

footer = """
__ttlhash = %s
__ttlfile = %s
"""

interfaceClass = """
class %s( object ):
    implements(%s)
%s_obj = %s()
"""

class InstrGen( object ) :
    machname = '__m'

    def __init__( self, outfile=None ):
        self.outfile = outfile
        self.fd = open( outfile, 'w' ) if outfile else StringIO()
        self.pyindent = ''
        self.optimaltext = []
        self.pytext = None
        # prolog for python translated template
        self.initialize( prolog )

    def __call__( self, outfile ):
        clone = InstrGen( outfile )
        return clone

    def initialize( self, prolog ):
        self.fd.write( prolog )
        self.cr()

    def cr( self, count=1 ) :
        self.fd.write( '\n'*count )
        self.fd.write( self.pyindent )

    def codetext( self ) :
        return self.pytext

    #---- Generate Instructions

    def indent( self ):
        self.flushtext()
        self.cr()
        self.fd.write( '__m.indent()' )

    def upindent( self, up='' ):
        self.fd.write( '__m.upindent( up=%r )' % up )

    def downindent( self, down='' ):
        self.fd.write( '__m.downindent( down=%r )' % down )

    def comment( self, comment ) :
        self.cr()
        self.fd.write( '#' + comment.rstrip('\r\n') )

    def flushtext( self ) :
        if self.optimaltext :
            self.cr()
            self.fd.write( '__m.extend( %s )' % self.optimaltext )
            self.optimaltext = []

    def puttext( self, text, force=False ) :
        if sum(map( lambda x : len(x), self.optimaltext)) > 100 or force :
            self.flushtext()
        else :
            self.optimaltext.append( text )

    def putvar( self, var ) :
        self.flushtext()
        self.cr()
        self.fd.write( '__m.append( %s )' % var )

    def putstatement( self, stmt ):
        self.flushtext()
        self.cr()
        self.fd.write( stmt.rstrip('\r\n') )

    def putblock( self, codeblock, indent=True ):
        [ self.putstatement(line) for line in codeblock.splitlines() ]

    def evalexprs( self, code ) :
        self.flushtext()
        self.cr()
        self.fd.write( '__m.append( str(%s) )' % code )

    def pushbuf( self ):
        self.flushtext()
        self.cr()
        self.fd.write( '__m.pushbuf()' )

    def popcompute( self, astext=True ):
        self.flushtext()
        self.cr()
        if astext == True :
            self.fd.write( '__m.append( __m.popbuftext() )' )
        else :
            self.fd.write( '__m.append( __m.popbuf() )' )

    def popreturn( self, astext=True ):
        self.flushtext()
        self.cr()
        if astext == True :
            self.fd.write( 'return __m.popbuftext()' )
        else :
            self.fd.write( 'return __m.popbuf()' )

    def computetag( self ):
        self.flushtext()
        self.cr()
        self.fd.write( '__m.handletag( *__m.popbuf() )' )

    def blockbegin( self, line, pyindent=True ) :
        self.putstatement( line )
        if pyindent == True :
            self.pyindent += '  '

    def finish( self ):
        self.flushtext()

    def putimport( self, ttlloc, modname ):
        self.cr()
        line = '%s = __m.importas( %r, %r )' % (modname, ttlloc, modname)
        self.fd.write( line )

    def putinherit( self, ttlloc ):
        self.cr()
        self.fd.write( '__m.inherit( %r, globals() )' % ttlloc, )

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
        self.fd.write( footer % (ttlhash, ttlfile) )
        self.cr()
        if isinstance(self.fd, StringIO):
            self.pytext = self.fd.getvalue()
        else :
            self.fd.close()
            self.pytext = open(self.outfile).read()
