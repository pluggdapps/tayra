# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Tayra Compiler implemented as plugin. It also implements pluggapps' web
interface :class:`ITemplate`.
"""

import imp, os, re, sys, os.path
from   os.path              import isfile, basename, join, isdir, dirname
from   hashlib              import sha1

from   pluggdapps.plugin        import Plugin, implements, ISettings
import pluggdapps.utils         as h
from   pluggdapps.interfaces    import ITemplate

import tayra.utils

class TTLCompiler( Plugin ):
    """Tayra compiler. Implemented as plugin to leverage on pluggdapps
    configuration system. Also implement :class:`ITemplate`. Creating a
    plugin instance can be a costly operation, to avoid this instantiate this
    plugin once and use :meth:`_init` to initialize it for subsequent uses.
   """

    implements( ITemplate )

    _memcache = {}

    ttlloc = None
    """TemplateLookup object. Encapsulates location information for template
    file and its intermediate python file."""

    ttlfile = ''
    """Absolute file path pointing to .ttl template script file in."""

    ttltext = ''
    """String of template script either read from the template file or
    received directly."""

    pyfile = ''
    """If present, absolute file path pointing to compiled template script,
    .py file."""

    pytext = ''
    """String of python script translated from template script."""

    encoding = ''
    """Character encoding of original template script file."""

    ttlparser = None
    """:class:`tayra.parser.TTLParser` object."""

    igen = None
    """:class:`tayra.codegen.InstrGen` object."""

    mach = None
    """:class:`tayra.runtime.StackMachine` object."""

    def __init__( self ):
        from tayra.parser   import TTLParser
        from tayra.codegen  import InstrGen
        from tayra.runtime  import StackMachine
        
        self.ttlparser = TTLParser( self )
        self.igen = InstrGen( self )
        self.mach = StackMachine( self ) # Stack machine

    def __call__( self, **kwargs ):
        """Clone a plugin with the same settings as this one. settings can
        also be overriden by passing ``settings`` key-word argument as a
        dictionary."""
        settings = {}
        settings.update({ k : self[k] for k in self })
        settings.update( kwargs.pop( 'settings', {} ))
        kwargs['settings'] = settings
        return self.qp( ISettings, 'tayra.ttlcompiler', **kwargs )

    def _init( self, file=None, text=None ):
        """Reinitialize the compiler object to compile a different template
        script."""
        from pluggdapps import papackages
        self.ttlloc = TemplateLookup( self, file, text )
        self.encoding = self.ttlloc.encoding
        self.ttlfile = self.ttlloc.ttlfile
        self.ttltext = self.ttlloc.ttltext
        self.pyfile = self.ttlloc.pyfile
        
        # Compute the module name from ttlfile.
        asset = h.asset_spec_from_abspath( self.ttlfile, papackages )
        if asset :
            n = '.'.join(asset.split(':', 1)[1].split( os.path.sep ))
            self.modulename = n[:-4] if n.endswith('.ttl') else n
        else :
            n = '.'.join(self.ttlfile.split( os.path.sep ))
            self.modulename = n[:-4] if n.endswith('.ttl') else n

        self.mach._init( self.ttlfile )
        self.igen._init()

        # Check whether pyfile is older than the ttl file. In debug mode is is
        # always re-generated.
        self.pytext = ''
        if self['debug'] == False :
            if self.ttlfile and isfile( self.ttlfile ) :
                if self.pyfile and isfile( self.pyfile ) :
                    m1 = os.stat( self.ttlfile ).st_mtime
                    m2 = os.stat( self.pyfile ).st_mtime
                    if m1 <= m2 :
                        self.pytext = open( self.pyfile ).read()

    def toast( self, ttltext=None ):
        """Convert template text into abstract-syntax-tree. Return the root
        node :class:`tayra.ast.Template`."""
        ttltext = ttltext or self.ttltext
        self.ast = self.ttlparser.parse( ttltext, ttlfile=self.ttlfile )
        return self.ast

    def topy( self, ast, *args, **kwargs ):
        """Generate intermediate python text from ``ast`` obtained from
        :meth:`toast` method. If configuration settings allow for persisting
        the generated python text, then this method will save the intermediate
        python text in file pointed by :attr:`pyfile`."""
        ast.validate()
        ast.headpass1( self.igen )                   # Head pass, phase 1
        ast.headpass2( self.igen )                   # Head pass, phase 2
        ast.generate( self.igen, *args, **kwargs )   # Generation
        ast.tailpass( self.igen )                    # Tail pass
        pytext = self.igen.codetext()
        if self.pyfile and isdir( dirname( self.pyfile )) :
            open( self.pyfile, 'w', encoding='utf-8' ).write( pytext )
        return pytext

    def compilettl( self, file=None, text=None, args=[], kwargs={} ):
        """Translate a template script text or template script file into 
        intermediate python text. Compile the python text and return the code
        object. If ``memcache`` configuration is enable, compile code is
        cached in memory using a hash value generated from template text.
        
        ``args`` and ``kwargs``,
            position arguments and keyword arguments to use during
            AST.generate() pass.
        """
        self._init( file=file, text=text ) if (file or text) else None
        code = self._memcache.get( self.ttlloc.ttlhash, None )
        if not code :
            if not self.pytext :
                self.pytext = self.topy( self.toast(), *args, **kwargs )
            code = compile( self.pytext, self.pyfile, 'exec' )
        if self['memcache'] :
            self._memcache.setdefault( self.ttlloc.ttlhash, code )
        return code

    def load( self, code, context={} ):
        """Using an optional ``context``, a dictionary of key-value pairs, and
        the code object obtained from :meth:`compilettl` method, create a new
        module instance populating it with ``context`` and some standard
        references."""
        from   tayra.runtime import Namespace
        import tayra.h       as tmplh

        # Module instance for the ttl file
        module = imp.new_module( self.modulename )
        ctxt = {
            self.igen.machname : self.mach,
            '_compiler'   : self,
            'this'        : Namespace( None, module ),
            'local'       : module,
            'parent'      : None,
            'next'        : None,
            'h'           : tmplh,
            '__file__'    : self.pyfile,
            '_ttlfile'    : self.ttlfile,
            '_ttlhash'    : self.ttlloc.ttlhash,
        }
        ctxt.update( context )
        ctxt['_context'] = ctxt
        module.__dict__.update( ctxt )
        # Execute the code in module's context
        sys.modules.setdefault( self.modulename, module )
        exec( code, module.__dict__, module.__dict__ )
        return module

    def generatehtml( self, module, context={} ):
        """Using the ``module`` object obtained from :meth:`load` method, and
        a context dictionary, call the template module's entry point to 
        generate HTMl text and return the same.
        """
        try :
            entry = getattr( module.this, self['entry_function'] )
            args = context.get( '_bodyargs', [] )
            kwargs = context.get( '_bodykwargs', {} )
            html = entry( *args, **kwargs ) if callable( entry ) else ''
            try :
                from bs4 import BeautifulSoup
                if self['beautify_html'] :
                    html = BeautifulSoup( html ).prettify()
            except :
                pass
            return html
        except :
            if self['debug'] : raise
            return ''

    def importlib(self, this, context, file):
        """Import library ttl files inside the main script's context"""
        compiler = self()
        context['_compiler'] = compiler
        context['this'] = this
        return compiler.load( compiler.compilettl(file=file), context=context )
        

    #---- ITemplate interface methods

    def render( self, context, **kwargs ):
        """:meth:`pluggdapps.interfaces.ITemplate.render` interface 
        method. Generate HTML string from template script passed either via 
        ``ttext`` or via ``tfile``.

        ``tfile``,
            Location of Tayra template file, either as relative directory or as
            asset specification.

        ``ttext``,
            Tayra template text string.
        """
        file, text = kwargs.get('file', None), kwargs.get('text', None)
        code = self.compilettl( file=file, text=text )
        module = self.load( code, context=context )
        html = self.generatehtml( module, context )
        return html

    #---- ISettings interface methods

    @classmethod
    def default_settings( cls ):
        """:meth:`pluggdapps.plugin.ISettings.default_settings` interface 
        method."""
        return _defaultsettings

    @classmethod
    def normalize_settings( cls, sett ):
        """:meth:`pluggdapps.plugin.ISettings.normalize_settings` interface 
        method."""
        sett['nocache'] = h.asbool( sett['nocache'] )
        sett['optimize'] = h.asint( sett['optimize'] )
        sett['lex_debug'] = h.asint( sett['lex_debug'] )
        sett['yacc_debug'] = h.asint( sett['yacc_debug'] )
        sett['strict_undefined'] = h.asbool( sett['strict_undefined'] )
        sett['directories'] = h.parsecsvlines( sett['directories'] )
        sett['tag.plugins'] = h.parsecsvlines( sett['tag.plugins'] )
        sett['beautify_html'] = h.asbool( sett['beautify_html'] )
        sett['memcache'] = h.asbool( sett['memcache'] )
        return sett


