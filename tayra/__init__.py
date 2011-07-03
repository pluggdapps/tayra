import time, imp
from   StringIO                 import StringIO

from   zope.component           import getGlobalSiteManager
import pkg_resources            as pkg

from   tayra.ttl.codegen        import Template
import tayra.ttl.plugins

__version__ = '0.1dev'

EPGROUP     = 'tayra.ttl.plugins'
EPNAME      = 'ITTLPlugins'

def loadplugins() :
    # Find plugins
    packages = pkg.WorkingSet().by_key
    entrypoints = {}
    for pkgname, d in packages.items() :
        names = d.get_entry_map( group=EPGROUP )
        for name, entrypoint in names.items() :
            if name != EPNAME : continue
            try : ep = d.get_entry_info( EPGROUP, name )
            except : continue
            entrypoints.setdefault( pkgname, ep )

    # Load plugins
    plugins = {}
    for pkgname, ep in entrypoints.items() :
        obj = ep.load()
        ttllocs = obj.implementers()
        for ttllocs in ttllocs :
            tmpl = Template( ttlloc, TTLParser(debug=debuglevel) )
            igen = InstrGen( tmpl.pyfile )
            __m  = StackMachine( tmpl.ttlfile, igen, tmpl )
            module = imp.new_module( tmpl.modulename() )
            module.__dict__.update({ 
                igen.machname : __m,
                'self'   : module,
                'local'  : module,
                'parent' : None,
                'next'   : None,
            })
            code = tmpl.loadcode()
            tmpl.execmod( module, code )

    # Search for plugins
    gsm = getGlobalSiteManager()
    for x in gsm.registeredUtilities() :
        z = plugins.setdefault( x.provided, {} )
        if x.name :
            z.setdefault( x.name, x.component )
        else :
            z.setdefault( x.name, [] ).append( x.component )
    return plugins

plugins = loadplugins()

from   tayra.ttl.parser         import TTLParser
from   tayra.ttl.codegen        import InstrGen
from   tayra.ttl.runtime        import StackMachine

def queryplugin( interface, name='' ) :
    return plugins[interface][name]


#---- APIs for executing Tayra Template Language

def ttl_cmdline( ttlloc, debuglevel, show, dump ):
    ttlparser = TTLParser( debug=debuglevel )
    tmpl = Template( ttlloc, ttlparser, pyfile=StringIO() )
    pyfile, ttltext = (tmpl.ttlfile+'.py'), open(tmpl.ttlfile).read()
    htmlfile = tmpl.ttlfile.rsplit('.', 1)[0] + '.html'
    if show :
        print "AST tree ..."
        tu = tmpl.toast()
        tu.show()
    elif dump :
        tu = tmpl.toast()
        rctext =  tu.dump()
        if rctext != tmpl.ttltext : print "Mismatch ..."
        else : print "Success ..."
    else :
        print "Generating py / html file ... "
        igen = InstrGen( pyfile )
        __m  = StackMachine( tmpl.ttlfile, igen, tmpl )
        module = imp.new_module( tmpl.modulename() )
        module.__dict__.update({ 
            igen.machname : __m,
            'self'   : module,
            'local'  : module,
            'parent' : None,
            'next'   : None,
        })
        code = tmpl.loadcode()
        open(pyfile, 'w').write(tmpl.pytext)

        tmpl.execmod( module, code )

        # Fetch parent-most module
        supermod = tmpl.supermost( module )
        body = supermod.__dict__.pop( 'body' )
        html = body()
        open(htmlfile, 'w').write(html)


def ttl_render( ttlloc,
                ttldir=None,
                cachedir=None, 
                modname='xyz'+str(int(time.time())),
                inplace=False,
                debuglevel=0,
                show=True,
                dump=True,
              ):
    if inplace :    # For command line execution
        ttl_cmdline( ttlloc, debuglevel, show, dump )
        return None
    else :
        ttlparser = TTLParser( debug=debuglevel )
        tmpl = Template( ttlloc, ttlparser, ttldir=ttldir, cachedir=cachedir )
        igen = InstrGen( tmpl.pyfile )
        __m  = StackMachine( tmpl.ttlfile, igen, tmpl )
        module = imp.new_module( tmpl.modulename() )
        module.__dict__.update({ 
            igen.machname : __m,
            'self'   : module,
            'local'  : module,
            'parent' : None,
            'next'   : None,
        })
        code = tmpl.loadcode()
        tmpl.execmod( module, code )

        # Fetch parent-most module
        supermod = tmpl.supermost( module )
        body = supermod.__dict__.pop( 'body' )
        html = body()
        return html
