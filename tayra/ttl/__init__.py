import time, imp
from   StringIO                 import StringIO
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
    'directories' : [],
    'module_directory' : None,
    'default_filters' : None,
    'imports' : None,
    'strict_undefined' : False,
    'devmod': True,
    'reload_templates': False,
    'debug_templates': False,
    'input_encoding': 'utf-8',
    'usetagplugins' : [ 'html' ],
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
    from   tayra.ttl.compiler       import Compiler, TemplateLookup
    [ Compiler( TemplateLookup( ttlloc, ttlconfig ), ttlconfig=ttlconfig 
              ).execttl( context=context )
      for ttlloc in ttllocs ]

ttlplugins = {}         # { interfaceName : {plugin-name: instance, ... }, ... }
tagplugins = {}         # { plugin-name   : (instance, hander-dict), ... }
fbplugins  = {}         # { plugin-name   : instance }
escfilters = {}         # { plugin-name   : instance }
init_status = 'pending'
def initplugins( ttlconfig, force=False ):
    """Collect and organize Tayra template plugins including, plugins for
    interfaces,
        ITayraTag, ITayraFilterBlock, ITayraEscapeFilter"""

    global ttlplugins, tagplugins, init_status
    if init_status == 'progress' :
        return ttlconfig

    if (force == True) or ttlconfig.get( 'tagplugins', None ) == None :
        # Load and classify plugins
        init_status = 'progress'
        gsm = getGlobalSiteManager()

        # Load plugin packages
        packages = ttlconfig.get( 'plugin_packages', '' )
        packages = [ x.strip(' \t') for x in packages.split(',') ]
        [ __import__(pkg) for pkg in filter(None, packages) ]

        # Gather plugins template tag handlers, filter-blocks
        for x in gsm.registeredUtilities() :
            if x.provided == ITayraTag :           # Tag handlers
                tagplugins[x.name] = x.component
                ttlconfig['tagplugins'] = tagplugins
            if x.provided == ITayraFilterBlock :    # Filter blocks
                fbplugins[x.name] = x.component
                ttlconfig['fbplugins'] = fbplugins
            if x.provided == ITayraEscapeFilter :   # Escape Filters
                escfilters[x.name] = x.component
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
    def __init__( self, ttlloc, ttlconfig_ ):
        """`ttlconfig` parameter will find its way into every object defined
        by the templating engine.
        TODO : somehow find a way to pass the arguments to `body` function
        """
        ttlconfig = deepcopy( defaultconfig )
        ttlconfig.update( ttlconfig_ )
        # Initialize plugins
        self.ttlconfig = initplugins(
                ttlconfig, force=ttlconfig.get('devmod', True)
        )
        self.ttlloc = ttlloc
        self.ttlparser = TTLParser( ttlconfig=ttlconfig )

    def __call__( self, entry=None, context={} ):
        from   tayra.ttl.compiler       import Compiler, TemplateLookup
        self.compiler = Compiler(
            self.ttlloc, ttlconfig=self.ttlconfig, ttlparser=self.ttlparser
        )
        context['_ttlcontext'] = context
        module = self.compiler.execttl( context=context )
        # Fetch parent-most module
        entry = getattr( module.self, entry or 'body' )
        # TODO : Optionally translate the return string into unicode
        html = entry() if callable( entry ) else ''
        return html

def ttl_cmdline( ttlloc, **kwargs ):
    from   tayra.ttl.compiler       import Compiler, TemplateLookup
    from   datetime                 import datetime as dt

    # Parse command line arguments
    args = eval( kwargs.pop( 'args', '[]' ))
    context = eval( kwargs.pop( 'context', '{}' ))
    debuglevel = kwargs.pop( 'debuglevel', 0 )
    show = kwargs.pop( 'show', False )
    dump = kwargs.pop( 'dump', False )
    ttlconfig = deepcopy( defaultconfig )
    # directories, module_directory, devmod
    ttlconfig.update( kwargs )
    ttlconfig.setdefault( 'module_directory', dirname( ttlloc ))

    # Initialize plugins
    ttlconfig = initplugins( ttlconfig, force=ttlconfig.get('devmod', True) )

    # Setup parser
    ttlparser = TTLParser( debug=debuglevel, ttlconfig=ttlconfig )
    compiler = Compiler( ttlloc, ttlconfig=ttlconfig, ttlparser=ttlparser )
    pyfile = compiler.ttlfile+'.py'
    htmlfile = compiler.ttlfile.rsplit('.', 1)[0] + '.html'

    if debuglevel :
        print "AST tree ..."
        tu = compiler.toast()
    elif show :
        print "AST tree ..."
        tu = compiler.toast()
        tu.show()
    elif dump :
        tu = compiler.toast()
        rctext =  tu.dump()
        if rctext != open( compiler.ttlfile ).read() : print "Mismatch ..."
        else : print "Success ..."
    else :
        print "Generating py / html file ... "
        pytext = compiler.topy()
        open(pyfile, 'w').write(pytext)

        #code = compiler.ttl2code( pyfile=pyfile, pytext=pytext )
        #context['_ttlcontext'] = context
        #module = compiler.execttl( code, context=context )
        ## Fetch parent-most module
        #body = getattr( module.self, 'body' )
        #html = body( *args ) if callable( body ) else ''

        ttlconfig.setdefault( 'memcache', 'true' )
        r = Renderer( ttlloc, ttlconfig )
        html = r( context=context )
        open( htmlfile, 'w' ).write( html )

        # This is for measuring performance
        st = dt.now()
        [ r( context=context ) for i in range(10) ]
        print (dt.now() - st) / 10

