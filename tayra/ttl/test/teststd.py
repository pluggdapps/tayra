#! /usr/bin/env python

import os, sys
from   optparse         import OptionParser
from   os.path          import abspath, join, isfile, isdir, basename
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
    print  
    print "Reference checking ... "
    for f in os.listdir( STDTTLDIR ) :
        outfile = join( STDTTLDIR, f )
        if f.startswith('.') or f.endswith( '.ttl' ) or isdir(outfile): continue
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
