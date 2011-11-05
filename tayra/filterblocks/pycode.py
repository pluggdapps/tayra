# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.interfaces     import  ITayraFilterBlock

gsm = getGlobalSiteManager()

class PyCode( object ):
    """Handle python code blocks.

    Follows indentation rules as defined by python language. To maintain
    consistency, it is better to indent the entire python code block by 2
    spaces. Each line will be interpreted as a python statement and substituted
    as is while compiling them into an intermediate .py text. If the //pycode//
    filter block is defined inside //@function// or //@interface// definition,
    then the filter block will inherit the same local scope and context as
    applicable to the function / interface definition. ''Otherwise, it will be
    considered as local to the implicitly defined body() function and will not
    be considered at global scope.'' To circumvent this situation, pycode filter
    block accept a ''global'' token that can be passed while defining the block.
    For example,

    {{{ Code ttl
    <div>
      :fb-pycode global
        print "hello world"
      :fbend
    }}}
    """
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
