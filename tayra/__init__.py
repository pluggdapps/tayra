# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""
Tayra is a full-featured abstract markup language to template web documents.
It is primarily inspired from 
`mako-templates <http://www.makotemplates.org/>`_ and
`HAML <http://haml-lang.com/>`_ (especially the indentation based
markup definitions). Although it is young and relatively a new kid among
the old-timers, it can be considered as the evolutionary next step for some of
them. And probably it is the only templating language that allows developers
to build and distribute their templates as plugins, not to mention the fact
that tayra's implementation itself is heavily based on plugins.
"""
    
from   os.path            import dirname, join, basename, abspath, isfile

from   pluggdapps.plugin  import Plugin, ISettings
import pluggdapps.utils   as h

__version__ = '0.43dev'

template_plugins = [
    'tayra:test/stdttl/implementer.ttl'
]

def loadttls( pa, ttlfiles, compiler_setts={} ):
    """Load tayra template files implementing template plugins.
    :meth:`package()` entry point, that will be called during pluggdapps 
    pre-booting, can use this API to load ttl files.

    ``pa``,
        Pre-boot version of the platform coming via pacakge() entry point.

    ``ttlfiles``,
        List of tayra template files, implementing template plugins, in asset
        specification format.

    ``compiler_sett``,
        Dictionary of settings for TTLCompiler plugin to override the default
        configuration, configuration settings from master ini file and
        backed data store.
    """

    for ttlfile in ttlfiles :
        compiler = pa.qp(
                pa, ISettings, 'tayra.ttlcompiler', settings=compiler_setts )
        code = compiler.compilettl( file=ttlfile )
        compiler.load( code, context={} )
        pa.logdebug( "Loaded template plugin %r ..." % ttlfile )

def package( pa ) :
    """Pluggdapps package must implement this entry point. This function
    will be called during platform pre-booting. Other than some initialization
    stuff, like dynamically loading template plugins using :func:`loadttls`,
    this entry point must return a dictionary of key,value pairs describing
    the package.
    """
    loadttls( pa, template_plugins, { 'debug' : True } )
    return {
        'ttlplugins' : template_plugins,
    }

def translatefile( ttlfile, compiler, options ):
    """Using an instance of TTLCompiler ``compiler``, and command line
    ``options``, translate ``ttlfile`` into corresponding HTML file. The
    intermediate .py file and the final HTML file are saved in the same
    directory as that of the ttlfile. ``options`` is expected to have
    attributes, ``args``, ``context``.
    """
    args = getattr( options, 'args', [] )
    args = eval( args ) if isinstance( args, str ) else args

    # Update context
    context = getattr( options, 'context', '{}' ).strip()
    try :
        context = eval(context)
    except :
        try :
            cxtfile = abspath( context )
            if isfile( cxtfile ) :
                context = eval( open( cxtfile ).read().strip() )
        except :
            context = {}

    context.update( _bodyargs=args )

    # Generate
    html = compiler.render( context, file=ttlfile )

    # Most probably invoked via command line, save as html file.
    htmlfile = join( dirname(compiler.ttlfile), 
                     basename(compiler.ttlfile).rsplit('.', 1)[0] + '.html' )
    open( htmlfile, mode='w', encoding='utf-8' ).write( html )


class BaseTTLPlugin( Plugin ):
    """Base class for all plugins implementing one or more template
    interfaces. Developers need not worry about this. Code generator and
    runtime will automatically create a blueprint, using this class, from 
    template-plugins. Provided the plugin is declared using `@implement`
    directive,::
    
        @implement tayra.interfaces:ITayraTestInterface as XYZTestInterface
    """
    
    #---- ISettings interface methods

    @classmethod
    def default_settings( cls ):
        """:meth:`pluggdapps.plugin.ISettings.default_settings` interface 
        method."""
        ds = h.ConfigDict()
        ds.__doc__ = (
            "Base class for all Tayra template plugins. This class does not "
            "provide any configurable parameters, instead refer to "
            "corresponding TTL-Plugin configuration." )
        return ds

    @classmethod
    def normalize_settings( cls, sett ):
        """:meth:`pluggdapps.plugin.ISettings.normalize_settings` interface 
        method."""
        return sett

import tayra.compiler       # Tayra compiler
import tayra.decorators     # Implementation of  TTL function decorators 
import tayra.interfaces     # Import interfaces specified by tayra project.
import tayra.tags           # Import plugins implementing ITayraTags
import tayra.filterblocks   # Import plugins implementing ITayraFilterBlock
import tayra.expr           # Import plugins implementing ITayraExpression


