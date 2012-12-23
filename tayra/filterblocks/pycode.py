# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

import re

from   pluggdapps.plugin    import Plugin, implements
from   tayra.interfaces     import ITayraFilterBlock

class PyCode( Plugin ):
    """Handle python code blocks.

    Follows indentation rules as defined by python language. To maintain
    consistency, it is better to indent the entire python code block by 2
    spaces. Each line will be interpreted as a python statement and substituted
    as is while compiling them into an intermediate .py text. If ``pycode``
    filter block is defined inside ``@function`` or ``@interface`` definition,
    then the filter block will inherit the same local scope and context as
    applicable to the function/interface definition. **Otherwise, it will be
    considered as local to the implicitly defined body() function and will not
    be considered at global scope.** To circumvent this situation, pycode
    filter block accept a **global** token that can be passed while defining
    the block.  For example,

    ... code-block : html 

        <div>
          :fb-pycode global
            print "hello world"
          :fbend
    """
    implements( ITayraFilterBlock )

    def __init__( self, *args, **kwargs ):
        self.pylines = []

    def headpass1( self, igen, filteropen, filtertext, filterclose ):
        pylines = filtertext.splitlines()
        self.tokens = list( filter( filteropen[4:].strip().split(' ') ))
        # Align indentation
        striplen = ( len(pylines[0]) - len(pylines[0].lstrip(' \t')) ) \
                            if pylines else 0
        if tokens and (tokens[0] == 'global') :
            [ igen.putstatement( l[striplen:] ) for l in pylines ]
            self.pylines = []
        else :
            self.pylines = [ line[striplen:] for line in pylines ]

    def headpass2( self, igen ):
        pass

    def generate( self, igen, *args, **kwargs ):        # Inline
        [ igen.putstatement( line ) for line in self.pylines ]

    def tailpass( self, igen ):
        self.pylines = []
