#! /usr/bin/env python

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

"""Command line execution"""

# -*- coding: utf-8 -*-

# Gotcha : None
#   1. Bug in PLY ???
#   Enabling optimize screws up the order of regex match (while lexing)
#       parser = Parser( yacc_debug=True )
# Notes  : None
# Todo   : None

import unittest, os, re
import difflib          as diff
from   random           import choice, randint, shuffle
from   optparse         import OptionParser
from   os.path          import isfile, splitext

from   tayra            import __version__ as VERSION
from   tayra            import TTL_EXTNAME, TSS_EXTNAME
from   tayra.tss.parser import TSSParser
#from   tayra.h.parser import TTLParser

def _option_parse() :
    '''Parse the options and check whether the semantics are correct.'''
    parser = OptionParser(usage="usage: %prog [options] filename")
    parser.add_option( '-o', '--outfile', dest='ofile', default=None,
                       help='Output html file to store translated result' )
    parser.add_option( '-d', action='store_true', dest='dump',
                       help='Dump translation' )
    parser.add_option( '-g', action='store_true', dest='debug',
                       help='Debug' )
    parser.add_option( '-s', action='store_true', dest='show',
                       help='Show AST parse tree' )
    parser.add_option( '-l', dest='debuglevel', default='0',
                       help='Debug level for PLY parser' )
    parser.add_option( '--version', action='store_true', dest='version',
                       help='Version information of the package' )

    options, args   = parser.parse_args()

    return options, args

def main() :
    options, args = _option_parse()
    #ttlparser = TTLParser( debug=options.debug )
    tssparser = TSSParser( debug=options.debug )
    tu = None
    if options.version :
        print VERSION
    if args and isfile( args[0] ) :
        ifile, ttl, tss = args[0], None, None
        if splitext(ifile)[0] == TTL_EXTNAME :
            ttl = open( ifile ).read()
        elif splitext(ifile)[0] == TSS_EXTNAME :
            tss = open( ifile ).read()
        else :
            tss = open( ifile ).read()
        debuglevel = int(options.debuglevel)
        print "Parsing ...",
        tu = tssparser.parse( tss, debuglevel=debuglevel )
        print "Done"
    if tu and options.dump :
        print tu.dump()
    elif tu and options.show :
        print "AST tree ..."
        tu.show()
    elif tu :
        ofile = options.ofile or (os.path.splitext(ifile)[0] + '.html')
        print "Translation ...",
        html = '<html><body>' + tu.tohtml() + '</body></html>'
        print "Done"
        open( ofile, 'w' ).write( html )

if __name__ == '__main__' :
    main()
