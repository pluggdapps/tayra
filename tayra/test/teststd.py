#! /usr/bin/env python

# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

import os, sys
from   optparse         import OptionParser
from   os.path          import abspath, join, isfile, isdir, basename
from   tayra            import ttl_cmdline

THISDIR = abspath( '.' )
STDTTLDIR = join( THISDIR, 'stdttl' )
STDTTLREFDIR = join( THISDIR, 'stdttl', 'ref' )


ua1 = """Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.10 """ \
      """(KHTML, like Gecko) Ubuntu/10.10 Chromium/8.0.552.237 """      \
      """Chrome/8.0.552.237 Safari/534.10"""
ua2 = """Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/5.0.1"""

class O( object ):
    pass

req = O()
req.headers = { 'User-Agent': ua2 }

contexts = {
    'useinterface.ttl' : '{ "plugin" : "testinterface" }',
    'body.ttl'         : '{ "_bodyargs" : ["hello", "world"] }',
    'dec_useragent.ttl': { "request" : req },
}
def test_stdttl() :
    for f in os.listdir(STDTTLDIR) :
        filepath = join(STDTTLDIR, f)
        if f.endswith('.ttl') :
            print '%r ...' % f
            ttl_cmdline( filepath, context=contexts.get(f, '{}') )
            print
    print  
    print "Reference checking ... "
    for f in os.listdir( STDTTLDIR ) :
        outfile = join( STDTTLDIR, f )
        if f.startswith('.') or f.endswith( '.ttl' ) or isdir(outfile) : continue
        reffile = join( STDTTLREFDIR, f )
        refpytext = open(reffile).read()
        pytext = open(outfile).read()
        print "%25r : %s" % ( basename(f), refpytext==pytext)

def _option_parse() :
    '''Parse the options and check whether the semantics are correct.'''
    parser = OptionParser(usage="usage: %prog [options] filename")

    options, args   = parser.parse_args()

    return options, args

if __name__ == '__main__' :
    options, args = _option_parse()
    test_stdttl()