_defaultsettings = h.ConfigDict()
_defaultsettings.__doc__ = TTLCompiler.__doc__

#---- PLY options.
_defaultsettings['optimize']    = {
    'default' : 1,
    'types'   : int,
    'help'    : "PLY Lexer/Yaccer option. "
                "For improved performance, it may be desirable to use Python's "
                "optimized mode (e.g., running Python with the -O option). "
                "However, doing so causes Python to ignore documentation "
                "strings. This presents special problems for lexer and parser. "
                "To handle this case, you can set this parameter to ``1``. For "
                "more information refer, "
                " http://www.dabeaz.com/ply/ply.html#ply_nn15."
}
_defaultsettings['lextab']    = {
    'default' : 'lextyrtab',
    'types'   : (str,),
    'help'    : "PLY-Lexer option. "
                "Points to the lex table that's used for optimized mode. Only "
                "if you're modifying the lexer and want some tests to avoid "
                "re-generating the table, make this point to a local lex table "
                "file. "
}
_defaultsettings['lex_debug'] = {
    'default' : 0,
    'types'   : (int,),
    'help'    : "PLY-Lex option. Run lexer in debug mode."
}
_defaultsettings['yacctab']    = {
    'default' : 'parsetyrtab',
    'types'   : (str,),
    'help'    : "PLY-Yacc option. "
                "Points to the yacc table that's used for optimized mode. Only "
                "if you're modifying the parser, make this point to a local "
                "yacc table file."
}
_defaultsettings['yacc_debug'] = {
    'default' : 0,
    'types'   : (int,),
    'help'    : "PLY-Yacc option. Run yaccer in debug mode."
}
_defaultsettings['yacc_outputdir'] = {
    'default' : '',
    'types'   : (str,),
    'help'    : "To change the directory in which the PLY YACC's parsetab.py "
                "file (and other output files) are written."
}

