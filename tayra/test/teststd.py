#! /usr/bin/env python

# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

import os, sys
from   argparse         import ArgumentParser
from   os.path          import abspath, dirname, join, isdir, basename

from   pluggdapps.platform  import Pluggdapps
from   tayra                import translatefile

THISDIR = dirname( abspath( __file__ ))
STDTTLDIR = join( THISDIR, 'stdttl' )
STDTTLREFDIR = join( THISDIR, 'stdttl', 'ref' )

ua1 = ( "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.10 "
        "(KHTML, like Gecko) Ubuntu/10.10 Chromium/8.0.552.237 "
        "Chrome/8.0.552.237 Safari/534.10" )
ua2 = "Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/5.0.1"

class O( object ):
    pass

req = O()
req.headers = { 'User-Agent': ua2 }

contexts = {
    'useinterface.ttl' : '{ "plugin" : "testinterface" }',
    'body.ttl'         : '{ "_bodyargs" : ["hello", "world"] }',
    'dec_useragent.ttl': { "request" : req },
}
skipttls = [ 'implementer.ttl' ]
def test_stdttl( compiler, options ) :
    for f in sorted( os.listdir( STDTTLDIR )) :
        if any([ f.endswith( x ) for x in skipttls ]) :
            continue
        if f.endswith('.ttl') :
            print( f )
            ttlfile = join(STDTTLDIR, f)
            options.context = contexts.get(f, '{}')
            translatefile( ttlfile, compiler, options )
            pyfile = ttlfile + '.py'
            htmlfile = join( STDTTLDIR, f.split('.', 1)[0]+'.html' )
            refpyfile = join( STDTTLREFDIR, f+'.py' )
            refhtmlfile = join( STDTTLREFDIR, f.split('.', 1)[0]+'.html' )
            # os.system( 'diff %s %s' % (htmlfile, refhtmlfile) )
            if f in [ 'templaterule.ttl' ] : continue
            assert open( pyfile ).read() == open( refpyfile ).read()
            assert open( htmlfile ).read() == open( refhtmlfile ).read()

def mainoptions() :
    argparser = ArgumentParser( description="Test standard ttl files" )
    return argparser

if __name__ == '__main__' :
    argparser = mainoptions()
    options = argparser.parse_args()
    pa = Pluggdapps.boot( None )

    compiler = pa.query_plugin( pa, ISettings, 'ttlcompiler' )
    test_stdttl( compiler, options )
