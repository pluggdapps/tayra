#! /usr/bin/env python

# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

from   argparse            import ArgumentParser
from   os.path             import isfile, join, dirname, basename
import time, os

import pluggdapps
from   pluggdapps.platform import Pluggdapps
from   pluggdapps.plugin   import ISettings

import tayra
from   tayra.utils         import Context

def mainoptions() :
    # Setup main script arguments
    description = "Pluggdapps command line script"
    argparser = ArgumentParser( description=description )
    argparser.add_argument( 
            '-l', dest='ttllex', action='store_true',
            help='Do lexical analysis of input file.' )
    argparser.add_argument(
            '-d', dest='dump', action='store_true',
            help='Dump translation' )
    argparser.add_argument(
            '-s', dest='show', action='store_true',
            help='Show AST parse tree' )
    argparser.add_argument(
            '-t', dest='test', action='store_true', 
            help='Execute test cases.' )
    argparser.add_argument(
            '-a', dest='args', default='[]',
            help='Argument to template' )
    argparser.add_argument(
            '-c', dest='context', default='{}',
            help='Context to template' )
    argparser.add_argument(
            '-g', dest='debug', default='0',
            help='Debug level for PLY argparser' )
    argparser.add_argument(
            '--version', dest='version', action='store_true',
            help='Version information of the package' )
    argparser.add_argument( 
            'ttlfile',
            help='Output html file to store translated result' )

    return argparser

#---- Lexer operations.
def fetchtoken( ttllex, stats ) :
    tok = ttllex.token()
    if tok :
        val = tok.value[1] if isinstance(tok.value, tuple) else tok.value
        print( "- %20r %s %s %s" % (val, tok.type, tok.lineno, tok.lexpos) )
        stats.setdefault( tok.type, [] ).append( tok.value )
    return tok

def lexical( pa, options ):
    from tayra.lexer import TTLLexer
    stats = {}
    setts = { 'optimize' : 0 }
    compiler = pa.query_plugin( pa, ISettings, 'ttlcompiler', settings=setts )
    ttllex = TTLLexer( compiler )
    ttllex.build( ttlfile=options.ttlfile )
    ttllex.input( open( options.ttlfile, encoding='utf-8-sig' ).read() )
    tok = fetchtoken( ttllex, stats )
    while tok :
        tok = fetchtoken( ttllex, stats )

#---- Parser operations.
def yaccer( pa, options, debuglevel=0 ):
    from tayra.parser import TTLParser
    setts = { 'optimize' : 0 }
    compiler = pa.query_plugin( pa, ISettings, 'ttlcompiler', settings=setts )
    ttlparser = TTLParser( compiler )
    text   = open( options.ttlfile, encoding='utf-8-sig' ).read()
    t1     = time.time()
    # set debuglevel to 2 for debugging
    ast = ttlparser.parse( text, options.ttlfile, debuglevel=debuglevel )
    print( "Time taken to parse : ", time.time() - t1 )
    return ast

if __name__ == '__main__' :
    argparser = mainoptions()
    options = argparser.parse_args()
    pa = Pluggdapps.boot( None )
    
    # Initialize plugins
    setts = {
        'lex_debug'  : int( options.debug ),
        'yacc_debug' : int( options.debug ),
        'debug'      : True,
    }

    compiler = pa.query_plugin( pa, ISettings, 'ttlcompiler', settings=setts )
    if options.version :
        print( tayra.__version__ )

    elif options.test :
        from tayra.test.teststd import test_stdttl
        print( "Executing TTL tests ..." )
        test_stdttl( compiler, options )

    elif options.ttllex and options.ttlfile : 
        print( "Lexing file %r ..." % options.ttlfile )
        lexical( pa, options )

    elif options.dump and options.ttlfile :
        print( "Parsing and dumping file %r ..." % options.ttlfile )
        ast = yaccer( pa, options, debuglevel=int(options.debug) )
        dumptext = ast.dump( context=Context() )
        text = open( options.ttlfile, encoding='utf-8-sig' ).read()
        if dumptext != text :
            open( 'dump', 'w' ).write( dumptext )
            open( 'text', 'w' ).write( text )
            assert False
        print( "Dump of AST matches the original text :)")

    elif options.show and options.ttlfile :
        print( "Parsing and describing file %r ..." % options.ttlfile )
        ast = yaccer( pa, options, debuglevel=int(options.debug) )
        ast.show()

    elif options.ttlfile and isfile( options.ttlfile ) :
        tayra.translatefile( options.ttlfile, compiler, options )

