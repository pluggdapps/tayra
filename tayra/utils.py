# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Common library functions and utility functions specific to tayra package."""

import re
from   xml.etree                import ElementTree

from   pluggdapps.utils.asset   import parse_assetspec, \
                                       asset_spec_from_abspath, \
                                       abspath_from_asset_spec
from   pluggdapps.utils.config  import settingsfor, plugin2sec, sec2plugin, \
                                       ConfigDict
from   pluggdapps.utils.jsonlib import json_encode, json_decode
from   pluggdapps.utils.lib     import parsecsv, parsecsvlines, asbool, \
                                       asint, asfloat, docstr, reseed_random, \
                                       mergedict, takewhile, dropwhile, \
                                       flatten

h = [ 'parse_assetspec', 'asset_spec_from_abspath', 'abspath_from_asset_spec',
      'settingsfor', 'plugin2sec', 'sec2plugin', 'json_encode', 'json_decode',
      'parsecsv', 'parsecsvlines', 'asbool', 'asint', 'asfloat', 'docstr',
      'reseed_random', 'mergedict', 'takewhile', 'dropwhile', 'flatten', 
      'ConfigDict' ]

def etx2html( etxconfig={}, etxloc=None, etxtext=None, **kwargs ):
    """TBD : Convert eazytext content either supplied as a file (containing
    the text) or as raw-text, into html.

    ``etxconfig``,
        configuration parameters for eazytext. A deep-copy of this will be
        used.
    ``etxloc``,
        file location, either in asset specification format, or absolute path.
    ``etxtext``
        raw-text containing eazytext wiki.
    ``kwargs``
        interpreted as config-parameters that will override ``etxconfig``.
    """
    from eazytext import Translate as ETXTranslate
    etxconfig = dict(etxconfig.items())
    etxconfig.update( kwargs )
    t = ETXTranslate( etxloc=etxloc, etxtext=etxtext, etxconfig=etxconfig )
    return t( context={} )

def directive_tokens( s ):
    """Directives are meta constructs that provide more information on how to
    interpret a template text. Typically a directive starts with a **@**
    followed by directive name and one or more tokens and/or attributes
    pairs."""
    parts = list( filter( None, s.split(' ') ))
    typ = parts.pop(0)
    params = []
    for part in parts :
        try :
            name,value = part.strip().split('=', 1)
            params.append( (name, value) )
        except  :
            params.append( part.strip() )
    return params

class Context( object ):
    def __init__( self, htmlindent='' ):
        self.htmlindent = htmlindent

