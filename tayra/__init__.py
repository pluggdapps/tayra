import time, codecs
from   os.path                  import dirname, basename, join
from   copy                     import deepcopy
from   datetime                 import datetime as dt

from   zope.component           import getGlobalSiteManager
import pkg_resources            as pkg
from   paste.util.converters    import asbool

# Import tag-plugins so that they can register themselves.
import tayra.tags
import tayra.tags.html
import tayra.tags.forms
import tayra.tags.customhtml
# Import filterblock-plugins so that they can register themselves.
import tayra.filterblocks.pycode
# Import escapefilter-plugins so that they can register themselves.
import tayra.escfilters.common

from   tayra.interfaces         import ITayraTag, ITayraFilterBlock, \
                                       ITayraEscapeFilter
from   tayra.parser             import TTLParser

__version__ = '0.1dev'

EP_TTLGROUP = 'tayra.ttlplugins'
EP_TTLNAME  = 'ITTLPlugin'
DEFAULT_ENCODING = 'utf-8'

defaultconfig = {
    # Development mode settings
    'devmod'            : True,
    'strict_undefined'  : False,
    # List of directories to look for the .ttl file
    'directories'       : '.',
    # path to store the compiled .py file (intermediate file)
    'module_directory'  : None,
    # CSV of escape filter names to be applied for expression substitution
    'escape_filters'    : '',
    # Default input endcoding for .ttl file.
    'input_encoding'    : DEFAULT_ENCODING,
    # Standard list of tag plugins to use
    'usetagplugins'     : 'html5, html5.forms',
    # Don't bother about indentation for output html file
    'uglyhtml'          : True,
    # CSV list of plugin packages that needs to be imported, before compilation.
    'plugin_packages'   : '',
    # In memory cache for compiled ttlfile
    'memcache'          : True,
    'text_as_hashkey'   : False,
}

def normalizeconfig( config ):
    """Convert the string representation of config parameters into
    programmable types. It is assumed that all config parameters are atleast
    initialized with default value.
    """
    config['devmod'] = asbool( config['devmod'] )
    config['strict_undefined'] = asbool( config['strict_undefined'] )
    try :
        config['directories'] = [
            x.strip() for x in config['directories'].split(',') if x.strip()
        ]
    except :
        pass
    config['module_directory'] = config['module_directory'] or None
    try :
        config['escape_filters'] = [
            x.strip() for x in config['escape_filters'].split(',') if x.strip()
        ]
    except :
        pass
    try :
        config['usetagplugins'] = [
            x.strip() for x in config['usetagplugins'].split(',') if x.strip()
        ]
    except :
        pass
    config['uglyhtml'] = asbool( config['uglyhtml'] )
    try :
        config['plugin_packages'] = [
            x.strip() for x in config['plugin_packages'].split(',') if x.strip()
        ]
    except :
        pass
    config['memcache'] = asbool( config['memcache'] )
    config['text_as_hashkey'] = asbool( config['text_as_hashkey'] )
    return config


def _findttls():
    """Search for tayra template plugins."""
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

ttlplugins = {}         # { interfaceName : {plugin-name: instance, ... }, ... }
tagplugins = {}         # { plugin-name   : (instance, hander-dict), ... }
fbplugins  = {}         # { plugin-name   : instance }
escfilters = {}         # { plugin-name   : instance }
init_status = 'pending'
def initplugins( ttlconfig, force=False ):
    """Collect and organize Tayra template plugins including, plugins for
    interfaces,
        ITayraTag, ITayraFilterBlock, ITayraEscapeFilter
    """

    global ttlplugins, tagplugins, init_status
    if init_status == 'progress' :
        return ttlconfig

    if (force == True) or ttlconfig.get( 'tagplugins', None ) == None :
        # Load and classify plugins
        init_status = 'progress'
        gsm = getGlobalSiteManager()
        usetagplugins = ttlconfig['usetagplugins']

        # Load plugin packages
        packages = ttlconfig['plugin_packages']
        if isinstance( packages, basestring ):
            packages = [ x.strip(' \t') for x in packages.split(',') ]
        [ __import__(pkg) for pkg in filter(None, packages) ]

        # Gather plugins template tag handlers, filter-blocks
        for x in gsm.registeredUtilities() :
            if x.provided == ITayraTag :            # Tag handlers
                try    : namespace, tagname = x.name.rsplit('.', 1)
                except : namespace, tagname = '', x.name
                if namespace in usetagplugins:
                    tagplugins[tagname] = x.component
                elif namespace == '' :
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

    init_status = 'done'
    return ttlconfig


def queryTTLPlugin( interface, name, *args, **kwargs ):
    foriface = ttlplugins.get( interface, None )
    if foriface == None : return None

    if name :
        p = foriface.get( name, None )
        return p( *args, **kwargs ) if p and callable(p) else p
    else :
        return map( lambda p : p(*args, **kwargs) if callable(p) else p,
                    foriface.values() )


class BaseTTLPlugin( object ):
    def __init__( self, *args, **kwargs ):
        self.args = args
        self.kwargs = kwargs

    def __call__( self, *args, **kwargs ):
        return self.__class__( *args, **kwargs )


#---- APIs for executing Tayra Template Language

class Renderer( object ):
    def __init__( self, ttlloc=None, ttltext=None, ttlconfig={} ):
        """`ttlconfig` parameter will find its way into every object defined
        by the templating engine.
            TODO : somehow find a way to pass the arguments to `body` function
        """
        ttlconfig_ = deepcopy( defaultconfig )
        ttlconfig_.update( ttlconfig )
        # Initialize plugins
        self.ttlconfig = initplugins( ttlconfig_, force=ttlconfig_['devmod'] )
        self.ttlloc, self.ttltext = ttlloc, ttltext
        self.ttlparser = TTLParser( ttlconfig=self.ttlconfig )

    def __call__( self, entryfn='body', context={} ):
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
        # TODO : Optionally translate the return string into unicode
        html = entry() if callable( entry ) else ''
        return html

def ttl_cmdline( ttlloc, **kwargs ):
    from   tayra.compiler       import Compiler

    ttlconfig = deepcopy( defaultconfig )
    # directories, module_directory, devmod
    ttlconfig.update( kwargs )
    ttlconfig.setdefault( 'module_directory', dirname( ttlloc ))

    # Parse command line arguments and configuration
    args = eval( ttlconfig.pop( 'args', '[]' ))
    context = eval( ttlconfig.pop( 'context', '{}' ))
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

