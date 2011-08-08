import time, codecs
from   os.path                  import dirname
from   copy                     import deepcopy

from   zope.component           import getGlobalSiteManager
import pkg_resources            as pkg

# Import tag-plugins so that they can register themselves.
import tayra.ttl.tags
import tayra.ttl.tags.html
import tayra.ttl.tags.customhtml
import tayra.ttl.tags.forms
# Import filterblock-plugins so that they can register themselves.
import tayra.ttl.filterblocks.pycode
# Import escapefilter-plugins so that they can register themselves.
import tayra.ttl.escfilters.common

from   tayra.ttl.interfaces     import ITayraTag, ITayraFilterBlock, \
                                       ITayraEscapeFilter
from   tayra.ttl.parser         import TTLParser

EP_TTLGROUP = 'tayra.ttlplugins'
EP_TTLNAME  = 'ITTLPlugin'
DEFAULT_ENCODING = 'utf-8'

defaultconfig = {
    # Development mode settings
    'devmod'            : True,
    'reload_templates'  : False,
    'debug_templates'   : False,
    # List of directories to look for the .ttl file
    'directories'       : '.',
    # path to store the compiled .py file (intermediate file)
    'module_directory'  : None,
    # CSV of escape filter names to be applied for expression substitution
    'escape_filters'    : '',
    # Default input endcoding for .ttl file.
    'input_encoding'    : DEFAULT_ENCODING,
    # Standard list of tag plugins to use
    'usetagplugins'     : 'html',
    # Don't bother about indentation for output html file
    'uglyhtml'          : False,
    # CSV list of plugin packages that needs to be imported, before compilation.
    'plugin_packages'   : '',
    # In memory cache for ttlfile to compiled python code
    'memcache'          : False,
}

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
    from tayra.ttl.compiler import Compiler
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

        # Load plugin packages
        packages = ttlconfig['plugin_packages']
        packages = filter(None, [ x.strip(' \t') for x in packages.split(',') ])
        [ __import__(pkg) for pkg in filter(None, packages) ]

        # Gather plugins template tag handlers, filter-blocks
        for x in gsm.registeredUtilities() :
            if x.provided == ITayraTag :           # Tag handlers
                tagplugins[x.name] = x.component
            if x.provided == ITayraFilterBlock :    # Filter blocks
                fbplugins[x.name] = x.component
            if x.provided == ITayraEscapeFilter :   # Escape Filters
                escfilters[x.name] = x.component
        ttlconfig['tagplugins'] = tagplugins
        ttlconfig['fbplugins'] = fbplugins
        ttlconfig['escfilters'] = escfilters

        # Load ttl files implementing template plugins
        [ _loadttls( ttllocs, ttlconfig ) for pkg, ttllocs in _findttls() ]

        # Setup ttlplugin lookup table
        for x in gsm.registeredUtilities() :
            # Skip plugins for tags, filters and filter-blocks
            if x.provided in [ ITayraTag, ITayraFilterBlock, ITayraEscapeFilter
               ] : continue
            z = ttlplugins.setdefault( x.provided, {} )
            z.setdefault( x.name, x.component )

    init_status = 'done'
    return ttlconfig

def queryTTLPlugin( interface, name='' ):
    if name :
        return ttlplugins[interface][name]
    else :
        return ttlplugins[interface].values()


#---- APIs for executing Tayra Template Language

class Renderer( object ):
    def __init__( self, ttlloc=None, ttltext=None, ttlconfig_={} ):
        """`ttlconfig` parameter will find its way into every object defined
        by the templating engine.
            TODO : somehow find a way to pass the arguments to `body` function
        """
        ttlconfig = deepcopy( defaultconfig )
        ttlconfig.update( ttlconfig_ )
        # Initialize plugins
        self.ttlconfig = initplugins( ttlconfig, force=ttlconfig['devmod'] )
        self.ttlloc, self.ttltext = ttlloc, ttltext
        self.ttlparser = TTLParser( ttlconfig=ttlconfig )

    def __call__( self, entryfn='body', context={} ):
        from tayra.ttl.compiler import Compiler
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
    from   tayra.ttl.compiler       import Compiler
    from   datetime                 import datetime as dt

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
    ttlparser = TTLParser( debug=debuglevel, ttlconfig=ttlconfig )
    comp = Compiler( ttlloc=ttlloc, ttlconfig=ttlconfig, ttlparser=ttlparser )
    pyfile = comp.ttlfile+'.py'
    htmlfile = comp.ttlfile.rsplit('.', 1)[0] + '.html'

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
        pytext = comp.topy()
        # Intermediate file should always be encoded in 'utf-8'
        codecs.open(pyfile, mode='w', encoding=DEFAULT_ENCODING).write(pytext)

        ttlconfig.setdefault( 'memcache', True )
        r = Renderer( ttlloc, ttlconfig )
        html = r( context=context )
        codecs.open( htmlfile, mode='w', encoding=encoding).write( html )

        # This is for measuring performance
        st = dt.now()
        [ r( context=context ) for i in range(10) ]
        print (dt.now() - st) / 10

