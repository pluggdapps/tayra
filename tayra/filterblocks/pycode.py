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
            self.parser, self.opensyn, self.text, self.closesyn = args
        else :
            self.parser = self.opensyn = self.text = self.closesyn = None

    def __call__( self, parser=None, filteropen=None, filtertext=None,
                  filterclose=None ):
        parser = parser or self.parser
        opensyn = filteropen or self.opensyn
        text = filtertext or self.text
        closesyn = filterclose or self.closesyn
        return PyCode( parser, opensyn, text, closesyn )

    def headpass1( self, igen ):                        # Global
        lines = self.text.splitlines()
        self.tokens = tokens = lines.pop(0).strip().split(' ') if lines else []
        # Align indentation
        striplen = ( len(lines[0]) - len(lines[0].lstrip(' \t')) ) if lines else 0
        if tokens and tokens[0] == 'global' :
            [ igen.putstatement( line[striplen:] ) for line in lines ]
            self.lines = []
        else :
            self.lines = [ line[striplen:] for line in lines ]

    def headpass2( self, igen ):
        pass

    def generate( self, igen, *args, **kwargs ):        # Inline
        [ igen.putstatement( line ) for line in self.lines ]

    def tailpass( self, igen ):
        pass

# Register this plugin
gsm.registerUtility( PyCode(), ITayraFilterBlock, PyCode.pluginname )
