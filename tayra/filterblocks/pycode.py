# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

import re, os

from   pluggdapps.plugin    import Plugin, implements
from   tayra.interfaces     import ITayraFilterBlock

class TayraFilterBlockPy( Plugin ):
    """Handle python code blocks.

    Follows indentation rules as defined by python language. To maintain
    consistency, it is better to indent the entire python code block by 2
    spaces. Each line will be interpreted as a python statement and substituted
    as is while compiling them into an intermediate .py text. If ``pycode``
    filter block is defined inside ``@def`` or ``@interface`` definition,
    then the filter block will inherit the same local scope and context as
    applicable to the function/interface definition. **Otherwise, it will be
    considered as local to the implicitly defined body() function and will not
    be considered at global scope.** To circumvent this situation, pycode
    filter block accept a **global** token that can be passed while defining
    the block.  For example,

    ... code-block : html 

        <div>
          :py:
          print "hello world"
          :py:
    """
    implements( ITayraFilterBlock )

    def __init__( self, *args, **kwargs ):
        self.pylines = []

    def headpass1( self, igen, filteropen, filtertext, filterclose ):
        indent = len(filteropen.split(os.linesep)[-1])
        # Align indentation
        pylines = filtertext.splitlines()
        if pylines :
            self.pylines = [ pylines[0] ] + [ l[indent:] for l in pylines[1:] ]
        else :
            self.pylines = []
        return None

    def headpass2( self, igen, result ):
        return result

    def generate( self, igen, result, *args, **kwargs ):   # Inline
        self.localfunc = kwargs.get( 'localfunc', False )
        self.args, self.kwargs = args, kwargs
        if self.localfunc :
            [ igen.putstatement( line ) for line in self.pylines ]
        return result

    def tailpass( self, igen, result ):
        if self.localfunc == False :
            [ igen.putstatement( line ) for line in self.pylines ]
        self.pylines = []
        return result
