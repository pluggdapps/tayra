import imp, os, stat, posixpath, re
from   os.path                  import isfile, abspath, basename, join
from   hashlib                  import sha1
from   StringIO                 import StringIO

from   tayra.ttl                import initplugins
from   tayra.ttl.parser         import TTLParser
from   tayra.ttl.codegen        import InstrGen
from   tayra.ttl.runtime        import StackMachine, Namespace

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
        self.ttllookup = ttllookup if isinstance(ttllookup, TemplateLookup) \
                         else TemplateLookup(ttllookup, ttlconfig)
        self.ttlfile, self.pyfile = self.ttllookup.ttlfile, self.ttllookup.pyfile
        self.ttltext = None
        # Parser phase
        self.ttlparser = ttlparser or TTLParser()
        # Instruction generation phase
        self.pyfd = open( pyfile, 'w' ) if self.pyfile else StringIO()
        self.igen = igen or InstrGen( self.pyfd )
        # Initialize plugins
        initplugins( ttlconfig )

    def __call__( self, ttllookup ):
        clone = Compiler(
                    ttllookup,
                    ttlparser=self.ttlparser,
                    igen=self.igen
                )
        return clone

    def execttl( self, code=None, context={} ):
        """Execute the template code (python compiled) under module's context
        `module`.
        """
        # Stack machine
        __m  = StackMachine( self.ttlfile, self )
        # Module instance for the ttl file
        module = imp.new_module( self.modulename )
        module.__dict__.update({
            self.igen.machname : __m,
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
        if pytext :
            code = compile( pytext, pyfile or self.ttlfile, 'exec' )
            return code

        code = self._memcache.get( self.ttlfile, None )
        if code == None and self.pyfile :
            pytext = open(self.pyfile).read()
            code = compile( pytext, self.pyfile, 'exec')
        elif code == None :
            pytext = self.topy()
            code = compile( pytext, self.ttlfile, 'exec')
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
        if tu :
            tu.preprocess( self.igen )
            tu.generate( self.igen, *args, **kwargs )
            return self.igen.codetext()
        else :
            return None

    modulename = property(lambda s : basename( s.ttlfile ).split('.', 1)[0] )



class TemplateLookup( object ) :
    TTLCONFIG = [
        ('directories', []),
        ('module_directory',None),
        ('devmod',True)
    ]
    def __init__( self, ttlloc, ttlconfig ):
        [ setattr( self, k, ttlconfig.get(k, default) )
          for k, default in self.TTLCONFIG ]
        self.ttlloc = os.sep.join(ttlloc) if hasattr(ttlloc, '__iter__') else ttlloc
        self.directories = [ d.rstrip(' \t/') for d in self.directories ]
        self.ttlfile = self._locatettl()
        self.pyfile = self._locatepy()

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
            pass
        # If uri is relative to one of the template directories
        if uri.startswith('/') :
            files = filter( 
                lambda f : isfile(f),
                [ join(d, uri) for d in self.directories ]
            )
            return files[0]
        raise Exception( 'Error locating TTL file %r' % uri )

    def _locatepy( self ):
        ttlloc = self.ttlloc[1:] if self.ttlloc.startswith('/') else self.ttlloc
        pyfile = join( self.module_directory, ttlloc+'.py' 
                 ) if self.module_directory else None
        # Check whether the python intermediate file is not outdated, in devmod
        if pyfile and self.devmod and isfile( pyfile ) :
            ttltext, pytext = open(self.ttlfile).read(), open(pyfile).read()
            hashref = sha1( ttltext ).hexdigest()
            s = re.search( r"__ttlhash = '([0-9a-f])'\n", pytext )
            try :
                hashval = int( s.groups[0], 16 )
                if hashref == hashval : return pyfile
            except : pass
        elif pyfile and isfile(pyfile) :
            return pyfile
        else :
            return None

    def modcachepy( self, pytext ):
        if self.pyfile :
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

