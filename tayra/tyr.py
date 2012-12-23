#! /usr/bin/env python

# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

from   argparse            import ArgumentParser
from   os.path             import isfile, join, dirname, basename
import time
from   pluggdapps.platform import Pluggdapps
from   pluggdapps.plugin   import ISettings

from   tayra.utils         import Context

def options() :
    # Setup main script arguments
    description = "Pluggdapps command line script"
    argparser = ArgumentParser( description=description )
    argparser.add_argument( 
            '-o', '--outfile', dest='ofile',
            default=None,
            help='Outfile to dump the result' )
    argparser.add_argument( 
            '-l', dest='ttllex',
            action='store_true',
            help='Do lexical analysis of input file.' )
    argparser.add_argument( 
            '-p', dest='ttlyacc',
            action='store_true',
            help='Parse the file, check the dump and show the tree.' )
    argparser.add_argument(
            '-d', dest='dump',
            action='store_true',
            help='Dump translation' )
    argparser.add_argument(
            '-s', dest='show',
            action='store_true',
            help='Show AST parse tree' )
    argparser.add_argument(
            '-t', dest='generate',
            action='store_true', 
            help='Generate python executable' )
    argparser.add_argument( 
            '-x', dest='execute',
            action='store_true', 
            help='Executable and generate html' )
    argparser.add_argument(
            '-a', dest='args',
            default='[]',
            help='Argument to template' )
    argparser.add_argument(
            '-c', dest='context',
            default='{}',
            help='Context to template' )
    argparser.add_argument(
            '-g', dest='debug',
            default='0',
            help='Debug level for PLY argparser' )
    argparser.add_argument(
            '--version', dest='version',
            action='store_true',
            help='Version information of the package' )
    argparser.add_argument( 
            'ttlfile',
            help='Output html file to store translated result' )

    return argparser

def translatefile( pa, options ):
    args = eval( options.args )
    context = eval( options.context )
    context.update( _bodyargs=args )

    # Initialize plugins
    setts = {
        'lex_debug' : int(options.debug),
        'yacc_debug' : int(options.debug),
    }
    # Setup parser
    compiler = pa.query_plugin( pa, ISettings, 'ttlcompiler', settings=setts )
    compiler._init( file=options.ttlfile )
    pyfile = compiler.ttlfile+'.py'
    htmlfile = join( dirname(compiler.ttlfile), 
                     basename(compiler.ttlfile).rsplit('.', 1)[0] + '.html' )

    print( "Generating py / html file ... " )
    (pytext, code) = compiler.compile()
    # Intermediate file should always be encoded in 'utf-8'
    enc = compiler.encoding[:-4] if compiler.encoding.endswith('-sig') else \
            compiler.encoding # -sig is used to interpret BOM
    open( pyfile, mode='w', encoding=enc ).write( pytext )

    # Generate
    html = compiler.generate( context, code )
    open( htmlfile, mode='w', encoding=enc ).write( html )

    # This is for measuring performance
    st = time.time()
    [ compiler.generate( context, code ) for i in range(2) ]
    print( (time.time() - st) / 2 )

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
    setts = { 'parse_optimize' : False }
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
    setts = { 'parse_optimize' : False }
    compiler = pa.query_plugin( pa, ISettings, 'ttlcompiler', settings=setts )
    ttlparser = TTLParser( compiler )
    text   = open( options.ttlfile, encoding='utf-8-sig' ).read()
    t1     = time.time()
    # set debuglevel to 2 for debugging
    ast = ttlparser.parse( text, options.ttlfile, debuglevel=debuglevel )
    print( "Time taken to parse : ", time.time() - t1 )
    return ast

if __name__ == '__main__' :
    argparser = options()
    options = argparser.parse_args()
    pa = Pluggdapps.boot( None )
    
    if options.version :
        print( tayra.__version__ )

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
        translatefile( pa, options )

