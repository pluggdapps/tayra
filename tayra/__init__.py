# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

"""Package code handles following functions,

* Command script APIs for,
  * dump(), regenerate ttl text from its AST, formed by parsing the text.
  * show(), display AST in human readable form.
  * Compile .ttl file into .ttl.py file and finally generate the .html file.
* API for web frameworks to render tayra-templates.
* API to query TTLPlugins. Template plugins implemented using Tayra template
  language in .ttl files.
* Import modules implementing plugins, which are expected to be registered with
  global-site-manager by modules themselves.
* Define package version.
* Default configuration for template engine.
* Normalization function for configuration values.
* Plugin initialization, loading and setting-up tag-plugins, plugins defining
  escape filters (for expression substitution) and filter blocks.
* Find template plugins defined in setuptools packages, compile them and load
  them registering the Template plugins. queryTTLPlugin() works only after
  this phase is successfully completed.
"""

import codecs, re
from   os.path                  import dirname, basename, join
from   copy                     import deepcopy
from   datetime                 import datetime as dt

from   zope.component           import getGlobalSiteManager
import pkg_resources            as pkg

from   tayra.interfaces         import ITayraTag, ITayraFilterBlock, \
                                       ITayraEscapeFilter
from   tayra.utils              import ConfigDict, asbool, parsecsv
from   tayra.parser             import TTLParser
# Import tag-plugins so that they can register themselves.
import tayra.tags
import tayra.tags.html
import tayra.tags.forms
import tayra.tags.customhtml
# Import filterblock-plugins so that they can register themselves.
import tayra.filterblocks.pycode
# Import escapefilter-plugins so that they can register themselves.
import tayra.escfilters.common

__version__ = '0.1dev'

EP_TTLGROUP = 'tayra.plugins'
EP_TTLNAME  = 'ITTLPlugin'
DEFAULT_ENCODING = 'utf-8'
ESCFILTER_RE = re.compile( r'([a-zA-Z0-9_-]+)(\.[a-zA-Z0-9_.-]+)*,' )

defaultconfig = ConfigDict()
defaultconfig.__doc__ = """Configuration settings for tayra template engine."""
defaultconfig['parse_optimize']    = {
    'default' : True,
    'types'   : (bool,),
    'help'    : "PLY-Lexer-Yacc option. "
                "Set to False when you're modifying the lexer/parser. "
                "Otherwise, changes in the lexer/parser won't be used, "
                "if some lextab.py file exists. When releasing with a stable "
                "version, set to True to save the re-generation of the "
                "lexer/parser table on each run. Also note that, using "
                "python's optimization feature can break this option, refer, "
                "    http://www.dabeaz.com/ply/ply.html#ply_nn38 "
}
defaultconfig['lextab']    = {
    'default' : None,
    'types'   : (str,unicode),
    'help'    : "PLY-Lexer option. "
                "Points to the lex table that's used for optimized mode. Only "
                "if you're modifying the lexer and want some tests to avoid "
                "re-generating the table, make this point to a local lex table "
                "file. "
}
defaultconfig['yacctab']    = {
    'default' : None,
    'types'   : (str,unicode),
    'help'    : "PLY-Yacc option. "
                "Points to the yacc table that's used for optimized mode. Only "
                "if you're modifying the parser, make this point to a local "
                "yacc table file."
}
defaultconfig['strict_undefined']    = {
    'default' : False,
    'types'   : (bool,),
    'help'    : "Boolean to raise exception for un-defined context variables. "
                "If set to false, undefined variables will be silently "
                "digested as 'None' string. "
}
defaultconfig['directories']             = {
    'default' : '.',
    'types'   : ('csv', list),
    'help'    : "Comma seperated list of directory path to look for a "
                "template file. Default will be current-directory."
}
defaultconfig['module_directory']        = {
    'default' : None,
    'types'   : (str,),
    'help'    : "Directory path telling the compiler where to persist (cache) "
                "intermediate python file."
}
defaultconfig['escape_filters']          = {
    'default' : '',
    'types'   : ('csv', list),
    'help'    : "Comma seperated list of default escape filters to be applied "
                "during expression substitution."
}
defaultconfig['input_encoding']          = {
    'default' : 'utf-8',
    'types'   : (str,),
    'help'    : "Default input endcoding for .ttl file."
}
defaultconfig['usetagplugins']           = {
    'default' : ['html5', 'html5.forms'],
    'types'   : ('csv', list),
    'help'    : "Comma seperated list of tag plugin namespaces to use. Only "
                "plugins that are registered under the requested namespace will "
                "be used to generate the html."
}
defaultconfig['uglyhtml']                = {
    'default' : True,
    'types'   : (bool,),
    'help'    : "Boolean, to freely generate the output html file without "
                "bothering about indentation."
}
defaultconfig['plugin_packages']         = {
    'default' : '',
    'types'   : ('csv', list),
    'help'    : "Comma seperated list of plugin packages that needs to be "
                "imported, before compiling template files."
}
defaultconfig['memcache']                = {
    'default' : True,
    'types'   : (bool,),
    'help'    : "Cache the compiled python code in-memory to avoid "
                "re-compiling .ttl to .py file."
}
defaultconfig['text_as_hashkey']         = {
    'default' : False,
    'types'   : (bool,),
    'help'    : "To be used with 'memcache' option, where the cache tag "
                "will be computed using .ttl file's text content. This "
                "will have a small performance penalty instead of using "
                "template's filename as key."
}

