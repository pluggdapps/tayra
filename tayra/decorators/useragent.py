# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

import re
import pluggdapps.utils as h

__all__ = [ 'useragent' ]

re_ua = re.compile( r'(Firefox|Chrome)/(3|4|5|6|7|8)' )
ualookup = {
  ('Firefox', '3')  :  'ff3',
  ('Firefox', '4')  :  'ff4',
  ('Firefox', '5')  :  'ff5',
  ('Firefox', '6')  :  'ff6',
  ('Firefox', '7')  :  'ff7',
  ('Chrome',  '8')  :  'ch8',
}
uacallable = {}

def dofunc_onuseragent( context, namespace, *args, **kwargs ):
    """This function replaces the original function decorated by ``useragent``
    and gets called. It uses uacallable to map to right callable based on
    requesting user-agent.
    """
    req = context.get('request', None)
    x = re_ua.findall( req.headers.get('User-Agent', '') ) if req else None
    x = ualookup.get( x and x[0] or None, 'default' )
    y = uacallable.get( namespace, None )
    func = y.get( x, y.get('default', None) ) if y else None
    return func( *args, **kwargs ) if func else None

def useragent( agents=[], namespace=None, _ttlcontext={} ):
    """Decorator to wrap different functions by same name into dictionary of
    callable, based on user agents. When a call is made to the function
    elsewhere in the template the actual call will be mapped to a callable,
    based on global variable ``request``.

    ``agents``
        List of agents (as strings) that should match the request enviroment,
        for the decorated function to be called. If this argument is not
        supplied then, the decorated function will be treated as default
        callable.
    ``namespace``
        String to be used as namespace for storing
        { agent : callable, ... } dictionary. If namespace is not provided, then
        decorated function's name will be used as namespace name
    """
    args = [ agents, namespace ]
    def decorator( func ):
        agents, namespace = args
        namespace = namespace or func.__name__
        d = uacallable.setdefault( namespace, {} )
        agents = [ agents ] if isinstance( agents, str ) else agents
        if agents :
            d.update(dict([ (x, func) for x in agents ]))
        else :
            d.update( default=func )
        return h.hitch( dofunc_onuseragent, _ttlcontext, namespace )
    return decorator
