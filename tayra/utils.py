# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

class ConfigDict( dict ):
    """Configuration class to implement settings.py module providing the
    package-default options. Along with the default options, it is possible to
    add help-text for each config-key, as a tuple,
        self[option-name] = (option-value, helptext)

    The help-text will be aggregated as a dictionary under,
        self._spec
    """
    def __init__( self, *args, **kwargs ):
        self._spec = {}
        dict.__init__( self, *args, **kwargs )

    def __setitem__( self, name, value ):
        self._spec[name] = ConfigItem( value )
        return dict.__setitem__( self, name, value['default'] )

    def specifications( self ):
        return self._spec


class ConfigItem( dict ):
    def _options( self ):
        opts = self.get( 'options', '' )
        return opts() if callable(opts) else opts

    # Compulsory fields
    default = property( lambda self : self['default'] )
    types = property( 
        lambda self : ', '.join([ t.__name__ for t in self['types'] ])
    )
