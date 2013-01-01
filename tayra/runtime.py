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

import re, imp

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
                                for name in compiler['use_tag_plugins'] ]
        self.escfilters = [
            compiler.query_plugin( ITayraEscapeFilter, name ) 
            for name in compiler['escape_filters'] ]
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
    regex_str   = re.compile( TTLLexer.attrvalue )

    def handletag( self, contents, tagbegin, indent=False, nl='' ):
        tagbegin = tagbegin.replace('\n', ' ')[1:-1]    # remove < and >
        try    : tagname, tagbegin = tagbegin.split(' ', 1)
        except : tagname, tagbegin = tagbegin, ''
        
        styles, remtag = self.handletag_style( tagbegin )
        attributes, remtag = self.handletag_attributes( remtag )
        tokens, remtag = self.handletag_strings( remtag )
        tokens.extend( self.handletag_tokens( remtag ))

        for plugin in self.tagplugins :
            html = plugin.handle( self, tagname, tokens, styles, attributes,
                                  contents )
            if html == None : continue
            self.append( html )
            break
        else :
            raise Exception("Unable to handle tag %r" % tagname)

    def evalexprs( self, text, filters, globals_, locals_ ) :
        out = str( eval( text, globals_, locals_ ))
        for f in h.parsecsv( filters ) :
            for p in self.escfilters :
                out1 = p.filter( self, f, out )
                if out1 != None : 
                    out = out1
                    break
        return out

    def importttl( self, name, pyfile ):
        return imp.load_module( name, open(pyfile), pyfile,
                                (".py", "r", imp.PY_SOURCE) )

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

    # TODO : Can this method be replaced by pluggdapps.utils.lib.hitch ??
    def hitch( self, obj, cls, interfacefunc, *args, **kwargs ) :
        def fnhitched( self, *a, **kw ) :
            kwargs.update( kw )
            return interfacefunc( self, *(args+a), **kwargs )
        return fnhitched.__get__( obj, cls )

    def use( self, interface, pluginname='' ):
        return queryTTLPlugin( self.ttlplugins, interface, pluginname )

    #---- Local methods.

    def handletag_strings( self, tagbegin ): # Parse string tokens.
        remtag, tokens, s = '', [], 0
        for m in self.regex_str.finditer( tagbegin ) :
            tokens.append( m.group() )
            start, end = m.regs[0]
            remtag += tagbegin[s:start]
            s = end
        remtag += tagbegin[s:].strip(' \t\r\n')
        return tokens, remtag

    def handletag_style( self, tagbegin ): # Parse style content {...}
        remtag, style = '', ''
        s = 0
        for m in self.regex_style.finditer( tagbegin ) :
            style = ';' + m.group()[1:-1].strip(' \t\r\n')
            start, end = m.regs[0]
            remtag += tagbegin[s:start]
            s = end
        remtag += tagbegin[s:].strip(' \t\r\n')
        styles = list( filter( None, style.split(';') ))
        return styles, remtag

    def handletag_attributes( self, tagbegin ): # Parse attributes
        remtag, attributes, s = '', [], 0
        for m in self.regex_attrs.finditer( tagbegin ):
            attributes.append( m.group() )
            start, end = m.regs[0]
            remtag += tagbegin[s:start]
            s = end
        remtag += tagbegin[s:].strip(' \t\r\n')
        return attributes, remtag

    def handletag_tokens( self, tagbegin ): # Parse tokens
        tokens = list( filter( None, tagbegin.split(' ') ))
        return tokens


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