#----
_defaultsettings['encoding']             = {
    'default' : 'utf-8-sig',
    'types'   : (str,),
    'help'    : "Encoding to use while reading the template script file."
}
_defaultsettings['strict_undefined']    = {
    'default' : False,
    'types'   : (bool,),
    'help'    : "Boolean to raise exception for undefined context variables. "
                "If set to false, undefined variables will be silently "
                "digested as 'None' string. "
}
_defaultsettings['directories']             = {
    'default' : '.',
    'types'   : ('csv',list),
    'help'    : "Comma separated list of directory path to look for a "
                "template file. Default will be current-directory."
}
_defaultsettings['cache_directory']        = {
    'default' : '',
    'types'   : (str,),
    'help'    : "Directory path telling the compiler where to persist (cache) "
                "intermediate python file."
}
_defaultsettings['nocache'] = {
    'default' : False,
    'types'   : (bool,),
    'help'    : "If set to True, will not persist the intermediate python "
                "file."
}
_defaultsettings['expression.default']          = {
    'default' : 'tayra.ExpressionPy',
    'types'   : (str,),
    'help'    : "Default plugin to use for evaluating text in expression "
                "substitution. This plugin will be used if filter() call"
                "fails in other ITayraExpression plugins."
}
_defaultsettings['tag.plugins']           = {
    'default' : 'tayra.HTML5Forms, tayra.HTML5, tayra.Tags',
    'types'   : ('csv', list),
    'help'    : "Comma separated list of tag plugins to use. Plugins in the "
                "specified order will be invoked to handle the template tags, "
                "so the order of the plugin is important."
}
_defaultsettings['input_encoding']          = {
    'default' : 'utf-8-sig',
    'types'   : (str,),
    'help'    : "Default input encoding for .ttl file."
}
_defaultsettings['beautify_html']                = {
    'default' : True,
    'types'   : (bool,),
    'help'    : "Boolean, if True will generate human readable html output. "
                "Make sure that BeautifulSoup, beautifulsoup4, is "
                "installed. Do not enable this in production mode, might "
                "slow down the web page."
}
_defaultsettings['memcache']                = {
    'default' : True,
    'types'   : (bool,),
    'help'    : "Cache the compiled python code in-memory to avoid "
                "re-compiling .ttl to .py file."
}
_defaultsettings['entry_function']  = {
    'default'  : 'body',
    'types'    : (str,),
    'help'     : "Entry point, function in python module, into compiled "
                 "template script."
}


