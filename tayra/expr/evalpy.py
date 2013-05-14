# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Provides default expression evaluated and a common set of filtering
methods."""

from   pluggdapps.plugin    import Plugin, implements
import pluggdapps.utils     as h
from   tayra.interfaces     import ITayraExpression

class ExpressionEvalPy( Plugin ):
    """Plugin evaluates python expression and discards the resulting
    value. Doesn't supply any filtering rules."""

    implements( ITayraExpression )

    def eval( self, mach, text, globals_, locals_ ):
        """:meth:`tayra.interfaces.ITayraExpression.eval` interface 
        method."""
        eval( text, globals_, locals_ )
        return ''
