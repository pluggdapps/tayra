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

import os, re
from   optparse             import OptionParser
from   os.path              import isfile, splitext
from   StringIO             import StringIO

import tayra
from   tayra                import __version__ as VERSION

def _option_parse() :
    '''Parse the options and check whether the semantics are correct.'''
    parser = OptionParser(usage="usage: %prog [options] filename")
    parser.add_option( '-o', '--outfile', dest='ofile', default=None,
                       help='Output html file to store translated result' )
    parser.add_option( '-d', action='store_true', dest='dump',
                       help='Dump translation' )
    parser.add_option( '-s', action='store_true', dest='show',
                       help='Show AST parse tree' )
    parser.add_option( '-t', action='store_true', dest='generate',
                       help='Generate python executable' )
    parser.add_option( '-x', action='store_true', dest='execute',
                       help='Executable and generate html' )
    parser.add_option( '-g', dest='debug', default='0',
                       help='Debug level for PLY parser' )
    parser.add_option( '--version', action='store_true', dest='version',
                       help='Version information of the package' )

    options, args   = parser.parse_args()

    return options, args

def main() :
    options, args = _option_parse()
    tu = None

    # Parse
    if options.version :
        print VERSION
    if args and isfile( args[0] ) and options.generate :
        tayra.ttl_render( args[0],
                          inplace=True,
                          debuglevel=int(options.debug),
                          show=options.show,
                          dump=options.dump,
                        )
    elif args and isfile( args[0] ) :
        tayra.ttl_render( args[0],
                          inplace=True,
                          debuglevel=int(options.debug),
                          show=options.show,
                          dump=options.dump,
                        )
if __name__ == '__main__' :
    main()
