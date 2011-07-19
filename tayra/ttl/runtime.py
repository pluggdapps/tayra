# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

import imp, re
from   StringIO                 import StringIO
from   os.path                  import basename

from   zope.component           import getGlobalSiteManager

from   paste.util.import_string import eval_import
from   tayra.ttl.interfaces     import ITayraTags
from   tayra.ttl.codegen        import InstrGen
from   tayra.ttl                import tagplugins, DEFAULT_ENCODING, \
                                       queryTTLPlugin

# Note :
# Special variables that the context should not mess with,
#       _m, _ttlhash, _ttlfile
#       StringIO, implements, getGlobalSiteManager, tayra
#       _Interface_<interfacename><num>
#       _Interface_<interfacename><num>_obj

gsm = getGlobalSiteManager()

class StackMachine( object ) :
    def __init__( self,
                  ifile,
                  compiler,
                  usetagplugins=[ 'html', 'customhtml', 'forms' ],
                  encoding=DEFAULT_ENCODING
                ):
        self.taghandlers = self._buildtaghandlers( usetagplugins )
        self.bufstack = [ [] ]
        self.ifile, self.usetagplugins, = ifile, usetagplugins
        self.compiler = compiler
        self.encoding = DEFAULT_ENCODING
        self.htmlindent = self.encodetext( '' )
        self.emptystring = self.encodetext( '' )

    def _buildtaghandlers( self, usetagplugins ):
        taghandlers = {}
        for pluginname in usetagplugins :
            handlers = tagplugins.get( pluginname, None )
            if handlers :
                taghandlers.update( handlers[1] )
        return taghandlers

    #---- Stack machine instructions

    def setencoding( self, encoding ):
        self.encoding = encoding
        self.htmlindent = self.encodetext( '' )
        self.emptystring = self.encodetext( '' )

    def encodetext( self, text ) :
        if isinstance( text, unicode) :
            return text
        else :
            text = str( text )
            return unicode( text, self.encoding )

    def upindent( self, up='' ) :
        self.htmlindent += up
        return self.htmlindent

    def downindent( self, down='' ) :
        self.htmlindent = self.htmlindent[:-len(down)]
        return self.htmlindent

    def indent( self ) :
        return self.append( self.htmlindent )

    def prunews( self ) :
        buf = self.bufstack[-1]
        buf.reverse()
        while buf :
            v = buf.pop(0).rstrip(' \t\r\n')
            if v :
                buf.insert(0, v)
                break
        buf.reverse()
        self.bufstack[-1] = buf

    def append( self, value ) :
        if isinstance(value, basestring) :
            value = self.encodetext( value )
        self.bufstack[-1].append( value )
        return value

    def extend( self, value ) :
        if isinstance(value, list) :
            value = [ self.encodetext(v) for v in value ]
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
        buf = self.popbuf()
        return self.emptystring.join( buf )

    def handletag( self, tagname, specifiers, style, attrs, tagfinish ) :
        """Entry point to handle tags"""
        from   tayra.ttl.tags       import handle_default
        tagnm = tagname.strip(' \t\r\n')[1:]
        handler = self.taghandlers.get( tagnm, None ) or handle_default
        self.append( handler( tagname, specifiers, style, attrs, tagfinish ))

    def importas( self, ttlloc, modname, childglobals ):
        compiler = self.compiler( ttlloc )
        parent_context = childglobals['_ttlcontext']
        module = compiler.execttl( context=parent_context )
        return module

    def inherit( self, ttlloc, childglobals ):
        compiler = self.compiler( ttlloc )
        # inherit module
        parent_context = childglobals['_ttlcontext']
        parent_context.update({
            'self'   : childglobals['self'],
            'parent' : None,
            'next'   : childglobals['local'],
        })
        module = compiler.execttl( context=parent_context )
        childglobals['self']._linkparent( Namespace( None, module ))
        childglobals['local'].parent = module
        return module

    def register( self, obj, interface, pluginname ):
        gsm.registerUtility( obj, interface, pluginname )

    def hitch( self, obj, cls, interfacefunc, *args, **kwargs ) :
        def fnhitched( self, *a, **kw ) :
            kwargs.update( kw )
            return interfacefunc( self, *(args+a), **kwargs )
        return fnhitched.__get__( obj, cls )

    def use( self, interface, pluginname='' ):
        return queryTTLPlugin( interface, pluginname )


class Namespace( object ):
    def __init__( self, parentnm, localmod ):
        self._parentnm = parentnm
        self._localmod = localmod

    def __getattr__( self, name ):
        if self._parentnm :
            return getattr(
                self._localmod, name, getattr( self._parentnm, name, None )
           )
        else :
            return getattr( self._localmod, name, None )
        
    def __setattr__( self, name, value ):
        if name in [ '_parentnm', '_localmod' ] :
            self.__dict__[name] = value
        else :
            setattr( self._localmod, name, value )
        return value

    def _linkparent( self, parentnm ):
        nm, parnm = self, self._parentnm
        while parnm : nm, parnm = parnm, parnm._parentnm
        nm._parentnm = parentnm
        return parentnm
