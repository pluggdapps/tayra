# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Plugin implements filter-block with syntax ``:py:``."""

import re, os

from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra.interfaces     import ITayraFilterBlock

class FilterBlockPy( Plugin ):
    """Handle python code blocks.

    Follows indentation rules as defined by python language. To maintain
    consistency, it is better to indent the entire python code block by 2
    spaces. Each line will be interpreted as a python statement and substituted
    as is while compiling them into an intermediate .py text.
    
    - If filter block is defined inside ``@def`` or ``@interface`` definition,
      then the filter block will inherit the same local scope and context as
      applicable to the function/interface definition.
    - Otherwise, it will be considered as local to the implicitly defined
      body() function.
    - To define python code blocks that are global to entire template module,
      define them outside template tags.

    .. code-block:: ttl
        :linenos:

        <div>
          :py:
            print( "hello world" )
          :py:
    """
    implements( ITayraFilterBlock )

    def headpass1( self, igen, node ):
        self.filteropen = node.FILTEROPEN.dump(None) + node.NEWLINES1.dump(None)
        return None

    def headpass2( self, igen, node, result ):
        return result

    def generate( self, igen, node, result, *args, **kwargs ):   # Inline
        self.localfunc = kwargs.get( 'localfunc', False )
        self.args, self.kwargs = args, kwargs
        if self.localfunc :
            self.genlines( igen, node, *args, **kwargs )
        return result

    def tailpass( self, igen, node, result ):
        if self.localfunc == False :
            self.genlines( igen, node, *self.args, **self.kwargs )
        return result

    def genlines( self, igen, node, *args, **kwargs ):
        indent = len( self.filteropen.rsplit(os.linesep, 1)[-1] )
        prefix = ''
        filtertext = node.filtertext[:]
        while filtertext :
            TERM = filtertext.pop(0)
            term = TERM.dump(None)
            igen.comment( "lineno:%s" % TERM.lineno )
            igen.putstatement( prefix + term.rstrip(' \t') )
            prefix = term.rsplit( os.linesep, 1 )[-1][indent:]
        node.NEWLINES2.generate( igen, *args, **kwargs )

    #---- ISettings interface methods

    @classmethod
    def default_settings( cls ):
        return _default_settings

    @classmethod
    def normalize_settings( cls, sett ):
        return sett

_default_settings = h.ConfigDict()
_default_settings.__doc__ = (
    "Plugin to handle tayra template's python code blocks" )
