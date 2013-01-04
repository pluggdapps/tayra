# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""
Tayra templating is a full-featured abstract markup language to describe
web-documents. It is primarily inspired from 
`mako-templates <http://www.makotemplates.org>`_ and 
`HAML <http://haml-lang.com/>`_ (for its indentation based markup
definitions). Although it is young and relatively a new kid among
the old-timers, it can be considered as the evolutionary next step for some of
them, if not all. The language itself is a meta-syntax and actual heavy
lifting is done by plugins implementing one of the many Tayra specification,
like, :class:`ITayraTags`, :class:`ITayraFilterBlock`,
:class:`ITayraEscapeFilter`. And probably it is the only templating
language that allows developers to build and distribute their templates
as plugins.

"""
    
from   os.path            import dirname, join, basename
from   pluggdapps.plugin  import Plugin, ISettings

__version__ = '0.3dev'

template_plugins = [
    'tayra:test/stdttl/implementer.ttl'
]

def loadttls( pa, ttlfiles, compiler_setts={} ):
    """Load tayra template files implementing template plugins. package()
    entry point can use this API to load ttl files.

    ``pa``,
        Pre-boot version of the platform coming via pacakge() entry point.

    ``ttlfiles``,
        List of tayra template files, implementing template plugins, in asset
        specification format.

    ``compiler_sett``,
        Dictionary of settings for TTLCompiler plugin to override the default
        configuration.
    """

    for ttlfile in ttlfiles :
        compiler = pa.query_plugin( pa, ISettings, 'ttlcompiler',
                                    settings=compiler_setts )
        code = compiler.compilettl( file=ttlfile )
        compiler.load( code, context={} )
        pa.loginfo( "Loaded template plugin %r ..." % ttlfile )

def package( pa ) :
    """A pluggdapps package must implement this entry point. This function
    will be called during platform pre-booting. Other than some initialization
    stuff, like dynamically loading template plugins using :func:`loadttls`,
    this entry point must return a dictionary of key,value pairs describing
    the package.
    """
    loadttls( pa, template_plugins, { 'debug' : True } )
    return {}

def translatefile( ttlfile, compiler, options ):
    """Using ``compiler``, an instance of TTLCompiler, and ``options``
    compiler and translate ``ttlfile`` into corresponding HTML file. The
    intermediate .py file and the final HTML file are saved in the same
    directory as the ttlfile."""
    args = getattr( options, 'args', [] )
    args = eval( args ) if isinstance( args, str ) else args
    context = getattr( options, 'context', {} )
    context = eval( context ) if isinstance( context, str ) else context
    context.update( _bodyargs=args )

    # Setup parser
    compiler._init( file=ttlfile )
    htmlfile = join( dirname(compiler.ttlfile), 
                     basename(compiler.ttlfile).rsplit('.', 1)[0] + '.html' )

    # Intermediate file should always be encoded in 'utf-8'
    enc = compiler.encoding[:-4] if compiler.encoding.endswith('-sig') else \
            compiler.encoding # -sig is used to interpret BOM
    code = compiler.compilettl()

    # Generate
    module = compiler.load( code, context=context )
    html = compiler.generatehtml( module, context )
    open( htmlfile, mode='w', encoding='utf-8' ).write( html )


class BaseTTLPlugin( Plugin ):
    """Base class for all plugins implementing one or more template
    interfaces.
    
    Tayra template plugins automatically derive from this base class when they
    declare,

        @implement <Interface.specfication> as <pluginname>
    """
    pass

import tayra.compiler       # Tayra compiler
import tayra.decorators     # Implementation of  TTL function decorators 
import tayra.interfaces     # Import interfaces specified by tayra project.
import tayra.tags           # Import plugins implementing ITayraTags
import tayra.filterblocks   # Import plugins implementing ITayraFilterBlock
import tayra.escfilters     # Import plugins implementing ITayraEscapeFilter