class TemplateLookup( object ) :
    """Lookup template file, template text, intermediate python file."""

    ttlfile = ''
    """Absolute file path pointing to .ttl template script file in."""

    ttltext = ''
    """String of template script either read from the template file or
    received directly."""

    pyfile = ''
    """Absolute file path pointing to compiled template script, .py file."""

    encoding = ''
    """Character encoding of original template script file."""

    ttlhash = ''
    """Hash value generated from template text."""

    def __init__( self, compiler, ttlloc=None, ttltext=None ):
        self.compiler = compiler

        if ttlloc :
            ttlfile = h.abspath_from_asset_spec( ttlloc )
            cachedir = compiler['cache_directory']
            self.encoding = self.charset( ttlfile=ttlfile,
                                          encoding=compiler['encoding'] )
            if compiler['nocache'] :
                self.pyfile = '<Source provided directly as text>'

            elif cachedir :
                if not isdir( cachedir ):
                    compiler.pa.logdebug(
                            "Creating cache directory %r " % cachedir )
                    os.makedirs( cachedir, exist_ok=True )
                self.pyfile = join( cachedir, ttlloc+'.py' )
                if not isfile( self.pyfile ):
                    os.makedirs( dirname( self.pyfile ), exist_ok=True )
            else :
                self.pyfile = ttlfile + '.py'

            self.ttlfile = h.locatefile( ttlfile, compiler['directories'] )
            self.ttltext = open( self.ttlfile, encoding=self.encoding ).read()

            # If reloading is available from the platform do so.
            try :
                if compiler['debug'] and isfile( ttlfile ) :
                    compiler.pa._monitoredfiles.append(tttllfile)
            except :
                pass

        elif ttltext :
            parselines = ttltext.encode('utf-8').splitlines()
            self.encoding = self.charset( parselines=parselines,
                                          encoding=compiler['encoding'] )
            self.pyfile = '<Source provided directly as text>'
            self.ttlfile = '<Source provided directly as text>'
            self.ttltext = ttltext.decode( self.encoding ) \
                                if isinstance( ttltext, bytes ) else ttltext

        else :
            raise Exception( 'Invalid ttl source !!' )

            return self._ttlhash

    def charset( self, ttlfile=None, parselines=None, encoding=None ):
        """Charset must come as parameter specifier for @doctype directive
        in the beginning of the Tayra template script. Parse the script for
        the directive and return the encoding string.  Returns encoding string
        or byte-string.

        ``ttlfile``,
            Template script file.

        ``parseline``,
            A line of string or byte-string specifying the @doctype directive.
        """
        parselines = parselines or open( ttlfile, 'rb' ).readlines()
        parseline = None
        for line in parselines :
            line = line.strip()
            if line.startswith( b'@doctype' ) :
                parseline = line
                break
            if line.startswith( b'<' ) :
                break
        if parseline :
            m = re.search( b'charset="([^"]+")', parseline[8:] )
            encoding = m.groups()[0].decode('utf-8') if m else encoding
        return encoding

    def _get_ttlhash( self ):
        return sha1( self.ttltext.encode('utf-8') ).hexdigest()

    ttlhash = property( _get_ttlhash )

