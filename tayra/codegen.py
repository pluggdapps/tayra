# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Instruction generator for :class:`tayra.runtime.StackMachine`. Generates
intermediate python file.
"""

from   io   import   StringIO

import_header = """\
import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin

"""

tb_decorator = """\
def __traceback_decorator__( frames ):
    from copy    import deepcopy
    from os.path import basename

    def _map2ttl( frame ):
        filename = frame.filename
        lineno = frame.lineno
        lines = open(filename).readlines()[:lineno]
        lines.reverse()
        rc = {}
        for l in lines :
            if l.strip().startswith('# lineno') :
                _, ttl_lineno = l.split(':', 1)
                ttl_lineno = int( ttl_lineno )
                ttl_text = open( _ttlfile ).readlines()[ ttl_lineno-1 ]
                return ttl_lineno, ttl_text
        return None, None

    newframes = []
    for frame in frames :
        newframes.append( frame )
        frameadded = getattr( frame, '_ttlframeadded', False )

        basen = basename( frame.filename )
        if basen.endswith( '.ttl.py' ) \
             and basen == (basename( _ttlfile ) + '.py') \
             and frameadded == False :
            newframe = deepcopy( frame )
            frame._ttlframeadded = True
            try :
                newframe.lineno, newframe.linetext = _map2ttl( newframe )
                if newframe.lineno :
                    newframe.filename = _ttlfile
                    newframes.append( newframe )
            except :
                raise
                continue
    return newframes
"""

footer = """\
"""

importtext = """\
_context = globals()['_context']
%s = _compiler.importlib(this, _context, %r)
"""

interfaceClass = """\
from  %s import %s
class %s( BaseTTLPlugin ):
  implements(%s) 
"""


class InstrGen( object ):
    """Instruction generator to compile template script to an intermediate
    python file. This file can be loaded as template module and executed in
    the context of a HTTP request to generate the final HTML response. Since
    creating an instance of this class every time can be a costly operation,
    create it once and use :meth:`_init` to initialize for subsequent uses.
    """

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
        """Initialize and begin generating the intermediate python file.
        Generates import statements and in debug mode generate trace-back
        generator.
        """
        self.outfd.write( import_header )
        if self.compiler['debug'] :
            self.outfd.write( tb_decorator )
        self.cr()

    def cr( self, count=1 ):
        """Generate a new-line (along with current indentation level) in
        python generated text.
        """
        self.outfd.write( '\n'*count )
        self.outfd.write( self.pyindent )

    def codeindent( self, up=None, down=None, indent=True ):
        """Increase or decrease python code-indentation for subsequently
        generated code."""
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
        name, s = s.split(' ',1) if s.startswith('-') else ('', s)
        name = name[1:] if name else name
        try    : text, filts = s.split('|', 1)
        except : text, filts = s, ''
        text, filts = text.strip(), filts.strip()
        if text :
            self.flushtext()
            self.outline(
            '_m.append(_m.evalexprs( %r, %r, %r, globals(), locals()) )' % (
                        name, text, filts )
            )

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

    def popobject( self, returnwith=None ):
        """Some times a function might want to return something else other
        than stacked buffers."""
        self.flushtext()
        if returnwith :
            # Discard the newest buffer in the stack
            self.outline( '_m.popbuf()' ) 
            self.outline( 'return ' + returnwith )
        else :
            self.outline( 'return _m.popobject()' )

    def handletag( self, **kwargs ):
        """Pop the last two buffers from the stack and supply them to
        :class:`ITayraTags` plugins. The returned HTML text from the plugin is
        only again pushed into the stack buffer."""
        self.flushtext()
        # first arg is `content` and second arg is `tag`
        self.outline(
          '_m.handletag( _m.popbuftext(), _m.popbuftext(), **%s )' % kwargs
        )

    #---- Instructions to handle directives.

    def importttl( self, modname, ttlfile ):
        """Special method to handle @import directive."""
        lines = importtext % (modname, ttlfile)
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
            methodlines = []
            for meth in methods :
                if meth == 'default_settings' :
                    methodlines.append( '  %s = classmethod(%s)'%(meth, meth) )
                else :
                    methodlines.append( '  %s = %s' % (meth, meth) )
            self.putblock( '\n'.join( [codeblock] + methodlines ) )

    #def useinterface( self, module, interfacename, pluginname, name ):
    #    line = 'from  %s import %s' % ( module, interfacename )
    #    self.putstatement(line)
    #    if isinstance(pluginname, tuple):
    #        line = '%s = _m.use( %s, _m.evalexprs(%s, %r) )' % (
    #                    name, interfacename, pluginname[0], pluginname[1] )
    #    else :
    #        line = '%s = _m.use( %s, %r )' % (name, interfacename, pluginname)
    #    self.putstatement(line)

    # TODO : Remove ttlhash and ttlfile.
    def footer( self, ttlhash, ttlfile ):
        """Add the footer python code."""
        self.outline( footer )

    def finish( self ):
        """Call this when there is no more instruction to generate. Before
        calling this :meth:`footer` method must have been called."""
        self.pytext = self.outfd.getvalue()

    #-- Local methods

    def outline( self, line, count=1 ):
        self.cr( count=count )
        self.outfd.write( line )
