# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

from   os.path          import dirname, join, basename

import pluggdapps.utils         as h
from   pluggdapps.plugin        import Plugin, ISettings

import tayra.interfaces

__version__ = '0.3dev'

template_plugins = [
    'tayra:test/stdttl/implementer.ttl'
]

def loadttls( pa, ttlfiles, compiler_setts={} ):
    for ttlfile in ttlfiles :
        compiler = pa.query_plugin( pa, ISettings, 'ttlcompiler',
                                    settings=compiler_setts )
        code = compiler.compilettl( file=ttlfile )
        compiler.load( code, context={} )
        print( "Loaded template plugin %r ..." % ttlfile )

def package( pa ) :
    """Entry point that returns a dictionary of key,value details about the
    package.
    """
    loadttls( pa, template_plugins, { 'debug' : True } )
    return {}

def translatefile( ttlfile, compiler, options ):
    """Useing ``compiler``, an instance of TTLCompiler, and ``options``
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
    interfaces."""
    pass

import tayra.decorators
import tayra.compiler
import tayra.tags
import tayra.filterblocks
import tayra.escfilters
