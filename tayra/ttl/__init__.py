import time, imp
from   StringIO                 import StringIO

from   zope.component           import getGlobalSiteManager, queryUtility
import pkg_resources            as pkg

import tayra.ttl.tags.html
import tayra.ttl.tags.customhtml
import tayra.ttl.tags.forms
from   tayra.ttl.interfaces     import ITayraTags
from   tayra.ttl.parser         import TTLParser

EP_TTLGROUP = 'tayra.ttlplugins'
EP_TTLNAME  = 'ITTLPlugin'

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

    return [ ( pkgname, ep.load().implementers() )
             for pkgname, ep in entrypoints.items() ]

def loadttls( ttllocs, ttlconfig, context={} ):
    """Only when the plugins are compile and loaded, it is available for rest
    of the system.
    """
    from   tayra.ttl.compiler       import Compiler, TemplateLookup
    [ Compiler( TemplateLookup( ttlloc, ttlconfig )).execttl( context=context )
      for ttllocs in ttllocs ]

plugins = {}
tagplugins = {}
def initplugins( ttlconfig ):
    """Collect and organize Tayra template plugins"""
    global plugins, tagplugins

    loadttls( findttls(), ttlconfig )
    gsm = getGlobalSiteManager()
    for x in gsm.registeredUtilities() :
        z = plugins.setdefault( x.provided, {} )
        if x.name :
            z.setdefault( x.name, x.component )
        else :
            z.setdefault( x.name, [] ).append( x.component )
    # Gather plugins for template tag handlers
    [ tagplugins.setdefault( name, (obj, obj.handlers()) )
      for name, obj in plugins.get( ITayraTags, {} ).items()
      if not isinstance( obj, list )
    ]
    # Gather plugins for filters
    # Gather plugins for filter-blocks
    return plugins

def query_ttlplugin( interface, name='' ) :
    return plugins[interface][name]


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
        module = compiler.execttl( context=context )
        # Fetch parent-most module
        entry = getattr( module.self, entry or 'body' )
        html = entry()
        return html

def ttl_cmdline( ttlloc, **kwargs ):
    from   tayra.ttl.compiler       import Compiler, TemplateLookup
    context = eval( kwargs.pop( 'context', '{}' ))
    debuglevel = kwargs.pop( 'debuglevel', True )
    show = kwargs.pop( 'show', True )
    dump = kwargs.pop( 'dump', True )
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
        code = compiler.ttl2code( pyfile=pyfile, pytext=pytext )
        module = compiler.execttl( code )
        open(pyfile, 'w').write(pytext)
        # Fetch parent-most module
        html = module.self.body()
        open(htmlfile, 'w').write(html)
