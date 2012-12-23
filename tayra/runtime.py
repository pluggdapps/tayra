# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

# Note :
# Special variables that the context should not mess with,
#       _m, _ttlhash, _ttlfile
#       StringIO, implements, getGlobalSiteManager, tayra
#       _Interface_<interfacename><num>
#       _Interface_<interfacename><num>_obj

import re

import pluggdapps.utils     as h
from   pluggdapps.plugin    import pluginname

from   tayra.lexer      import TTLLexer
from   tayra.interfaces import ITayraTags, ITayraEscapeFilter, \
                               ITayraFilterBlock

class Attributes( dict ):
    def __init__( self, *args, **kwargs ):
        self.attrstext = kwargs.pop( '_attrstext', [] )
        self.attrslist = kwargs.pop( '_attrslist', [] )
        dict.__init__( self, *args, **kwargs )

    def __str__( self ):
        attrslist = self.attrslist + map(lambda x: '%s="%s"'% x, self.items())
        s = ' '.join(filter( None, [ self.attrstext, attrslist ]))
        return s

    def __repr__( self ):
        return '%s' % self.__str__()

class StackMachine( object ) :
    DEFAULT_TAGS = [ 'html', 'customhtml', 'forms' ]

    Attributes = Attributes

    def __init__( self, ifile, compiler ):
        self.compiler = compiler
        self.encoding = compiler.encoding
        self.tagplugins = [ compiler.query_plugin( ITayraTags, name )
                                for name in compiler['usetagplugins'] ]
        self.escfilters = [ compiler.query_plugin( ITayraEscapeFilter, name )
                                for name in compiler['escape_filters'] ]
        self.escfilters = { x.codename : x for x in self.escfilters }
        self.filterblocks = compiler.query_plugins( ITayraFilterBlock )
        self.filterblocks = { pluginname(x) : x for x in self.filterblocks }
        self.bufstack = [ [] ]
        self.ifile = ifile
        self.htmlindent = ''

    #---- Stack machine instructions

    def indent( self ) :
        return self.append( self.htmlindent )

    def upindent( self, up='' ) :
        self.htmlindent += up
        return self.htmlindent

    def downindent( self, down='' ) :
        self.htmlindent = self.htmlindent[:-len(down)]
        return self.htmlindent

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
        x = ''.join( self.popbuf() )
        return x

    regex_style = re.compile( r'\{.*\}' )
    regex_attrs = re.compile( TTLLexer.attrname+'='+TTLLexer.attrvalue )

    def handletag( self, contents, tagbegin, indent=False, nl='' ):
        tagbegin = tagbegin.replace('\n', ' ')[1:-1]    # remove < and >
        try    : tagname, tagbegin = tagbegin.split(' ', 1)
        except : tagname, tagbegin = tagbegin, ''
        # Parse style content {...}
        tagbegin1, style = '', ''
        s = 0
        for m in self.regex_style.finditer( tagbegin ) :
            style = ';' + m.group()[1:-1].strip(' \t\r\n')
            start, end = m.regs[0]
            tagbegin1 += tagbegin[s:start]
            s = end
        tagbegin1 += tagbegin[s:].strip(' \t\r\n')
        styles = list( filter( None, style.split(';') ))
        # Parse attributes
        tagbegin2, attributes, s = '', [], 0
        for m in self.regex_attrs.finditer( tagbegin1 ):
            attributes.append( m.group() )
            start, end = m.regs[0]
            tagbegin2 += tagbegin1[s:start]
            s = end
        tagbegin2 += tagbegin1[s:].strip(' \t\r\n')
        # Parse tokens
        tokens = list( filter( None, tagbegin2.split(' ') ))
        
        for plugin in self.tagplugins :
            html = plugin.handle( self, tagname, tokens, styles, attributes,
                                  contents )
            if html == None : continue
            self.append( html )
            break
        else :
            raise Exception("Unable to handle tag %r" % tagname)

    def evalexprs( self, text, filters ) :
        for f in h.parsecsv( filters ) :
            text = self.escfilters[f].filter( text )
        return text

    def importas( self, ttlfile, childglobals ):
        compiler = self.compiler( ttlfile=ttlfile )
        parent_context = childglobals['_ttlcontext']
        module = compiler.execttl( context=parent_context )
        return module

    def inherit( self, ttlloc, childglobals ):
        compiler = self.compiler( ttlloc=ttlloc )
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

    # TODO : Can this method be replaced by pluggdapps.utils.lib.hitch ??
    def hitch( self, obj, cls, interfacefunc, *args, **kwargs ) :
        def fnhitched( self, *a, **kw ) :
            kwargs.update( kw )
            return interfacefunc( self, *(args+a), **kwargs )
        return fnhitched.__get__( obj, cls )

    def use( self, interface, pluginname='' ):
        return queryTTLPlugin( self.ttlplugins, interface, pluginname )


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