def normalizeconfig( config ):
    """Convert string representation of config parameters into programmable
    data types. It is assumed that all config parameters are atleast initialized
    with default value.
    """
    config['devmod'] = asbool( config['devmod'] )
    config['strict_undefined'] = asbool( config['strict_undefined'] )
    config['module_directory'] = config['module_directory'] or None
    config['uglyhtml'] = asbool( config['uglyhtml'] )
    config['memcache'] = asbool( config['memcache'] )
    config['text_as_hashkey'] = asbool( config['text_as_hashkey'] )
    try    : config['directories'] = parsecsv( config['directories'] )
    except : pass
    try    :
        filters = ESCFILTER_RE.findall( config['escape_filters'].strip() + ',' )
        filters = [] if filters and filters[0][0] == 'n' else filters
        filters = [ ( f[0], f[1].strip('. ,') ) for f in filters if f ]
        config['escape_filters'] = filters
    except : pass
    try    : config['usetagplugins'] = parsecsv( config['usetagplugins'] )
    except : pass
    try    : config['plugin_packages'] = parsecsv( config['plugin_packages'] )
    except : pass
    return config


def _findttls():
    """Search for template plugins, and return a list of tuples,
    ( pkgname, list-of-ttl-files ).
    """
    packages = pkg.WorkingSet().by_key
    entrypoints = {}
    for pkgname, d in packages.items() :
        names = d.get_entry_map( group=EP_TTLGROUP )
        for name, entrypoint in names.items() :
            if name != EP_TTLNAME : continue
            try : ep = d.get_entry_info( EP_TTLGROUP, name )
            except : continue
            entrypoints.setdefault( pkgname, ep )
    return [ ( pkgname, ep.load()().implementers() )
             for pkgname, ep in entrypoints.items() ]


def _loadttls( ttllocs, ttlconfig, context={} ):
    """Only when the plugins are compile and loaded, it is available for rest
    of the system.
    """
    from tayra.compiler import Compiler
    [ Compiler( ttlloc=ttlloc, ttlconfig=ttlconfig ).execttl( context=context )
      for ttlloc in ttllocs ]


def initplugins( ttlconfig, force=False ):
    """Collect and organize Tayra template plugins, and plugins implementing
    language interfaces, like, ITayraTag, ITayraFilterBlock, ITayraEscapeFilter,

    Plugins are loaded and organised in the following format,
    `ttlplugins`,
        { interfaceName : {plugin-name: instance, ... }, ... }
    `tagplugins`,
        { plugin-name   : instance ... }
    `fbplugins`,
        { plugin-name   : instance ... }
    `escfilters`,
        { plugin-name   : instance ... }
        
    and also saved inside ttlconfig for further processing.
    """
    ttlplugins = {}
    tagplugins = {}
    fbplugins  = {}
    escfilters = {}

    if (force == True) or ttlconfig.get( 'tagplugins', None ) == None :
        # Load and classify plugins
        gsm = getGlobalSiteManager()
        usetagplugins = ttlconfig['usetagplugins'] + [u'']

        # import plugin packages defined in `ttlconfig`
        packages = ttlconfig['plugin_packages']
        if isinstance( packages, basestring ):
            packages = [ x.strip(' \t') for x in packages.split(',') ]
        [ __import__(pkg) for pkg in filter(None, packages) ]

        # Gather plugins template tag handlers, filter-blocks
        for x in gsm.registeredUtilities() :
            if x.provided == ITayraTag :            # Tag handlers
                try    : namespace, tagname = x.name.rsplit('.', 1)
                except : namespace, tagname = u'', x.name
                if namespace in usetagplugins :
                    tagplugins[tagname] = x.component
            elif x.provided == ITayraFilterBlock :    # Filter blocks
                fbplugins[x.name] = x.component
            elif x.provided == ITayraEscapeFilter :   # Escape Filters
                escfilters[x.name] = x.component
            else :
                continue
            if not hasattr( x.component, 'pluginname' ) :
                raise Exception(
                    '%r plugin must have `pluginname` attribute' % x.component
                )

        ttlconfig['tagplugins'] = tagplugins
        ttlconfig['fbplugins'] = fbplugins
        ttlconfig['escfilters'] = escfilters

        # Load ttl files implementing template plugins
        [ _loadttls( ttllocs, ttlconfig ) for pkg, ttllocs in _findttls() ]

        # Setup ttlplugin lookup table
        for x in gsm.registeredUtilities() :
            # Skip plugins for tags, filters and filter-blocks
            if getattr( x.component, 'itype', None ) == 'ttlplugin' :
                z = ttlplugins.setdefault( x.provided, {} )
                z.setdefault( x.name, x.component )
        ttlconfig['ttlplugins'] = ttlplugins
    return ttlconfig


