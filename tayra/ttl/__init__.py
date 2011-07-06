import time, imp
from   StringIO                 import StringIO

from   zope.component           import getGlobalSiteManager
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

def loadttls( ttllocs ):
    """Only when the plugins are compile and loaded, it is available for rest
    of the system.
    """
    [ Compiler( ttlloc ).execttl() for ttllocs in ttllocs ]

def runplugins():
    """Collect and organize Tayra template plugins"""
    loadttls( findttls() )
    gsm = getGlobalSiteManager()
    plugins = {}
    for x in gsm.registeredUtilities() :
        z = plugins.setdefault( x.provided, {} )
        if x.name :
            z.setdefault( x.name, x.component )
        else :
            z.setdefault( x.name, [] ).append( x.component )
    return plugins

def query_ttlplugin( interface, name='' ) :
    return plugins[interface][name]

# Dictionary of all globally registered plugins
plugins = runplugins()

# Dictionary of tag plugins
tagplugins = dict([
    ( name, (obj, obj.handlers()) )
    for name, obj in plugins.get( ITayraTags, {} ).items()
    if not isinstance( obj, list )
])

#---- APIs for executing Tayra Template Language

def render( ttlloc,
            ttldir=None,
            cachedir=None, 
            # Command line
            inplace=False,
            debuglevel=0,
            show=True,
            dump=True,
          ):
    from   tayra.ttl.compiler       import Compiler, supermost
    if inplace :    # For command line execution
        ttl_cmdline( ttlloc, debuglevel, show, dump )
        return None
    else :
        ttlparser = TTLParser( debug=debuglevel )
        compiler = Compiler(
            ttlloc, ttlparser=ttlparser, ttldir=ttldir, cachedir=cachedir
        )
        module = compiler.execttl()
        # Fetch parent-most module
        supermod = supermost( module )
        body = supermod.__dict__.pop( 'body' )
        html = body()
        return html

def ttl_cmdline( ttlloc, debuglevel, show, dump ):
    from   tayra.ttl.compiler       import Compiler, supermost
    ttlparser = TTLParser( debug=debuglevel )
    compiler = Compiler( ttlloc, ttlparser=ttlparser )
    pyfile, ttltext = (compiler.ttlfile+'.py'), open(compiler.ttlfile).read()
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
        if rctext != compiler.ttltext : print "Mismatch ..."
        else : print "Success ..."
    else :
        print "Generating py / html file ... "
        module = compiler.execttl()
        open(pyfile, 'w').write(compiler.pytext)
        # Fetch parent-most module
        supermod = supermost( module )
        body = supermod.__dict__.pop( 'body' )
        html = body()
        open(htmlfile, 'w').write(html)
