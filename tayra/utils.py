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
        opts = self.get( 'options', u'' )
        return opts() if callable(opts) else opts

    # Compulsory fields
    default = property( lambda self : self['default'] )
    types = property( 
        lambda self : u', '.join([ t.__name__ for t in self['types'] ])
    )


def asbool( obj ):
    """Convert ``obj`` to Boolean value based on its string representation"""
    if not isinstance(obj, (str, unicode)) : return bool(obj)

    obj = obj.strip().lower()
    if obj in ['true', 'yes', 'on', 'y', 't', '1']:
        return True
    elif obj in ['false', 'no', 'off', 'n', 'f', '0']:
        return False
    else:
        raise ValueError( "String is not true/false: %r" % obj )


def parsecsv( line ) :
    """parse a comma separated `line`, into a list of strings"""
    vals = line and line.split( ',' ) or []
    vals = filter( None, [ v.strip(' \t') for v in vals ] )
    return vals


def hitch( function, *args, **kwargs ) :
    """Hitch a function with a different object and different set of
    arguments."""
    def fnhitched( *a, **kw ) :
        kwargs.update( kw )
        return function( *(args+a), **kwargs )
    return fnhitched
