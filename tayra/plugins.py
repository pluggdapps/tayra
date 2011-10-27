# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

from   zope.interface       import implements
from   tayra.interfaces     import ITTLPlugins

class TestPlugins( object ):
    implements( ITTLPlugins )

    def implementers( self ):
        #return ['tayra:test/stdttl/implementer.ttl']
        return []
