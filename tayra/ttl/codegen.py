# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

from   os.path      import join, splitext, isfile, abspath, basename
from   StringIO     import StringIO
from   copy         import deepcopy
from   hashlib      import sha1

class Template( object ) :
    TMPLHASH = {}

    def __init__( self,
                  ttlloc,
                  ttlparser,
                  pyfile=None,
                  htmlfile=None,
                  ttldir=None,
                  cachedir=None,
                ):
        self.ttlloc, self.ttldir, self.cachedir = ttlloc, ttldir, cachedir
        self.tmplcache = join( cachedir, 'ttltemplates' ) if cachedir else None
        self.ttlfile = self.locatettl()
        self.pyfile = pyfile or self.locatepy() or StringIO()
        self.ttltext = open( self.ttlfile ).read()
        self.ttlparser = ttlparser
        self.pytext, self.code, self.igen = None, None, InstrGen(self.pyfile)
        if isinstance( self.pyfile, basestring ) :
            self.htmlfile = self.pyfile.rsplit( '.', 2 )[0] + '.html'

    def __call__( self, ttlloc ):
        clone = Template( ttlloc, self.ttlparser, self.ttldir, self.cachedir )
        return clone
        
    def _pyfromcache( self, pyfile, hashref ):
        pytext = open( pyfile ).read()
        s = re.search( r"__ttlhash = '([0-9a-f])'\n", pytext )
        try :
            hashval = int( s.groups[0], 16 )
            if hashval == hashref :
                return pytext
        except :
            return None
        return None

    def execmod( self, module, code=None ):
        """Execute the template code (python compiled) under module's context
        `module`. If `code` is None, it will generated from the
        ttl translated file.
        """
        self.code = code or self.code or self.loadcode()
        exec code in module.__dict__, module.__dict__
        return module

    def loadcode( self, igen=None ):
        """Code loading involves, picking up the intermediate python file from
        the cache (if disk persistence is enabled and the file is available)
        or, generate afresh using `igen` Instruction Generator.
        """
        igen = igen or self.igen
        hashval = sha1(self.ttltext).hexdigest()
        filename = self.pyfile \
                   if isinstance(self.pyfile, basestring) else self.ttlfile
        if hashval in self.TMPLHASH :
            _, self.code = self.TMPLHASH[hashval]
        elif isinstance( self.pyfile, basestring ) :
            self.pytext = self._pyfromcache( self.pyfile, hashval )
            if not self.pytext :  # Generate afresh
                self.pytext = self.topy()
                self.TMPLHASH[hashval] = ( self.ttlfile, self.code )
                open( self.pyfile, 'w' ).write( self.pytext )    # Cache file
            self.code = compile(self.pytext, filename, 'exec')
        else :
            self.pytext = self.topy()
            self.TMPLHASH[hashval] = ( self.ttlfile, self.code )
            self.code = compile(self.pytext, filename, 'exec')
        return self.code

    def toast( self, *args, **kwargs ):
        tu = self.ttlparser.parse(
                self.ttltext, ttlfile=self.ttlfile, *args, **kwargs
            )
        return tu

    def topy( self, *args, **kwargs ):
        igen = kwargs.pop( 'igen', self.igen )
        tu = self.toast( *args, **kwargs )
        tu.preprocess( self.igen )                # Pre-process with igen
        tu.generate( self.igen, *args, **kwargs ) # Generate intermediate python
        return self.igen.codetext()

    def locatettl( self ):
        uri = self.ttlloc
        if isfile( abspath(uri) ) :
            ttlfile = abspath(uri)
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

    def locatepy( self ):
        pyfile, uri = None, self.ttlloc
        if self.tmplcache :
            ttlloc_ = uri[1:] if uri.startswith('/') else uri 
            pyfile = join( self.tmplcache, ttlloc_+'.py' )
        return pyfile if pyfile and isfile(pyfile) else None

    def modulename( self ):
        return basename( self.ttlfile ).split('.', 1)[0]

    def supermost( self, module ):
        parmod = module.parent
        while parmod : module, parmod = parmod, parmod.parent
        return module


prolog = """# -*- encoding:utf-8 -*-

from   StringIO             import StringIO
from   zope.interface       import implements
from   zope.component       import getGlobalSiteManager
import tayra
from   tayra.ttl.runtime    import StackMachine

#UNDEFINED = runtime.UNDEFINED
#__M_dict_builtin = dict
#__M_locals_builtin = locals
#_magic_number = 6
#_template_filename=u'/home/pratap/mybzr/pratap/dev/pluggdapps/bootstrap/bootstrap/templates/_base/base.mak'
#_template_uri=u'bootstrap:templates/_base/base.mak'
#_template_cache=cache.Cache(__name__, _modified_time)
#_source_encoding='utf-8'
#_exports = []
"""

