# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

import re
from   StringIO                 import StringIO
from   os.path                  import basename

from   zope.component           import getGlobalSiteManager

from   tayra.ttl                import queryTTLPlugin

# Note :
# Special variables that the context should not mess with,
#       _m, _ttlhash, _ttlfile
#       StringIO, implements, getGlobalSiteManager, tayra
#       _Interface_<interfacename><num>
#       _Interface_<interfacename><num>_obj

gsm = getGlobalSiteManager()

class Attributes( dict ):
    def __init__( self, *args, **kwargs ):
        self.attrstext = kwargs.pop( '_attrstext', [] )
        self.attrslist = kwargs.pop( '_attrslist', [] )
        dict.__init__( self, *args, **kwargs )

    def __str__( self ):
        s = self.attrstext + ' '.join( 
            self.attrslist + map( lambda x : '%s="%s"' % x, self.items() )
        )
        return s

    def __repr__( self ):
        return '%s' % self.__str__()

class StackMachine( object ) :
    DEFAULT_TAGS = [ 'html', 'customhtml', 'forms' ]

    Attributes = Attributes

    def __init__( self,
                  ifile,
                  compiler,
                  ttlconfig={},
                ):
        self.escfilters = ttlconfig.get( 'escfilters', {} )
        self.tagplugins = ttlconfig.get( 'tagplugins', {} )
        self.def_escfilters = [
            f.strip().split('.',1)
            for f in ttlconfig['escape_filters'].split(',') if f
        ]
        self.ttlconfig = ttlconfig

        self.bufstack = [ [] ]
        self.ifile = ifile
        self.compiler = compiler
        self.encoding = self.ttlconfig['input_encoding']
        self.htmlindent = ''

    _cache_taghandlers = {}
    def _buildtaghandlers( self, usetagplugins ):
        key = ''.join( usetagplugins )
        if key in self._cache_taghandlers :
            return self._cache_taghandlers[key]

        taghandlers = {}
        for pluginname in usetagplugins :
            handlers = self.tagplugins.get( pluginname, None )
            if handlers :
                taghandlers.update( handlers[1] )
        self._cache_taghandlers.setdefault( key, taghandlers )
        return taghandlers

    #---- Stack machine instructions

    def setencoding( self, encoding ):
        #self.encoding = encoding
        pass

    #def encodetext( self, text ) :
    #    if isinstance( text, unicode) :
    #        return text
    #    else :
    #        text = repr( text )
    #        return unicode( text, self.encoding )

    def upindent( self, up='' ) :
        self.htmlindent += up
        return self.htmlindent

    def downindent( self, down='' ) :
        self.htmlindent = self.htmlindent[:-len(down)]
        return self.htmlindent

    def indent( self ) :
        return self.append( self.htmlindent )

    def append( self, value ) :
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
        buf = self.popbuf()
        return ''.join( buf )

    def handletag( self, contents, tag, indent=False, nl='' ):
        """Entry point to handle tags"""
        tagplugin = self.tagplugins.get( tag[0], self.tagplugins['_default'] )
        self.append(
            tagplugin.handle( self, tag, contents, indent=indent, newline=nl )
        )

    def evalexprs( self, val, filters ) :
        filters = self.def_escfilters + \
                  [ f.strip().split('.',1) for f in filters.split(',') if f ]
        skip  = filters.pop(0) if filters and filters[0][0] == 'n' else None
        if skip == None :   # No filtering
            text = val
        elif filters :      # Pluggable filters
            for filt in filters :
                text = self.escfilters.get( filt[0], None )( self, text, filt )
        return text

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

