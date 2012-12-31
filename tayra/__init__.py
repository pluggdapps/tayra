# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

import re
import pkg_resources        as pkg

import pluggdapps.utils     as h
from   pluggdapps.plugin    import Plugin, ISettings
from   pluggdapps.platform  import Pluggdapps

import tayra.interfaces

__version__ = '0.3dev'

template_plugins = [
    'tayra:test/stdttl/implementer.ttl'
]

def loadttls( ttlfiles ):
    from tayra.compiler import TTLCompiler
    pa = Pluggdapps.boot( None )
    for ttlfile in ttlfiles :
        compiler = TTLCompiler( pa )
        try :
            pytext, code = compiler.compile( file=ttlfile )
            compiler.load( code, context={} )
        except :
            h.print_exc()

def package() :
    """Entry point that returns a dictionary of key,value details about the
    package.
    """
    return {}

class BaseTTLPlugin( Plugin ):
    """Base class for all plugins implementing one or more template
    interfaces."""
    pass

import tayra.compiler
import tayra.tags
import tayra.filterblocks
import tayra.escfilters
