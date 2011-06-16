#! /usr/bin/env python

import os, sys
from   optparse         import OptionParser
from   os.path          import abspath, join
from   tayra.tss.parser import TSSParser

THISDIR = abspath( '.' )

def test_execute( f, options ) :
    print "Testing %r ..." % f,
    csstext = open(f).read()
    tssparser = TSSParser( debug=int(options.debug) )
    tu = tssparser.parse( csstext, debuglevel=int(options.debug) )
    rc = None
    if options.show :
        tu.show()
    else :
        dumptext = tu.dump()
        if tssparser.error_propertyname_prefix :
            print "Error : propertyname_prefix"
            rc = 'knownerror'
            if options.rmonsuccess : os.remove(f)
        elif csstext != dumptext :
            open('a', 'w').write(csstext)
            open('b', 'w').write(dumptext)
            print "(failure)"
            rc = 'failure'
        else :
            print "(success)"
            rc = 'success'
            if options.rmonsuccess : os.remove(f)
    return rc

def test_samplecss( cssdir, options ) :
    failures = success = total = knownerrors = 0
    for f in os.listdir( cssdir ) :
        f = join( cssdir, f )
        rc = test_execute(f, options)
        if rc == 'success' : success += 1
        elif rc == 'failure' : failures += 1
        elif rc == 'knownerror' : knownerrors += 1
        total += 1
    print "Success      : %r" % success
    print "Failures     : %r" % failures
    print "KnownErrors  : %r" % knownerrors
    print "Total        : %r" % total

def _option_parse() :
    '''Parse the options and check whether the semantics are correct.'''
    parser = OptionParser(usage="usage: %prog [options] filename")
    parser.add_option( '-d', dest='directory',
                       help='run test on directory' )
    parser.add_option( '-r', action='store_true', dest='rmonsuccess',
                       help='remove on success' )
    parser.add_option( '-g', dest='debug', default='0',
                       help='Debug' )
    parser.add_option( '-s', action='store_true', dest='show',
                       help='Show AST parse tree' )

    options, args   = parser.parse_args()

    return options, args

if __name__ == '__main__' :
    options, args = _option_parse()
    if args :
        test_execute( abspath(args[0]), options )
    elif options.directory :
        test_samplecss( abspath(options.directory), options )