footer = """
__ttlhash = %r
__ttlfile = %r
"""

interfaceClass = """
class %s( object ):
    implements(%s)
%s_obj = %s()
"""

class InstrGen( object ) :
    machname = '__m'

    def __init__( self, outfile ):
        self.outfile = outfile
        self.fd = open( outfile, 'w' 
                  ) if isinstance(outfile, basestring) else outfile
        self.pyindent = ''
        self.optimaltext = []
        self.pytext = None
        # prolog for python translated template
        self.initialize( prolog )

    def __call__( self, outfile ):
        clone = InstrGen( outfile )
        return clone

    def initialize( self, prolog ):
        self.fd.write( prolog )
        self.cr()

    def cr( self, count=1 ) :
        self.fd.write( '\n'*count )
        self.fd.write( self.pyindent )

    def codetext( self ) :
        return self.pytext

    #---- Generate Instructions

    def indent( self ):
        self.flushtext()
        self.cr()
        self.fd.write( '__m.indent()' )

    def upindent( self, up='' ):
        self.fd.write( '__m.upindent( up=%r )' % up )

    def downindent( self, down='' ):
        self.fd.write( '__m.downindent( down=%r )' % down )

    def comment( self, comment ) :
        self.cr()
        self.fd.write( '#' + comment.rstrip('\r\n') )

    def flushtext( self ) :
        if self.optimaltext :
            self.cr()
            self.fd.write( '__m.extend( %s )' % self.optimaltext )
            self.optimaltext = []

    def puttext( self, text, force=False ) :
        self.optimaltext.append( text )
        if force or sum(map( lambda x : len(x), self.optimaltext)) > 100 :
            self.flushtext()

    def putvar( self, var ) :
        self.flushtext()
        self.cr()
        self.fd.write( '__m.append( %s )' % var )

    def putstatement( self, stmt ):
        self.flushtext()
        self.cr()
        self.fd.write( stmt.rstrip('\r\n') )

    def putblock( self, codeblock, indent=True ):
        [ self.putstatement(line) for line in codeblock.splitlines() ]

    def evalexprs( self, code ) :
        self.flushtext()
        self.cr()
        self.fd.write( '__m.append( str(%s) )' % code )

    def pushbuf( self ):
        self.flushtext()
        self.cr()
        self.fd.write( '__m.pushbuf()' )

    def popcompute( self, astext=True ):
        self.flushtext()
        self.cr()
        if astext == True :
            self.fd.write( '__m.append( __m.popbuftext() )' )
        else :
            self.fd.write( '__m.append( __m.popbuf() )' )

    def popreturn( self, astext=True ):
        self.flushtext()
        self.cr()
        if astext == True :
            self.fd.write( 'return __m.popbuftext()' )
        else :
            self.fd.write( 'return __m.popbuf()' )

    def computetag( self ):
        self.flushtext()
        self.cr()
        self.fd.write( '__m.handletag( *__m.popbuf() )' )

    def blockbegin( self, line, pyindent=True ) :
        self.putstatement( line )
        if pyindent == True :
            self.pyindent += '  '

    def finish( self ):
        self.flushtext()

    def putimport( self, ttlloc, modname ):
        self.cr()
        line = '%s = __m.importas( %r, %r )' % (modname, ttlloc, modname)
        self.fd.write( line )

    def putinherit( self, ttlloc ):
        self.cr()
        self.fd.write( '__m.inherit( %r, globals() )' % ttlloc, )

    def importinterface( self, interface ):
        self.putstatement( 'import %s' % interface )

    def implement_interface( self, implements, interfaces ):
        interfaces = {}
        [ interfaces.setdefault( ifname, [] ).append( method ) 
          for ifname, method in interfaces ]
        # Define interface class, hitch the methods and register the plugin
        for i in range(implements) :
            # Define interface implementer class
            interface, pluginname = implements[i]
            infcls = '__Interface' + str(i+1)
            codeblock = interfaceClass % ( infcls, interface, infcls, infcls )
            self.putblock( codeblock )
            # hitch methods with interface class
            for method in interfaces.get( interface, [] ) :
                line = '__m.hitch( %s_obj, %s, %s )' % (infcls, infcls, method)
                self.putstatement( line )
            # register the interface providing object
            line = '__m.register( %s_obj, %s, %r )' % ( infcls, interface,
                   pluginname )
            self.putstatement(line)

    def useinterface( self, interface, pluginname, importname ):
        line = '%s = __m.use( %s, %s )' % ( importname, interface, pluginname )
        self.putstatement(line)

    def footer( self, ttlhash, ttlfile ):
        self.cr()
        self.fd.write( footer % (ttlhash, ttlfile) )
        if isinstance(self.fd, StringIO):
            self.pytext = self.fd.getvalue()
        else :
            self.fd.close()
            self.pytext = open(self.outfile).read()
