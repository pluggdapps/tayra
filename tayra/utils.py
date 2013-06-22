# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Common library functions and utility functions specific to tayra package."""

import re
from   xml.etree                import ElementTree

import pluggdapps.utils         as h

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

def pynamespace(module, filterfn=None):
    """if ``module`` is string import module and collect all attributes
    defined in the module that do not start with `_`. If ``__all__`` is
    defined, only fetch attributes listed under __all__. Additionally apply
    ``filterfn`` function and return a dictionary of namespace from module."""
    module = h.string_import(module) if isinstance(module, str) else module
    d = { k:getattr(module,k) for k in getattr(module,'__all__',vars(module)) }
    [ d.pop(k) for k,v in d.items() if filterfn(k, v) ] if filterfn else None
    return d


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

