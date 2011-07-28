import time, imp
from   StringIO                 import StringIO

from   zope.component           import getGlobalSiteManager
import pkg_resources            as pkg

# Import tag-plugins so that they can register themselves.
import tayra.ttl.tags.html
import tayra.ttl.tags.customhtml
import tayra.ttl.tags.forms
# Import filterblock-plugins so that they can register themselves.
import tayra.ttl.filterblocks.pycode
# Import escapefilter-plugins so that they can register themselves.
import tayra.ttl.filters.common

from   tayra.ttl.interfaces     import ITayraTags, ITayraFilterBlock, \
                                       ITayraEscapeFilter
from   tayra.ttl.parser         import TTLParser

EP_TTLGROUP = 'tayra.ttlplugins'
EP_TTLNAME  = 'ITTLPlugin'
DEFAULT_ENCODING = 'utf-8'

def findttls():
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

def loadttls( ttllocs, ttlconfig, context={} ):
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
    """Collect and organize Tayra template plugins"""
    global ttlplugins, tagplugins, init_status
    if init_status == 'progress' :
        return None
    if (force == False) and tagplugins:
        return None

    init_status = 'progress'
    gsm = getGlobalSiteManager()

    # Load plugin packages
    packages = ttlconfig.get( 'plugin_packages', '' )
    packages = [ x.strip(' \t') for x in packages.split(',') ]
    [ __import__(pkg) for pkg in filter(None, packages) ]

    # Gather plugins template tag handlers, filter-blocks
    for x in gsm.registeredUtilities() :
        if x.provided == ITayraTags :           # Tag handlers
            tagplugins[x.name] = ( x.component, x.component.handlers() )
        if x.provided == ITayraFilterBlock :    # Filter blocks
            fbplugins[x.name] = x.component
        if x.provided == ITayraEscapeFilter :   # Escape Filters
            escfilters[x.name] = x.component

    # Load ttl files implementing template plugins
    [ loadttls( ttllocs, ttlconfig ) for pkg, ttllocs in findttls() ]

    # Setup plugin lookup table
    for x in gsm.registeredUtilities() :
        # Skip plugins for tags, filters and filter-blocks
        if x.provided in [ ITayraTags ] : continue
        z = ttlplugins.setdefault( x.provided, {} )
        z.setdefault( x.name, x.component )
    init_status = 'done'
    return None

def queryTTLPlugin( interface, name='' ) :
    if name :
        return ttlplugins[interface][name]
    else :
        return ttlplugins[interface].values()

#---- APIs for executing Tayra Template Language

class Renderer( object ):
    def __init__( self, ttlloc, ttlconfig ):
        self.ttlloc, self.ttlconfig = ttlloc, ttlconfig

    def __call__( self, entry=None, context={} ):
        from   tayra.ttl.compiler       import Compiler, TemplateLookup
        ttlparser = TTLParser()
        compiler = Compiler(
            self.ttlloc, ttlconfig=self.ttlconfig, ttlparser=ttlparser
        )
        context['_ttlcontext'] = context
        module = compiler.execttl( context=context )
        # Fetch parent-most module
        entry = getattr( module.self, entry or 'body' )
        html = entry()
        return html

def ttl_cmdline( ttlloc, **kwargs ):
    from   tayra.ttl.compiler       import Compiler, TemplateLookup
    args = eval( kwargs.pop( 'args', '[]' ))
    debuglevel = kwargs.pop( 'debuglevel', 0 )
    show = kwargs.pop( 'show', False )
    dump = kwargs.pop( 'dump', False )
    ttlconfig = kwargs  # directories, module_directory, devmod
    ttlparser = TTLParser( debug=debuglevel )
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
        code = compiler.ttl2code( pyfile=pyfile, pytext=pytext )
        module = compiler.execttl( code )
        # Fetch parent-most module
        body = getattr( module.self, 'body' )
        html = body( *args ) if callable( body ) else ''
        open( htmlfile, 'w' ).write( html )
