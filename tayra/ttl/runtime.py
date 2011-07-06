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
from   tayra.ttl.codegen        import InstrGen
from   tayra.ttl                import tagplugins

class StackMachine( dict ) :
    def __init__( self,
                  ifile,
                  compiler,
                  usetagplugins=[ 'html', 'customhtml', 'forms' ],
                  encoding='utf-8'
                ):
        self.taghandlers = {}
        [ self.taghandlers.update( tagplugins[k][1] ) for k in usetagplugins ]
        self.bufstack = [ [] ]
        self.ifile, self.usetagplugins, = ifile, usetagplugins
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
        from   tayra.ttl.tags       import handle_default
        tagnm = tagname.strip(' \t\r\n')[1:]
        handler = self.taghandlers.get( tagnm, None ) or handle_default
        self.append( handler( tagname, specifiers, style, attrs, tagfinish ))

    def importas( self, ttlloc ):
        compiler = self.compiler( ttlloc )
        module = compiler.execttl()
        return module

    def inherit( self, ttlloc, childglobals ):
        compiler = self.compiler( ttlloc )
        # inherit module
        parent_context = {
            compiler.igen.machname : __m,
            'self'   : childglobals['self'],
            'parent' : None,
            'next'   : childglobals['local'],
        }
        module = compiler.execttl( context=parent_context )
        childglobals['self'].__linkparent( Namespace( None, module ))
        childglobals['local'].parent = module
        return module

    def register( self, obj, interface, pluginname ):
        gsm.registerUtility( obj, interface, pluginname )

    def hitch( self, obj, cls, interfacefunc, *args, **kwargs ) :
        def fnhitched( self, *a, **kw ) :
            kwargs.update( kw )
            return interfacefunc( *(args+a), **kwargs )
        return fnhitched.__get__( obj, cls )

    def use( self, interface, pluginname='' ):
        return tayra.query_ttlplugin( interface, pluginname )


class Namespace( object ):
    def __init__( self, parentnm, localmod ):
        self._parentnm = parentnm
        self._localmod = localmod

    def __getattr__( self, name ):
        if self._parentnm :
            return self._localmod.get( name, self._parentnm.get( name, None ))
        else :
            return self._localmod.get( name, None )
        
    def __setattr__( self, name, value ):
        if name in [ '_parentnm', '_localmod' ] :
            self.__dict__[name] = value
        else :
            setattr( self._localmod, name, value )
        return value

    def __linkparent( self, parentnm ):
        nm, parnm = self, self._parentnm
        while parnm : nm, parnm = parnm, parnm._parentnm
        nm._parentnm = parentnm
        return parentnm
