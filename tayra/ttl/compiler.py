import imp
from   os.path                  import isfile, abspath, basename
from   hashlib                  import sha1
from   StringIO                 import StringIO

from   tayra.ttl.parser         import TTLParser
from   tayra.ttl.codegen        import InstrGen
from   tayra.ttl.runtime        import StackMachine, Namespace

CODECACHE = {}

class Compiler( object ):

    def __init__( self,
                  ttlloc,
                  ttlparser=None,
                  igen=None,
                  # TTLParser options
                  # InstrGen options
                  pyfile=None,
                  htmlfile=None,
                  ttldir=None,
                  cachedir=None,
                ):
        self.ttlloc, self.ttldir, self.cachedir = ttlloc, ttldir, cachedir
        self.tmplcache = join( cachedir, 'ttltemplates' ) if cachedir else None
        # Parser phase
        self.ttlfile = self._locatettl()
        self.ttltext = open( self.ttlfile ).read()
        self.hashttl = sha1( self.ttltext ).hexdigest()
        self.ttlparser = ttlparser or TTLParser()
        # Instruction generation phase
        self.pyfile, self.pytext = self._locatepy( self.tmplcache, self.ttlloc
                                   ) if pyfile else (None, None)
        self.pyfd = open( pyfile, 'w' ) if self.pyfile else StringIO()
        self.igen = igen or InstrGen( self.pyfd )
        self.pytext, self.code = None, None
        # Execution and translation phase -> to html
        if htmlfile :
            self.htmlfile = htmlfile
        elif isinstance( self.pyfile, basestring ) :
            self.htmlfile = self.pyfile.rsplit( '.', 2 )[0] + '.html'
        else :
            self.htmlfile = None
        self.htmlfd = open( htmlfile, 'w' ) if self.htmlfile else None


    def __call__( self, ttlloc ):
        clone = Template( ttlloc, self.ttlparser, self.ttldir, self.cachedir )
        return clone
        

    def _locatepy( self, tmplcache, ttlloc ):
        pyfile, uri = None, ttlloc
        if tmplcache :
            # Locate the python file from disk cache-directory
            ttlloc_ = uri[1:] if uri.startswith('/') else uri 
            pyfile = join( tmplcache, ttlloc_+'.py' )
            if isfile( pyfile ):
                # Check whether the python intermediate file is not outdated
                pytext = open( pyfile ).read()
                s = re.search( r"__ttlhash = '([0-9a-f])'\n", pytext )
                try :
                    hashval = int( s.groups[0], 16 )
                    if self.hashttl == hashval : return (pyfile, pytext)
                except : pass
        return (None, None)


    def _locatettl( self ):
        uri = self.ttlloc
        if isfile( abspath( uri )) :
            return uri
        elif uri.startswith('/') :
            ttlfile = join(self.ttldir, uri[1:]) if self.ttldir else uri
            if not isfile(ttlfile) :
                raise Exception( 'TTL file not found %r' % uri )
        else :
            try :
                mod, loc = uri.split(':', 1)
                _file, path, _descr = imp.find_module( mod )
                ttlfile = join( path, parts[1] )
            except :
                raise Exception( 'Error locating TTL file %r' % uri )
        return ttlfile if isfile(ttlfile) else None


    def ttl2code( self ):
        """Code loading involves, picking up the intermediate python file from
        the cache (if disk persistence is enabled and the file is available)
        or, generate afresh using `igen` Instruction Generator.
        """
        filename = self.pyfile or self.ttlfile+'.py'
        # Fetch the code from in-memory cache
        if self.hashttl in CODECACHE :
            _, self.code = CODECACHE[self.hashttl]
        # Generate afresh from the ttl-file
        elif not self.pytext :
            self.pytext = self.topy()
            CODECACHE[self.hashttl] = ( self.ttlfile, self.code )
            self.code = compile(self.pytext, filename, 'exec')
        self.pyfile and open( self.pyfile, 'w' ).write( self.pytext )
        return self.code


    def execttl( self, code=None, context={} ):
        """Execute the template code (python compiled) under module's context
        `module`. If `code` is None, it will generated from the
        ttl translated file.
        """
        # Stack machine
        __m  = StackMachine( self.ttlfile, self )
        # Module instance for the ttl file
        module = imp.new_module( self.modulename() )            
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


    def toast( self ):
        tu = self.ttlparser.parse( self.ttltext, ttlfile=self.ttlfile )
        return tu


    def topy( self, *args, **kwargs ):
        tu = self.toast()
        tu.preprocess( self.igen )                # Pre-process with igen
        tu.generate( self.igen, *args, **kwargs ) # Generate intermediate python
        return self.igen.codetext()


    def modulename( self ):
        return basename( self.ttlfile ).split('.', 1)[0]


def supermost( module ):
    """Walk through the module inheritance all the way to the parent most
    module, and return the same
    """
    parmod = module.parent
    while parmod : module, parmod = parmod, parmod.parent
    return module

