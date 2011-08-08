import imp, os, codecs
from   os.path                  import isfile, isdir, abspath, basename, \
                                       join, dirname
from   hashlib                  import sha1
from   StringIO                 import StringIO

from   tayra.ttl.parser         import TTLParser
from   tayra.ttl.codegen        import InstrGen
from   tayra.ttl.runtime        import StackMachine, Namespace


class Compiler( object ):
    _memcache = {}

    def __init__( self,
                  ttlloc=None,
                  ttltext=None,
                  # Template options
                  ttlconfig={},
                  # TTLParser options
                  ttlparser=None,
                  # InstrGen options
                  igen=None,
                ):
        # Source TTL
        if isinstance( ttlloc, TemplateLookup ) :
            self.ttllookup = ttlloc
        elif ttlloc or ttltext :
            self.ttllookup = TemplateLookup(
                ttlloc=ttlloc, ttltext=ttltext, ttlconfig=ttlconfig
            )
        else :
            raise Exception( 'To compile, provide a valid ttl source' )
        self.ttlfile, self.ttltext = self.ttllookup.ttlfile, self.ttllookup.ttltext
        self.pyfile, self.pytext = self.ttllookup.pyfile, self.ttllookup.pytext
        self.ttlconfig = ttlconfig
        # Parser phase
        self.ttlparser = ttlparser or TTLParser( ttlconfig=self.ttlconfig )
        # Instruction generation phase
        self.igen = igen or InstrGen( self, ttlconfig=self.ttlconfig )

    def __call__( self, ttlloc=None, ttltext=None, ttlparser=None ):
        ttlparser = ttlparser or self.ttlparser
        clone = Compiler( ttlloc=ttlloc, ttltext=ttltext,
                          ttlconfig=self.ttlconfig, ttlparser=ttlparser
                        )
        return clone

    def execttl( self, code=None, context={} ):
        """Execute the template code (python compiled) under module's context
        `module`.
        """
        # Stack machine
        _m  = StackMachine( self.ttlfile, self, ttlconfig=self.ttlconfig )
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

    def ttl2code( self ):
        """Code loading involves, picking up the intermediate python file from
        the cache (if disk persistence is enabled and the file is available)
        or, generate afresh using `igen` Instruction Generator.
        """
        pyfile, pytext = self.pyfile, self.pytext
        code = self._memcache.get( self.ttlfile, None )
        if code == None and self.pytext :
            code = compile( pytext, pyfile or self.ttlfile, 'exec' )
        elif code == None and pyfile :
            pytext = codecs.open(
                              pyfile, encoding=self.ttlconfig['input_encoding']
                            ).read()
            self.pytext = pytext
            code = compile( pytext, pyfile, 'exec')
        elif code == None :
            pytext = self.topy()
            code = compile( pytext, self.ttlfile, 'exec' )

        # Cache output to file
        self.ttllookup.modcachepy( pyfile, pytext )
        if self.ttlconfig['memcache'] :
            self._memcache.setdefault( self.ttlfile, code )
        return code

    def toast( self ):
        tu = self.ttlparser.parse( self.ttltext, ttlfile=self.ttlfile )
        return tu

    def topy( self, *args, **kwargs ):
        encoding = self.ttlconfig['input_encoding']
        tu = self.toast()
        kwargs['ttlhash'] = sha1( self.ttltext.encode(encoding) ).hexdigest()
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
    TTLCONFIG = [ 'directories', 'module_directory', 'devmod' ]
    def __init__( self, ttlloc=None, ttltext=None, ttlconfig={} ):
        [ setattr( self, k, ttlconfig[k] ) for k in self.TTLCONFIG ]
        self.ttlconfig = ttlconfig
        self.directories = [ d.rstrip(' \t/') for d in self.directories.split(',') ]
        self.ttlloc, self.ttltext = ttlloc, ttltext
        if self.ttlloc :
            self.ttlfile = self._locatettl( self.ttlloc, self.directories )
            self.ttltext = codecs.open(
                    self.ttlfile, encoding=ttlconfig['input_encoding']
            ).read()
            self.pyfile, self.pytext = self._locatepy( ttlloc, ttlconfig )
        elif self.ttltext :
            self.ttlfile = '<Source provided as raw text>'
            self.pyfile, self.pytext = None, None
        else :
            raise Exception( 'Invalid ttl source !!' )

    def _locatettl( self, ttlloc, dirs ):
        # If ttlloc is relative to one of the template directories
        files = filter( lambda f : isfile(f), [ join(d, ttlloc) for d in dirs ])
        if files : return files[0]

        # If ttlloc is provided in asset specification format
        try :
            mod, loc = ttlloc.split(':', 1)
            _file, path, _descr = imp.find_module( mod )
            ttlfile = join( path.rstrip(os.sep), loc )
            return ttlfile
        except :
            return None

        raise Exception( 'Error locating TTL file %r' % ttlloc )

    def _locatepy( self, ttlloc, ttlconfig ):
        devmod = ttlconfig['devmod']
        pyfile = self.computepyfile( ttlloc, ttlconfig )
        if devmod :    # In `devmod` always compile !!
            return None, None
        elif pyfile and isfile(pyfile) :
            pytext = codecs.open(pyfile, encoding=ttlconfig['input_encoding']
                                ).read()
            return pyfile, pytext
        elif pyfile :
            return pyfile, None
        else :
            return None, None

    def computepyfile( self, ttlloc, ttlconfig ) :
        module_directory = ttlconfig['module_directory']
        if module_directory :
            ttlloc = ttlloc[1:] if ttlloc.startswith('/') else ttlloc
            pyfile = join( module_directory, ttlloc+'.py' )
        else :
            pyfile = None
        return pyfile

    def modcachepy( self, pyfile, pytext ):
        if pyfile :
            d = dirname(pyfile)
            if not isdir(d) :
                os.makedirs(d)
            codecs.open( pyfile, mode='w', encoding=self.ttlconfig['input_encoding']
                       ).write( pytext )
            return len(pytext)
        return None


def supermost( module ):
    """Walk through the module inheritance all the way to the parent most
    module, and return the same
    """
    parmod = module.parent
    while parmod : module, parmod = parmod, parmod.parent
    return module
