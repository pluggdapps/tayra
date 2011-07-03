# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

import imp, re
from   StringIO                 import StringIO
from   os.path                  import basename

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
        return ''.join( self.popbuf() )

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

