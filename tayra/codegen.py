# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Instruction generator for :class:`StackMachine`. Generates the intermediate
python file."""

from   io   import   StringIO

import_header = """\
import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra                import BaseTTLPlugin"""

footer = """\
_ttlhash = %r
_ttlfile = %r """

importtext = """\
__compiler = _compiler()
ttlcode = __compiler.compilettl( file=%r )
_context = globals()['_context']
_context['_compiler'] = __compiler
_context['this'] = this
%s = __compiler.load( ttlcode, context=_context )\n
"""

interfaceClass = """\
from  %s import %s
class %s( BaseTTLPlugin ):
  implements(%s) 
"""

class InstrGen( object ):
    machname = '_m'

    def __init__( self, compiler ):
        self.compiler = compiler
        self._init()

    def _init( self ):
        self.outfd = StringIO()
        self.pyindent = ''
        self.optimaltext = []
        self.pytext = None

    def __call__( self ):
        return InstrGen( self.compiler )

    #---- API

    def initialize( self ):
        """Initialize and begin generating the intermediate python file."""
        self.outfd.write( import_header )
        self.cr()

    def cr( self, count=1 ):
        """Generate a new-line (along with current indentation level) in
        python generated text."""
        self.outfd.write( '\n'*count )
        self.outfd.write( self.pyindent )

    def codeindent( self, up=None, down=None, indent=True ):
        """Increase or decrease the python code-indentation for the
        intermediate text."""
        self.flushtext()
        if up != None :
            self.pyindent += up
        if down != None :
            self.pyindent = self.pyindent[:-len(down)]
        if indent : 
            self.outfd.write( self.pyindent )

    def codetext( self ):
        """Return the final text of python code."""
        return self.pytext

    #---- Instruction set

    def comment( self, comment, force=False ):
        """Optionally create a comment line inside the python code. Happens
        only when TTLCompiler['debug'] option is set true."""
        if self.compiler['debug'] or force :
            self.flushtext()
            self.outline( '# ' + ' '.join(comment.rstrip('\r\n').splitlines()) )

    def flushtext( self ):
        """:meth:`puttext` method's text string are not immediately appended
        to the stack buffer. They are accumulated and appended only when this
        method is called."""
        if self.optimaltext :
            self.outline( '_m.extend( %s )' % self.optimaltext )
            self.optimaltext = []

    def puttext( self, text, force=False ):
        """Append ``text`` into the stack machine."""
        self.optimaltext.append( text )
        self.flushtext() if force else None

    def putstatement( self, stmt ):
        """Add a python statement in the intermediate code."""
        self.flushtext()
        self.outline( stmt.rstrip('\r\n') )

    def putblock( self, codeblock, indent=True ):
        """Add a block of python statements in the intermediate code."""
        [ self.putstatement(line) for line in codeblock.splitlines() ]

    def evalexprs( self, s ):
        """Evaluate a string as python expression and append the result into
        the stack buffer."""
        try    : code, filts = s.split('|', 1)
        except : code, filts = s, ''
        code, filts = code.strip(), filts.strip()
        if code :
            self.flushtext()
            self.outline( 
                '_m.append(_m.evalexprs( %r, %r, globals(), locals()) )' % (
                        code, filts ))

    def pushbuf( self ):
        """Create a new buffer in the stack. The newly created buffer will
        start accumulated text string."""
        self.flushtext()
        self.outline( '_m.pushbuf()' )

    def popappend( self, astext=True ):
        """Pop the last buffer in the stack and append the text into the
        previous buffer in the stack."""
        self.flushtext()
        if astext == True :
            self.outline( '_m.append( _m.popbuftext() )' )
        else :
            self.outline( '_m.append( _m.popbuf() )' )

    def popreturn( self, astext=True ):
        """Pop the last buffer in the stack and return the text."""
        self.flushtext()
        if astext == True :
            self.outline( 'return _m.popbuftext()' )
        else :
            self.outline( 'return _m.popbuf()' )

    def handletag( self, indent=False, newline='' ):
        """Pop the last two buffers from the stack and supply them to
        :class:`ITayraTags` plugins. The returned HTML text from the plugin is
        only again pushed into the stack buffer."""
        self.flushtext()
        # first arg is `content` and second arg is `tag`
        self.outline(
          '_m.handletag( _m.popbuftext(), _m.popbuftext(), indent=%s, nl=%r)'\
                  % (indent, newline)
        )

    #---- Instructions to handle directives.

    def importttl( self, modname, ttlfile ):
        """Special method to handle @import directive."""
        lines = self.importtext % (ttlfile, modname)
        self.putblock( lines )

    def putinherit( self, ttlloc ):
        """Special method to handle @inherit directive."""
        self.outline( '_m.inherit( %r, globals() )' % ttlloc, )

    def implement_interface( self, implements, interfaces ):
        """Special method to handle @implement directive and @interface
        functions implementations."""
        interfaces_ = {}
        [ interfaces_.setdefault( ifname, [] ).append( methodname )
          for ifname, methodname in interfaces ]
        # Define interface class, hitch the methods and register the plugin
        for mod, ifname, pluginname in implements :
            # Define interface implementer class
            codeblock = interfaceClass % ( mod, ifname, pluginname, ifname )
            # hitch methods with interface class
            methods = interfaces_.get( ifname, [] )
            methodlines = [ '  %s = %s' % (meth, meth) for meth in methods ]
            self.putblock( '\n'.join( [codeblock] + methodlines ) )

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
        """Add the footer python code."""
        self.outline( footer % (ttlhash, ttlfile) )

    def finish( self ):
        """Call this when there is no more instruction to generate. Before
        calling this :meth:`footer` method must have been called."""
        self.pytext = self.outfd.getvalue()

    #-- Local methods

    def outline( self, line, count=1 ):
        self.cr( count=count )
        self.outfd.write( line )