def queryTTLPlugin( ttlplugins, interface, name, *args, **kwargs ):
    """Query for template plugins providing ``interface`` and registered
    under ``name``. If ``name`` is None, then a list of plugins providing
    (a.k.a implementing) the ``interface`` will be returned. If __call__
    method is defined by the template plugin component, a new clone of it
    will be created by calling the component with ``args`` and ``kwargs``.
    """
    iface = ttlplugins.get( interface, None )
    if iface == None : return None

    if name :
        p = iface.get( name, None )
        return p( *args, **kwargs ) if p and callable(p) else p
    else :
        return map( lambda p : p(*args, **kwargs) if callable(p) else p,
                    iface.values() )


class BaseTTLPlugin( object ):
    """Base class for all plugins implementing one or more template
    interfaces."""
    def __init__( self, *args, **kwargs ):
        self.args = args
        self.kwargs = kwargs

    def __call__( self, *args, **kwargs ):
        return self.__class__( *args, **kwargs )


#---- APIs for executing Tayra Template Language

class Renderer( object ):
    """Render a template into HTML.

    `ttlconfig` parameter will find its way into every object defined
    by the templating engine.

    """
    def __init__( self, ttlloc=None, ttltext=None, ttlconfig={} ):
        ttlconfig = ttlconfig or deepcopy( dict(defaultconfig.items()) )
        # Initialize plugins
        self.ttlconfig = initplugins( ttlconfig, force=ttlconfig['devmod'] )
        self.ttlloc, self.ttltext = ttlloc, ttltext
        self.ttlparser = TTLParser( ttlconfig=self.ttlconfig )

    def __call__( self, entryfn='body', context={} ):
        """Compile, execute and return html text corresponding the template
        document.

        key-word arguments,
        ``entryfn``,
            name of entry function to be called.
        ``context``,
            dictionary of key,value pairs to be used as context for generating
            html document.

        Arguments to body() function can be passed via context variables,
        ``_bodyargs`` (a list of positional arguments) and ``_bodykwargs`` a
        dictionary of key-word arguments.

        dictionary object ``context`` will also be available as _ttlcontext
        variable.
        """
        from tayra.compiler import Compiler
        self.compiler = Compiler( ttltext=self.ttltext,
                                  ttlloc=self.ttlloc,
                                  ttlconfig=self.ttlconfig,
                                  ttlparser=self.ttlparser
                                )
        context['_ttlcontext'] = context
        module = self.compiler.execttl( context=context )
        # Fetch parent-most module
        entry = getattr( module.self, entryfn )
        args = context.get( '_bodyargs', [] )
        kwargs = context.get( '_bodykwargs', {} )
        html = entry( *args, **kwargs ) if callable( entry ) else u''
        return html

def ttl_cmdline( ttlloc, **kwargs ):
    from   tayra.compiler       import Compiler

    ttlconfig = deepcopy( dict( defaultconfig.items() ))
    # directories, module_directory, devmod
    ttlconfig.update( kwargs )
    ttlconfig.setdefault( 'module_directory', dirname( ttlloc ))

    # Parse command line arguments and configuration
    args = eval( ttlconfig.pop( 'args', '[]' ))
    context = ttlconfig.pop( 'context', {} )
    context = eval(context) if isinstance(context, basestring) else context
    context.update( _bodyargs=args ) if args else None
    debuglevel = ttlconfig.pop( 'debuglevel', 0 )
    show = ttlconfig.pop( 'show', False )
    dump = ttlconfig.pop( 'dump', False )
    encoding = ttlconfig['input_encoding']

    # Initialize plugins
    ttlconfig = initplugins( ttlconfig, force=ttlconfig['devmod'] )

    # Setup parser
    ttlparser = TTLParser(
            ttlconfig=ttlconfig, debug=debuglevel )
    comp = Compiler( ttlloc=ttlloc, ttlconfig=ttlconfig, ttlparser=ttlparser )
    pyfile = comp.ttlfile+'.py'
    htmlfile = basename( comp.ttlfile ).rsplit('.', 1)[0] + '.html'
    htmlfile = join( dirname(comp.ttlfile), htmlfile )

    if debuglevel :
        print "AST tree ..."
        tu = comp.toast()
    elif show :
        print "AST tree ..."
        tu = comp.toast()
        tu.show()
    elif dump :
        tu = comp.toast()
        rctext =  tu.dump()
        if rctext != codecs.open( comp.ttlfile, encoding=encoding ).read() :
            print "Mismatch ..."
        else : print "Success ..."
    else :
        print "Generating py / html file ... "
        pytext = comp.topy( ttlhash=comp.ttllookup.ttlhash )
        # Intermediate file should always be encoded in 'utf-8'
        codecs.open(pyfile, mode='w', encoding=DEFAULT_ENCODING).write(pytext)

        ttlconfig.setdefault( 'memcache', True )
        r = Renderer( ttlloc=ttlloc, ttlconfig=ttlconfig )
        html = r( context=context )
        codecs.open( htmlfile, mode='w', encoding=encoding).write( html )

        # This is for measuring performance
        st = dt.now()
        [ r( context=context ) for i in range(2) ]
        print (dt.now() - st) / 2
