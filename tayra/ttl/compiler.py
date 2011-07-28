import imp, os, stat, posixpath, re
from   os.path                  import isfile, isdir, abspath, basename, \
                                       join, dirname
from   hashlib                  import sha1
from   StringIO                 import StringIO

from   tayra.ttl                import initplugins
from   tayra.ttl.parser         import TTLParser
from   tayra.ttl.codegen        import InstrGen
from   tayra.ttl.runtime        import StackMachine, Namespace

"""
ttlconfig:
memcache
    boolean, to cache ttl code objects in memory
directories 
    a list of directories to look for .ttl files
module_directory 
    cache directory to store the .py intermediate files
devmod 
    boolean, to enable development mode.
plugin_packages 
    a comma seperated list of packages to import for loading plugins.
"""

class Compiler( object ):
    _memcache = {}

    def __init__( self,
                  ttllookup,
                  # Template options
                  ttlconfig={},
                  # TTLParser options
                  ttlparser=None,
                  # InstrGen options
                  igen=None,
                ):
        self.ttlconfig = ttlconfig
        # Initialize plugins
        initplugins( ttlconfig, force=ttlconfig.get('devmod', True) )
        # Lookup files
        self.ttllookup = ttllookup if isinstance(ttllookup, TemplateLookup) \
                         else TemplateLookup(ttllookup, ttlconfig)
        self.ttlfile = self.ttllookup.ttlfile
        self.pyfile, self.pytext = self.ttllookup.pyfile, self.ttllookup.pytext
        self.ttltext = None
        # Parser phase
        self.ttlparser = ttlparser or TTLParser()
        # Instruction generation phase
        self.igen = igen or InstrGen()

    def __call__( self, ttllookup ):
        clone = Compiler( ttllookup, ttlconfig=self.ttlconfig )
        return clone

    def execttl( self, code=None, context={} ):
        """Execute the template code (python compiled) under module's context
        `module`.
        """
        # Stack machine
        _m  = StackMachine( self.ttlfile, self )
        # Module instance for the ttl file
        module = imp.new_module( self.modulename )
        module.__dict__.update({
            self.igen.machname : _m,
            'self'   : Namespace( None, module ),
            'local'  : module,
            'parent' : None,
            'next'   : None,
        })
        module.__dict__.update( context )
        # Load ttl translated python code
        code = code or self.ttl2code()
        # Execute the code in module's context
        exec code in module.__dict__, module.__dict__
        return module

    def ttl2code( self, pyfile=None, pytext=None ):
        """Code loading involves, picking up the intermediate python file from
        the cache (if disk persistence is enabled and the file is available)
        or, generate afresh using `igen` Instruction Generator.
        """
        pyfile = pyfile or self.pyfile
        pytext = pytext or self.pytext
        if pytext :
            code = compile( pytext, pyfile or self.ttlfile, 'exec' )
            return code
        code = self._memcache.get( self.ttlfile, None )
        if code == None and pyfile and pytext :
            code = compile( pytext, pyfile, 'exec')
        elif code == None :
            pytext = self.topy()
            self.ttllookup.modcachepy( pyfile, pytext )
            code = compile( pytext, self.ttlfile, 'exec')
        # Cache output to file
        self.ttllookup.modcachepy( pyfile, pytext )
        if self.ttlconfig.get( 'memcache', '' ).lower() == 'true' :
            self._memcache[self.ttlfile] = code
        return code

    def toast( self ):
        tu = None
        if self.ttlfile and self.ttltext :
            tu = self.ttlparser.parse( self.ttltext, ttlfile=self.ttlfile )
        elif self.ttlfile :
            self.ttltext = open( self.ttlfile ).read()
            tu = self.ttlparser.parse( self.ttltext, ttlfile=self.ttlfile )
        return tu

    def topy( self, *args, **kwargs ):
        tu = self.toast()
        kwargs['ttlhash'] = sha1( self.ttltext ).hexdigest()
        if tu :
            tu.validate()
            tu.headpass1( self.igen )                   # Head pass, phase 1
            tu.headpass2( self.igen )                   # Head pass, phase 2
            tu.generate( self.igen, *args, **kwargs )   # Generation
            tu.tailpass( self.igen )                    # Tail pass
            return self.igen.codetext()
        else :
            return None

    modulename = property(lambda s : basename( s.ttlfile ).split('.', 1)[0] )



class TemplateLookup( object ) :
    TTLCONFIG = [
        ('directories', []),
        ('module_directory',None),
        ('devmod', True)
    ]
    def __init__( self, ttlloc, ttlconfig ):
        [ setattr( self, k, ttlconfig.get(k, default) )
          for k, default in self.TTLCONFIG ]
        self.ttlloc = os.sep.join(ttlloc) if hasattr(ttlloc, '__iter__') else ttlloc
        self.directories = [ d.rstrip(' \t/') for d in self.directories ]
        self.ttlfile = self._locatettl()
        self.pyfile, self.pytext = self._locatepy()
        self.pytext = self.pytext or (self.pyfile and open(self.pyfile).read())

    def _locatettl( self ):
        uri = self.ttlloc
        # If uri is simple absoulte path
        if isfile( abspath( uri )) :
            return uri
        # If uri is provided in asset specification format
        try :
            mod, loc = uri.split(':', 1)
            _file, path, _descr = imp.find_module( mod )
            ttlfile = join( path.rstrip(os.sep), loc )
            return ttlfile
        except :
            return None
        # If uri is relative to one of the template directories
        files = filter(
            lambda f : isfile(f), [ join(d, uri) for d in self.directories ]
        )
        if files :
            files[0]
        else :
            raise Exception( 'Error locating TTL file %r' % uri )

    def _locatepy( self ):
        pyfile = self.computepyfile()
        # Check whether the python intermediate file is not outdated, in devmod
        if self.devmod :
            return None, None
        elif pyfile and isfile(pyfile) :
            return pyfile, open(pyfile).read()
        else :
            return None, None

    def computepyfile( self ) :
        if self.module_directory :
            ttlloc = self.ttlloc[1:] if self.ttlloc.startswith('/') else self.ttlloc
            pyfile = join( self.module_directory, ttlloc+'.py' )
        else :
            pyfile = None
        return pyfile

    def modcachepy( self, pyfile, pytext ):
        pyfile = pyfile or self.computepyfile()
        if pyfile :
            d = dirname(pyfile)
            if not isdir(d) :
                os.makedirs(d)
            open( pyfile, 'w' ).write( pytext )
            return len(pytext)
        return None


def supermost( module ):
    """Walk through the module inheritance all the way to the parent most
    module, and return the same
    """
    parmod = module.parent
    while parmod : module, parmod = parmod, parmod.parent
    return module
