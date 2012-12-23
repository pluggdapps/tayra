# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

from   io   import   StringIO

import_header = """\
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin"""

footer = """\
_ttlhash = %r
_ttlfile = %r """

interfaceClass = """\
from  %s import %s
class %s( BaseTTLPlugin ):
  implements(%s)
  pluginname = %r
  itype = 'ttlplugin' """

class InstrGen( object ):
    machname = '_m'

    def __init__( self, compiler ):
        self.compiler = compiler
        self.uglyhtml = compiler['uglyhtml']
        self.outfd = StringIO()
        self.pyindent = ''
        self.optimaltext = []
        self.pytext = None

    def __call__( self ):
        return InstrGen( self.compiler )

    #---- API

    def initialize( self ):
        self.outfd.write( import_header )
        self.cr()

    def cr( self, count=1 ):
        """Generate a new-line (along with current indentation level) in
        python generated text."""
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

    def codetext( self ):
        return self.pytext

    #---- Instruction set

    def indent( self ):
        if self.uglyhtml == False :
            self.flushtext()
            self.outline( '_m.indent()' )

    def upindent( self, up='' ):
        if self.uglyhtml == False :
            self.flushtext()
            self.outline( '_m.upindent( up=%r )' % up )

    def downindent( self, down='' ):
        if self.uglyhtml == False :
            self.flushtext()
            self.outline( '_m.downindent( down=%r )' % down )

    def comment( self, comment, force=False ):
        if self.compiler['debug'] or force :
            self.flushtext()
            self.outline( '# ' + ' '.join(comment.rstrip('\r\n').splitlines()) )

    def flushtext( self ):
        if self.optimaltext :
            self.outline( '_m.extend( %s )' % self.optimaltext )
            self.optimaltext = []

    def puttext( self, text, force=False ):
        self.optimaltext.append( text )
        self.flushtext() if force else None

    def putstatement( self, stmt ):
        self.flushtext()
        self.outline( stmt.rstrip('\r\n') )

    def putblock( self, codeblock, indent=True ):
        [ self.putstatement(line) for line in codeblock.splitlines() ]

    def evalexprs( self, s ):
        try    : code, filts = s.split('|', 1)
        except : code, filts = s, ''
        code, filts = code.strip(), filts.strip()
        if code :
            self.flushtext()
            self.outline('_m.append( _m.evalexprs(%s, %s) )' % (code, filts))

    def pushbuf( self ):
        self.flushtext()
        self.outline( '_m.pushbuf()' )

    def popappend( self, astext=True ):
        self.flushtext()
        if astext == True :
            self.outline( '_m.append( _m.popbuftext() )' )
        else :
            self.outline( '_m.append( _m.popbuf() )' )

    def popreturn( self, astext=True ):
        self.flushtext()
        if astext == True :
            self.outline( 'return _m.popbuftext()' )
        else :
            self.outline( 'return _m.popbuf()' )

    def handletag( self, indent=False, newline='' ):
        self.flushtext()
        # first arg is `content` and second arg is `tag`
        self.outline(
          '_m.handletag( _m.popbuftext(), _m.popbuftext(), indent=%s, nl=%r)'\
                  % (indent, newline)
        )

    #---- Instructions to handle directives.

    def putimport_ttl( self, ttlfile ):
        line = '%s = _m.importas( %r, globals() )' % ( modname, ttlfile )
        self.outline( line )

    def putimport( self, modnames ):
        self.outline( 'import %s' % modnames )

    def putinherit( self, ttlloc ):
        self.outline( '_m.inherit( %r, globals() )' % ttlloc, )

    def implement_interface( self, implements, interfaces ):
        interfaces_ = {}
        [ interfaces_.setdefault( ifname, [] ).append( methodname ) 
          for ifname, methodname in interfaces ]
        # Define interface class, hitch the methods and register the plugin
        for i in range(len(implements)):
            # Define interface implementer class
            module, interfacename, pluginname = implements[i]
            infcls = 'Interface_' + str(i+1)
            codeblock = interfaceClass % (
                    module, interfacename, infcls, interfacename, pluginname)
            # hitch methods with interface class
            methodlines = [ '  %s = %s' % ( method, method )
                            for method in interfaces_.get(interfacename, []) ]
            self.putblock( '\n'.join( [codeblock] + methodlines ) )
            # register the interface providing object
            line = '_m.register( %s(), %s, %r )' % (infcls, interfacename, pluginname)
            self.putstatement(line)

    def useinterface( self, module, interfacename, pluginname, name ):
        line = 'from  %s import %s' % ( module, interfacename )
        self.putstatement(line)
        if isinstance(pluginname, tuple):
            line = '%s = _m.use( %s, _m.evalexprs(%s, %r) )' % (
                        name, interfacename, pluginname[0], pluginname[1] )
        else :
            line = '%s = _m.use( %s, %r )' % ( name, interfacename, pluginname )
        self.putstatement(line)

    def footer( self, ttlhash, ttlfile ):
        self.outline( footer % (ttlhash, ttlfile) )

    def finish( self ):
        self.pytext = self.outfd.getvalue()

    #-- Local methods

    def outline( self, line, count=1 ):
        self.cr( count=count )
        self.outfd.write( line )
