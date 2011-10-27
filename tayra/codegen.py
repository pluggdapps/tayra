# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

from   os.path      import join, splitext, isfile, abspath, basename
from   StringIO     import StringIO
from   copy         import deepcopy
from   hashlib      import sha1

prolog = """
from   StringIO             import StringIO
from   zope.interface       import implements
from   tayra                import BaseTTLPlugin
from   tayra.decorator      import *
"""

footer = """
_ttlhash = %r
_ttlfile = %r
"""

interfaceClass = """
from  %s import %s
class %s( BaseTTLPlugin ):
  implements(%s)
  pluginname = %r
  itype = 'ttlplugin'"""

class InstrGen( object ) :
    machname = '_m'

    def __init__( self, compiler, ttlconfig={} ):
        from   tayra    import DEFAULT_ENCODING
        self.compiler = compiler
        self.ttlconfig = ttlconfig
        self.devmod = self.ttlconfig['devmod']
        self.uglyhtml = self.ttlconfig['uglyhtml']
        self.outfd = StringIO()
        self.pyindent = u''
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
        if self.uglyhtml == False :
            self.flushtext()
            self.cr()
            self.outfd.write( '_m.indent()' )

    def upindent( self, up=u'' ):
        if self.uglyhtml == False :
            self.flushtext()
            self.cr()
            self.outfd.write( '_m.upindent( up=%r )' % up )

    def downindent( self, down=u'' ):
        if self.uglyhtml == False :
            self.flushtext()
            self.cr()
            self.outfd.write( '_m.downindent( down=%r )' % down )

    def comment( self, comment ) :
        if self.devmod :
            self.flushtext()
            self.cr()
            self.outfd.write( '# ' + u' '.join(comment.rstrip('\r\n').splitlines()) )

    def flushtext( self ) :
        if self.optimaltext :
            self.cr()
            self.outfd.write( '_m.extend( %s )' % self.optimaltext )
            self.optimaltext = []

    def puttext( self, text, force=False ):
        self.optimaltext.append( text )
        if force :
            self.flushtext()

    def putattrs( self, attrstext=None, attrslist=None ):
        self.flushtext()
        self.cr()
        attrstext and self.outfd.write(
            '_m.append( _m.Attributes( _attrstext=%r ))' % attrstext
        )
        attrslist and self.outfd.write(
            '_m.append( _m.Attributes( _attrslist=%r ))' % attrslist
        )

    def putstatement( self, stmt ):
        self.flushtext()
        self.cr()
        self.outfd.write( stmt.rstrip('\r\n') )

    def putblock( self, codeblock, indent=True ):
        [ self.putstatement(line) for line in codeblock.splitlines() ]

    def evalexprs( self, code, filters ) :
        code = code.strip()
        if code :
            self.flushtext()
            self.cr()
            self.outfd.write('_m.append( _m.evalexprs(%s, %s) )' % (code, filters))

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

    def handletag( self, indent=False, newline=u'' ):
        self.flushtext()
        self.cr()
        # first arg is `content` and second arg is `tag`
        self.outfd.write(
            '_m.handletag( _m.popbuf(), _m.popbuf(), indent=%s, nl=%r )'%(
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

    def implement_interface( self, implements, interfaces ):
        interfaces_ = {}
        [ interfaces_.setdefault( ifname, [] ).append( methodname ) 
          for ifname, methodname in interfaces ]
        # Define interface class, hitch the methods and register the plugin
        for i in range(len(implements)) :
            # Define interface implementer class
            module, interfacename, pluginname = implements[i]
            infcls = 'Interface_' + str(i+1)
            codeblock = interfaceClass % (
                    module, interfacename, infcls, interfacename, pluginname)
            # hitch methods with interface class
            methodlines = [ '  %s = %s' % ( method, method )
                            for method in interfaces_.get(interfacename, []) ]
            self.putblock( u'\n'.join( [codeblock] + methodlines ) )
            # register the interface providing object
            line = '_m.register( %s(), %s, %r )' % (infcls, interfacename, pluginname)
            self.putstatement(line)

    def useinterface( self, module, interfacename, pluginname, name ):
        line = 'from  %s import %s' % ( module, interfacename )
        self.putstatement(line)
        if isinstance(pluginname, tuple) :
            line = '%s = _m.use( %s, _m.evalexprs(%s, %r) )' % (
                        name, interfacename, pluginname[0], pluginname[1] )
        else :
            line = '%s = _m.use( %s, %r )' % ( name, interfacename, pluginname )
        self.putstatement(line)

    def footer( self, ttlhash, ttlfile ):
        self.cr()
        self.outfd.write( footer % (ttlhash, ttlfile) )

    def finish( self ):
        self.pytext = self.outfd.getvalue()
