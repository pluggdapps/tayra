# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Package code handles following functions,

* Command script APIs for,
  * dump(), regenerate ttl text from its AST, formed by parsing the text.
  * show(), display AST in human readable form.
  * Compile .ttl file into .ttl.py file and finally generate the .html file.
* API for web frameworks to render tayra-templates.
* API to query TTLPlugins. Template plugins implemented using Tayra template
  language in .ttl files.
* Import modules implementing plugins, which are expected to be registered with
  global-site-manager by modules themselves.
* Define package version.
* Default configuration for template engine.
* Normalization function for configuration values.
* Plugin initialization, loading and setting-up tag-plugins, plugins defining
  escape filters (for expression substitution) and filter blocks.
* Find template plugins defined in setuptools packages, compile them and load
  them registering the Template plugins. queryTTLPlugin() works only after
  this phase is successfully completed.
"""

import re
import pkg_resources            as pkg

# from   tayra.interfaces         import ITayraTags, ITayraFilterBlock, \
#                                        ITayraEscapeFilter
# 
# # Import tag-plugins so that they can register themselves.
# import tayra.tags
# import tayra.tags.html
# import tayra.tags.forms
# import tayra.tags.customhtml
# 
# # Import filterblock-plugins so that they can register themselves.
# import tayra.filterblocks.pycode
# 
# # Import escapefilter-plugins so that they can register themselves.
# import tayra.escfilters.common

__version__ = '0.21dev'

EP_TTLGROUP = 'tayra.plugins'
EP_TTLNAME  = 'ITTLPlugin'
DEFAULT_ENCODING = 'utf-8-sig'
ESCFILTER_RE = re.compile( r'([a-zA-Z0-9_-]+)(\.[a-zA-Z0-9_.-]+)*,' )
DEVMOD = False

def _findttls():
    """Search for template plugins, and return a list of tuples,
    ( pkgname, list-of-ttl-files ).
    """
    packages = pkg.WorkingSet().by_key
    entrypoints = {}
    for pkgname, d in packages.items() :
        names = d.get_entry_map( group=EP_TTLGROUP )
        for name, entrypoint in names.items() :
            if name != EP_TTLNAME : continue
            try : ep = d.get_entry_info( EP_TTLGROUP, name )
            except : continue
            entrypoints.setdefault( pkgname, ep )
    return [ ( pkgname, ep.load()().implementers() )
             for pkgname, ep in entrypoints.items() ]


def _loadttls( ttlfiles, ttlconfig, context={} ):
    """Only when the plugins are compile and loaded, it is available for rest
    of the system.
    """
    from tayra.compiler import Compiler
    [ Compiler(
        ttlfile=ttlfile, ttlconfig=ttlconfig ).compile( context=context )
      for ttlfile in ttlfiles ]


def initplugins( ttlconfig, force=False ):
    """Collect and organize Tayra template plugins, and plugins implementing
    language interfaces, like, ITayraTags, ITayraFilterBlock, 
    ITayraEscapeFilter,

    Plugins are loaded and organised in the following format,
    `ttlplugins`,
        { interfaceName : {plugin-name: instance, ... }, ... }
    `tagplugins`,
        { plugin-name   : instance ... }
    `fbplugins`,
        { plugin-name   : instance ... }
    `escfilters`,
        { plugin-name   : instance ... }
        
    and also saved inside ttlconfig for further processing.
    """
    ttlplugins = {}
    tagplugins = {}
    fbplugins  = {}
    escfilters = {}

    if (force == True) or ttlconfig.get( 'tagplugins', None ) == None :
        # Load and classify plugins
        gsm = getGlobalSiteManager()
        usetagplugins = ttlconfig['usetagplugins'] + ['']

        # import plugin packages defined in `ttlconfig`
        packages = ttlconfig['plugin_packages']
        if isinstance( packages, str ):
            packages = [ x.strip(' \t') for x in packages.split(',') ]
        [ __import__(pkg) for pkg in filter(None, packages) ]

        # Gather plugins template tag handlers, filter-blocks
        for x in gsm.registeredUtilities() :
            if x.provided == ITayraTags :           # Tag handlers
                try    : namespace, tagname = x.name.rsplit('.', 1)
                except : namespace, tagname = '', x.name
                if namespace in usetagplugins :
                    tagplugins[tagname] = x.component
            elif x.provided == ITayraFilterBlock :  # Filter blocks
                fbplugins[x.name] = x.component
            elif x.provided == ITayraEscapeFilter : # Escape Filters
                escfilters[x.name] = x.component
            else :
                continue
            if not hasattr( x.component, 'pluginname' ) :
                raise Exception(
                    '%r plugin must have `pluginname` attribute' % x.component
                )

        ttlconfig['tagplugins'] = tagplugins
        ttlconfig['fbplugins'] = fbplugins
        ttlconfig['escfilters'] = escfilters

        # Load ttl files implementing template plugins
        [ _loadttls( ttlfiles, ttlconfig ) for pkg, ttlfiles in _findttls() ]

        # Setup ttlplugin lookup table
        for x in gsm.registeredUtilities() :
            # Skip plugins for tags, filters and filter-blocks
            if getattr( x.component, 'itype', None ) == 'ttlplugin' :
                z = ttlplugins.setdefault( x.provided, {} )
                z.setdefault( x.name, x.component )
        ttlconfig['ttlplugins'] = ttlplugins
    return ttlconfig


def queryTTLPlugin( ttlplugins, interface, name, *args, **kwargs ):
    """Query for template plugins providing ``interface`` and registered
    under ``name``. If ``name`` is None, then a list of plugins providing
    (a.k.a implementing) the ``interface`` will be returned. If __call__
    method is defined by the template plugin component, a new clone of it
    will be created by calling the component with ``args`` and ``kwargs``.
    """
    iface = ttlplugins.get( interface, None )
    if iface == None : return None

    if name :
        p = iface.get( name, None )
        return p( *args, **kwargs ) if p and callable(p) else p
    else :
        return map( lambda p : p(*args, **kwargs) if callable(p) else p,
                    iface.values() )


class BaseTTLPlugin( object ):
    """Base class for all plugins implementing one or more template
    interfaces."""
    def __init__( self, *args, **kwargs ):
        self.args = args
        self.kwargs = kwargs

    def __call__( self, *args, **kwargs ):
        return self.__class__( *args, **kwargs )

def package() :
    """Entry point that returns a dictionary of key,value details about the
    package.
    """
    return {}

import tayra.compiler
import tayra.tags
import tayra.filterblocks
import tayra.escfilters

