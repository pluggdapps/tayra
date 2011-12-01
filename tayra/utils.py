# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

class ConfigItem( dict ):
    """Convenience class encapsulating config value description, which is a
    dictionary of following keys,

    ``default``,
        Default value for this settings parameter.
    ``types``,
        Comma separated value of valid types. Allowed types are str, unicode,
        basestring, int, long, bool, 'csv'. 'csv' is a custom defined.
    ``help``,
        Help string describing the purpose and scope of settings parameter.
    ``webconfig``,
        Boolean, specifying whether the settings parameter is configurable via
        web.

    Method call ``html(request=request)`` can be used to translate help text
    into html.
    """
    typestr = {
        str   : 'str', unicode : 'unicode', list : 'list', tuple : 'tuple',
        'csv' : 'csv', dict    : 'dict',    bool : 'bool', int   : 'int',
    }
    def _options( self ):
        opts = self.get( 'options', '' )
        return opts() if callable(opts) else opts

    def html( self, request=None ):
        from  bootstrap.pluggdapp import pyramidapps
        bootstrap = pyramidapps.get( 'bootstrap', None )
        helptxt = self.help
        if bootstrap and request :
            sett = request.environ['settings']
            etxconfig = sett.sections['mod:eazytext']
            fn = lambda m : '[[ %s | %s ]]' % (
                        m, bootstrap.route_url('ispeccls', cls=m) )
            helptxt = re.sub(r'IPluggd[a-zA-Z0-9_]*', fn, helptxt )
        else :
            etxconfig = {}
        etxconfig['nested'] = True
        etxconfig['nested.article'] = False
        html = etx2html( etxconfig, etxtext=helptxt )
        return html

    # Compulsory fields
    default = property( lambda self : self['default'] )
    types   = property(
                lambda s : ', '.join([ s.typestr[k] for k in s['types'] ])
              )
    # Optional fields, mostly for rendering on user-agent.
    help = property( lambda self : self.get('help', '') )
    webconfig = property( lambda self : self.get('webconfig', True) )
    options = property( _options )


class ConfigDict( dict ):
    """Configuration class to implement settings.py module providing the
    package-default options. Along with the default options, it is possible to
    add help-text for each config-key, as a dictionary.

    The setting-value description will be aggregated as a dictionary under,
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


def etx2html( etxconfig={}, etxloc=None, etxtext=None, **kwargs ) :
    """Convert eazytext content either supplied as a file (containing the text)
    or as raw-text, into html.

    ``etxconfig``,
        Configuration parameters for eazytext. A deep-copy of this will be used.
    ``etxloc``,
        file location, either in asset specification format, or absolute path.
    ``etxtext``
        raw-text containing eazytext wiki.
    ``kwargs``
        interpreted as config-parameters that will override ``etxconfig``.
    """
    from eazytext import Translate as ETXTranslate
    etxconfig = dict(etxconfig.items())
    etxconfig.update( kwargs )
    t = ETXTranslate( etxloc=etxloc, etxtext=etxtext, etxconfig=etxconfig )
    return t( context={} )



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
