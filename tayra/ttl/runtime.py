# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

import imp, re
from   StringIO                 import StringIO
from   os.path                  import join, splitext, isfile, abspath, basename
from   hashlib                  import sha1

from   zope.component           import queryUtility
from   zope.component           import getUtility

from   paste.util.import_string import eval_import
from   tayra.ttl.interfaces     import ITayraTags
from   tayra.ttl.lexer          import TTLLexer
from   tayra.ttl.codegen        import InstrGen
import tayra

# Fetch all the tag handlers from registered plugins.
tagplugins = dict([ 
    ( name, (obj, obj.handlers()) )
    for name, obj in tayra.plugins.get( ITayraTags, {} ).items()
    if not isinstance( obj, list )
])

class StackMachine( dict ) :
    def __init__( self,
                  ifile,
                  igen,
                  tmpl,
                  usetagplugins=[ 'html' ],
                  encoding='utf-8'
                ):
        self.taghandlers = {}
        [ self.taghandlers.update( tagplugins[k][1] )
          for k in usetagplugins ]
        self.bufstack = [ [] ]
        self.ifile, self.usetagplugins, self.igen = ifile, usetagplugins, igen
        self.ttlparser = ttlparser
        self.encoding = 'utf-8'
        self.htmlindent = ''

    def encodetext( self, text ) :
        return text.encode( self.encoding )

    #---- Stack machine instructions

    def indent( self ) :
        text = self.encodetext( self.htmlindent )
        self.bufstack[-1].append( text )
        return text

    def upindent( self, up='' ) :
        self.htmlindent += up
        return self.htmlindent

    def downindent( self, down='' ) :
        self.htmlindent = self.htmlindent[:-len(down)]
        return self.htmlindent

    def append( self, value ) :
        if isinstance(value, basestring) :
            value = self.encodetext( value )
        self.bufstack[-1].append( value )
        return value

    def extend( self, value ) :
        if isinstance(value, list) :
            self.bufstack[-1].extend( value )
        else :
            raise Exception( 'Unable to extend context stack' )

    def pushbuf( self, buf=None ) :
        buf = []
        self.bufstack.append( buf )
        return buf

    def popbuf( self ) :
        return self.bufstack.pop(-1)

    def popbuftext( self ) :
        return ''.join( self.popbuf )

    def handletag( self, tagname, specifiers, style, attrs, tagfinish ) :
        """Entry point to handle tags"""
        tagnm = tagname.strip(TTLLexer.whitespac)[1:]
        handler = self.taghandlers.get( tagnm, None )
        if handler :
            html = handler( tagname, specifiers, style, attrs, tagfinish )
            self.append( html )
        else :
            Exception( 'Handler not known for %r' % tagnm )

    def importas( self, ttlloc, modname ):
        tmpl = self.tmpl( ttlloc )
        igen = self.igen( tmpl.pyfile )
        __m  = StackMachine( tmpl.ttlfile, igen, tmpl )
        # import module
        module = imp.new_module( modname )
        code = tmpl.loadcode()
        tmpl.execmod( module, code )
        return module

    def inherit( self, ttlloc, currglobals ):
        tmpl = self.tmpl( ttlloc )
        modname = basename( tmpl.ttlfile ).split('.', 1)[0]
        igen = self.igen( tmpl.pyfile )
        __m  = StackMachine( tmpl.ttlfile, igen, tmpl )
        # inherit module
        module = imp.new_module( tmpl.modulename() )
        currglobals['local'].parent = module
        module.__dict__.update({ 
            igen.machname : __m,
            'self'   : currglobals['self'],
            'local'  : module,
            'parent' : None,
            'next'   : currglobals['local'],
        })
        code = tmpl.loadcode()
        tmpl.execmod( module, code )

    def register( self, obj, interface, pluginname ):
        gsm.registerUtility( obj, interface, pluginname )

    def hitch( self, obj, cls, interfacefunc, *args, **kwargs ) :
        def fnhitched( self, *a, **kw ) :
            kwargs.update( kw )
            return interfacefunc( *(args+a), **kwargs )
        return fnhitched.__get__( obj, cls )

    def use( self, interface, pluginname='' ):
        return tayra.queryplugin( interface, pluginname )


class Template( object ) :
    TMPLHASH = {}

    def __init__( self,
                  ttlloc,
                  ttlparser,
                  ttldir=None,
                  cachedir=None,
                ):
        self.ttlloc, self.ttldir, self.cachedir = ttlloc, ttldir, cachedir
        self.tmplcache = join( cachedir, 'ttltemplates' ) if cachedir else None
        self.ttlfile = self.locatettl()
        self.pyfile = self.locatepy()
        self.ttltext = open( self.ttlfile ).read()
        self.ttlparser = ttlparser
        self.code, self.igen = None, InstrGen(self.pyfile)

    def __call__( self, ttlloc ):
        clone = Template( ttlloc, self.ttlparser, self.ttldir, self.cachedir )
        return clone
        
    def _pyfromcache( self, pyfile, hashref ):
        if not isfile(pyfile) : return None
        
        pytext = open( pyfile ).read()
        s = re.search( r'__ttlhash = ([0-9a-f])\n', pytext )
        try :
            hashval = s.groups[0]
            if hashval == hashref :
                return compile(pytext, self.pyfile or self.ttlfile, 'exec')
        except :
            return None
        return None

    def execmod( self, module, code=None ):
        """Execute the template code (python compiled) under module's context
        `module`. If `code` is None, it will generated from the
        ttl translated file.
        """
        self.code = code or self.code or self.loadcode()
        exec code in module.__dict__, self.module.__dict__
        return module

    def loadcode( self, igen=None ):
        """Code loading involves, picking up the intermediate python file from
        the cache (if disk persistence is enabled and the file is available)
        or, generate afresh using `igen` Instruction Generator.
        """
        igen = igen or self.igen
        hashval = sha1(self.ttltext).hexdigest()
        if hashval not in self.TMPLHASH :
            _, self.code = self.TMPLHASH[hashval]
        else :
            self.code = self.code or self._pyfromcache( pyfile, hashref )
            if not self.code :  # Generate afresh
                pytext = self.topy()
                self.code = compile(pytext, self.pyfile or self.ttlfile, 'exec')
                self.TMPLHASH[hashval] = ( self.ttlfile, self.code )
                self.cachepy( pytext, hashval )
                open( self.pyfile, 'w' ).write( pytext )    # Cache file
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
        parmod = module
        while parmod : parmod = parmod.parent
        return parmod
