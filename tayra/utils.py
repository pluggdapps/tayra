# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

import re
from   xml.etree    import ElementTree

def etx2html( etxconfig={}, etxloc=None, etxtext=None, **kwargs ):
    """Convert eazytext content either supplied as a file (containing the text)
    or as raw-text, into html.

    ``etxconfig``,
        Configuration parameters for eazytext. A deep-copy of this will be used.
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

