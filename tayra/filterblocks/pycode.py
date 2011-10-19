# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.interfaces     import  ITayraFilterBlock

gsm = getGlobalSiteManager()

class PyCode( object ):
    implements( ITayraFilterBlock )
    pluginname = 'pycode'

    def __init__( self, *args, **kwargs ):
        if args :
            self.parser, self.filteropen, self.filtertext, self.filterclose = \
                    args
        else :
            self.parser = self.filteropen = self.filtertext = \
            self.filterclose = None

    def __call__( self, parser=None, filteropen=None, filtertext=None,
                  filterclose=None ):
        parser = parser or self.parser
        filteropen = filteropen or self.filteropen
        filtertext = filtertext or self.filtertext
        filterclose = filterclose or self.filterclose
        return PyCode( parser, filteropen, filtertext, filterclose )

    def headpass1( self, igen ):                        # Global
        lines = self.filtertext.splitlines()
        # Signature
        self.signature = lines.pop(0) if lines else None
        self.tokens = tokens = self.signature.strip().split(' ')
        # Align indentation
        striplen = ( len(lines[0]) - len(lines[0].lstrip(' \t')) ) if lines else 0
        if tokens and tokens[0] == 'global' :
            lines = [ line[striplen:] for line in lines ]
            [ igen.putstatement( line ) for line in lines ]
            self.lines = []
        else :
            self.lines = [ line[striplen:] for line in lines ]

    def headpass2( self, igen ):
        pass

    def generate( self, igen, *args, **kwargs ):        # Inline
        lines = self.lines
        [ igen.putstatement( line ) for line in lines ]

    def tailpass( self, igen ):
        pass

# Register this plugin
gsm.registerUtility( PyCode(), ITayraFilterBlock, PyCode.pluginname )
