#! /usr/bin/env python

import os, sys
from   optparse         import OptionParser
from   os.path          import abspath, join, isfile
from   tayra.ttl        import ttl_cmdline

THISDIR = abspath( '.' )
STDTTLDIR = join( THISDIR, 'stdttl' )
STDTTLREFDIR = join( THISDIR, 'stdttl', 'ref' )
STDTTLFILES = [ join(STDTTLDIR, f) for f in os.listdir(STDTTLDIR) ]

def test_stdttl() :
    for f in STDTTLFILES :
        if f.endswith('.ttl') :
            print '%r ...' % f
            ttl_cmdline(f)
    for f in os.listdir( STDTTLDIR ) :
        if f.endswith( '.py' ) and isfile( join( STDTTLREFDIR, f )) :
            refpytext = open( join( STDTTLDIR, f )).read()
            pytext = open( f ).read()
            print "%20r : %s" % (f, refpytext==pytext)
        elif f.endswith( '.html' ) and isfile( join( STDTTLREFDIR, f)) :
            refhtmltext = open( join( STDTTLDIR, f )).read()
            htmltext = open( f ).read()
            print "%20r : %s" % (f, refhtmltext==htmltext)

def _option_parse() :
    '''Parse the options and check whether the semantics are correct.'''
    parser = OptionParser(usage="usage: %prog [options] filename")

    options, args   = parser.parse_args()

    return options, args

if __name__ == '__main__' :
    options, args = _option_parse()
    test_stdttl()
