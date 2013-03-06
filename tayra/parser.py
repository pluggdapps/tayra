# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Parser grammer for Tayra Template Language. Parser is defined using 
`PLY <http://www.dabeaz.com/ply>`_."""

import ply.yacc

from   tayra.lexer      import TTLLexer
from   tayra.ast        import *

class TTLParser( object ):
    """Parser class for tayra template language. This class is initialized
    with :class:`tayra.compiler.TTLCompiler` instance, and  configuration
    options like, ``optimize``, ``lex_debug``, ``lextab``, ``yacc_debug``,
    ``yacctab``, ``yacc_outputdir``.

    It might be a costly operation to create a TTLParser instance every time,
    and to avoid that use _initialize() method before starting off with a new
    template.
    """

    def __init__( self, compiler ) :
        self.compiler = compiler

    def _initialize( self, ttlfile=None ) :
        optimize = self.compiler['optimize']
        lex_debug = self.compiler['lex_debug']
        lextab = self.compiler['lextab']
        yacc_debug = self.compiler['yacc_debug']
        yacctab = self.compiler['yacctab']
        yacc_outputdir = self.compiler['yacc_outputdir']

        self.ttlfile = ttlfile

        # Build Lexer
        self.ttllex = TTLLexer( self.compiler )
        kwargs = { 'ttlfile' : ttlfile }
        kwargs.update( optimize=optimize ) if optimize else None
        kwargs.update( debug=lex_debug )
        kwargs.update( lextab=lextab ) if lextab else None
        self.ttllex.build( **kwargs )
        self.tokens = self.ttllex.tokens    # Important for YACCer
        self.ttllex.reset_lineno()

        # Build Yaccer
        kwargs = {'optimize' : optimize} if optimize else {}
        kwargs.update( debug=yacc_debug )
        kwargs.update( outputdir=yacc_outputdir ) if yacc_outputdir else None
        kwargs.update( tabmodule=yacctab )
        self.parser = ply.yacc.yacc( module=self, **kwargs )
        self.parser.ttlparser = self     # For AST nodes to access `this`
        self.parser.compiler = self.compiler

        self.prolog = True

    # ------------------------- Private functions -----------------------------

    def _coord( self, lineno, column=None ):
        return Coord( file=self.ttllex.ttlfile, line=lineno, column=column )
    
    def _parse_error(self, msg, coord):
        raise Exception("%s: %s" % (coord, msg))

    def _buildterms( self, p, terms ) :
        """Convenience function to construct Terminal nodes from parser object
        ``p``."""
        rc = []
        for t in terms :
            if t == None : 
                rc.append( None )
                continue
            elif isinstance(t, tuple) :
                cls, (val, lineno) = t[0], p[ t[1] ]
                rc.append( cls( p.parser, lineno, val ))
            else :
                rc.append(t)
        return rc
 
    #---- API methods.

    def parse( self, text, ttlfile=None, debuglevel=0 ):
        """Parse tayra templage text, ``text`` and return an AST tree. AST
        tree starts with a root node :class:`tayra.ast.Template`. Every time
        the parser is invoked the lexer, yaccer, app options will be reused.

        ``ttlfile``
            Name of the file being parsed (for meaningful error messages)

        ``debuglevel``
            Debug level to yacc
        """
        # Parser Initialize
        self._initialize( ttlfile=ttlfile )
        # parse and get the Translation Unit
        self.ast = self.parser.parse(text, lexer=self.ttllex, debug=debuglevel)
        return self.ast

    # ---------- Precedence and associativity of operators --------------------

    precedence = (
    )

    def p_template_1( self, p ) :
        """template : script"""
        p[0] = Template( p.parser, p[1] )

    def p_template_2( self, p ) :
        """template : """
        p[0] = Template( p.parser, None )

    def p_script_1( self, p ) :
        """script : doctype
                  | body
                  | importas
                  | inherit
                  | implement
                  | use
                  | statement
                  | tagline
                  | commentline
                  | tagblock
                  | commentblock
                  | textblock
                  | textspan
                  | filterblock
                  | functionblock
                  | interfaceblock
                  | ifelfiblock
                  | forblock
                  | whileblock"""
        p[0] = Script( p.parser, None, p[1] )

    def p_script_2( self, p ) :
        """script : script doctype
                  | script body
                  | script importas
                  | script inherit
                  | script implement
                  | script use
                  | script statement
                  | script tagline
                  | script commentline
                  | script tagblock
                  | script commentblock
                  | script textblock
                  | script textspan
                  | script filterblock
                  | script functionblock
                  | script interfaceblock
                  | script ifelfiblock
                  | script forblock
                  | script whileblock"""
        p[0] = Script( p.parser, p[1], p[2] )

    #-- Prolog

    def p_docytpe( self, p ) :
        """doctype  : DOCTYPE NEWLINES"""
        terms = [ (DOCTYPE, 1), (NEWLINES, 2) ]
        p[0] = DocType( p.parser, *self._buildterms( p, terms ))

    def p_body( self, p ) :
        """body     : BODY NEWLINES"""
        terms = [ (BODY, 1), (NEWLINES, 2) ]
        p[0] = Body( p.parser, *self._buildterms( p, terms ))

    def p_importas( self, p ) :
        """importas : IMPORT NEWLINES"""
        terms = [ (IMPORT, 1), (NEWLINES, 2) ]
        p[0] = ImportAs( p.parser, *self._buildterms( p, terms ))

    def p_inherit( self, p ) :
        """inherit  : INHERIT NEWLINES"""
        terms = [ (INHERIT, 1), (NEWLINES, 2) ]
        p[0] = Inherit( p.parser, *self._buildterms( p, terms ))

    def p_implement( self, p ) :
        """implement : IMPLEMENT NEWLINES"""
        terms = [ (IMPLEMENT, 1), (NEWLINES, 2) ]
        p[0] = Implement( p.parser, *self._buildterms( p, terms ))

    def p_use( self, p ) :
        """use      : USE NEWLINES"""
        terms = [ (USE, 1), (NEWLINES, 2) ]
        p[0] = Use( p.parser, *self._buildterms( p, terms ))

    def p_commentline( self, p ) :
        """commentline  : COMMENTLINE NEWLINES"""
        terms = [ (COMMENTLINE, 1), (NEWLINES, 2) ]
        p[0] = CommentLine( p.parser, *self._buildterms( p, terms ))

    def p_commentblock( self, p ) :
        """commentblock : COMMENTOPEN COMMENTTEXT COMMENTCLOSE NEWLINES
                        | COMMENTOPEN COMMENTCLOSE NEWLINES"""
        if len(p) == 5 :
            terms = [ (COMMENTOPEN,1), (COMMENTTEXT,2), (COMMENTCLOSE,3),
                      (NEWLINES,4) ]
        else :
            terms = [ (COMMENTOPEN,1), None, (COMMENTCLOSE,2), (NEWLINES,3) ]
        p[0] = CommentBlock( p.parser, *self._buildterms( p, terms ), 
                             prolog=self.prolog )

    #---- Script lines

    def p_statement( self, p ) :
        """statement    : STATEMENT NEWLINES"""
        terms = [ (STATEMENT, 1), (NEWLINES, 2) ]
        p[0] = Statement( p.parser, *self._buildterms(p, terms) )

    def p_tagline( self, p ) :
        """tagline      : tagspans NEWLINES"""
        p[1] = p[1].right_recursive( None, p[1].TAGBEGIN, p[1].text )
        terms = [ p[1], (NEWLINES, 2) ]
        p[0] = TagLine( p.parser, *self._buildterms(p, terms) )

    def p_tagspans_1( self, p ):
        """tagspans     : TAGBEGIN
                        | TAGBEGIN text"""
        if len(p) == 2 :
            terms = [ None, (TAGBEGIN,1), None ]
        else :
            terms = [ None, (TAGBEGIN,1), p[2] ]
        p[0] = TagSpans( p.parser, *self._buildterms(p, terms) )

    def p_tagspans_2( self, p ):
        """tagspans     : tagspans TAGBEGIN 
                        | tagspans TAGBEGIN text"""
        if len(p) == 3 :
            terms = [ p[1], (TAGBEGIN,2), None ]
        else :
            terms = [ p[1], (TAGBEGIN,2), p[3] ]
        p[0] = TagSpans( p.parser, *self._buildterms(p, terms) )

    def p_text( self, p ):
        """text         : TEXT
                        | text TEXT"""
        terms = [ None, (TEXT,1) ] if len(p) == 2 else [ p[1], (TEXT,2) ]
        p[0] = Text( p.parser, *self._buildterms(p, terms) )

    def p_textspan( self, p ):
        """textspan     : text tagspans NEWLINES"""
        p[2] = p[2].right_recursive( None, p[2].TAGBEGIN, p[2].text )
        terms = [ p[1], p[2], (NEWLINES,3) ] 
        p[0] = TextSpan( p.parser, *self._buildterms(p, terms) )

    #---- Script blocks

    def p_tagblock_1( self, p ) :
        """tagblock     : tagline INDENT script DEDENT"""
        terms = [ p[1], (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = TagBlock( p.parser, *self._buildterms( p, terms ) )

    def p_tagblock_2( self, p ) :
        """tagblock     : tagline INDENT DEDENT"""
        terms = [ p[1], (INDENT,2), None, (DEDENT,3) ]
        p[0] = TagBlock( p.parser, *self._buildterms( p, terms ) )

    def p_textblock_1( self, p ) :
        """textblock    : text NEWLINES"""
        terms = [ None, p[1], (NEWLINES, 2), None, None, None ]
        p[0] = TextBlock( p.parser, *self._buildterms(p, terms) )

    def p_textblock_2( self, p ):
        """textblock    : textblock text NEWLINES"""
        terms = [ p[1], p[2], (NEWLINES, 3), None, None, None ]
        p[0] = TextBlock( p.parser, *self._buildterms(p, terms) )

    def p_textblock_3( self, p ) :
        """textblock    : textblock INDENT script DEDENT"""
        terms = [ p[1], None, None, (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = TextBlock( p.parser, *self._buildterms(p, terms) )

    def p_textblock_4( self, p ) :
        """textblock    : textblock INDENT DEDENT"""
        terms = [ p[1], None, None, (INDENT,2), None, (DEDENT,3) ]
        p[0] = TextBlock( p.parser, *self._buildterms(p, terms) )

    def p_filterblock_1( self, p ) :
        """filterblock : FILTEROPEN NEWLINES filtertext FILTERCLOSE NEWLINES"""
        terms = [ (FILTEROPEN,1), (NEWLINES, 2), p[3], (FILTERCLOSE,4),
                  (NEWLINES,5) ]
        assert p[1][0].startswith( p[4][0].strip(' \t') )
        p[0] = FilterBlock( p.parser, *self._buildterms( p, terms ) )

    def p_filterblock_2( self, p ) :
        """filterblock : FILTEROPEN NEWLINES FILTERCLOSE NEWLINES"""
        terms = [ (FILTEROPEN,1), (NEWLINES,2), None, (FILTERCLOSE,3),
                  (NEWLINES,4) ]
        p[0] = FilterBlock( p.parser, *self._buildterms( p, terms ) )

    def p_filtertext( self, p ):
        """filtertext       : FILTERTEXT NEWLINES
                            | filtertext FILTERTEXT NEWLINES"""
        if len(p) == 4 :
            p[1].append( FILTERTEXT( p.parser, p[2][1], p[2][0]+p[3][0] ))
            p[0] = p[1]
        else :
            p[0] = [ FILTERTEXT( p.parser, p[1][1], p[1][0]+p[2][0] ) ]

    def p_functionblock_1( self, p ) :
        """functionblock : DECORATOR NEWLINES FUNCTION NEWLINES INDENT script DEDENT"""
        terms = [ (DECORATOR, 1), (NEWLINES, 2), (FUNCTION,3), (NEWLINES, 4),
                  (INDENT,5), p[6], (DEDENT,7) ]
        p[0] = FunctionBlock( p.parser, *self._buildterms(p, terms) )

    def p_functionblock_2( self, p ) :
        """functionblock : DECORATOR NEWLINES FUNCTION NEWLINES INDENT DEDENT"""
        terms = [ (DECORATOR,1), (NEWLINES, 2), (FUNCTION,3), (NEWLINES, 4),
                  (INDENT,5), None, (DEDENT,6) ]
        p[0] = FunctionBlock( p.parser, *self._buildterms(p, terms) )

    def p_functionblock_3( self, p ) :
        """functionblock : FUNCTION NEWLINES INDENT script DEDENT"""
        terms = [ None, None, (FUNCTION,1), (NEWLINES, 2), (INDENT,3), 
                  p[4], (DEDENT,5) ]
        p[0] = FunctionBlock( p.parser, *self._buildterms(p, terms) )

    def p_functionblock_4( self, p ) :
        """functionblock : FUNCTION NEWLINES INDENT DEDENT"""
        terms = [ None, None, (FUNCTION,1), (NEWLINES, 2), (INDENT,3),
                  None, (DEDENT,4) ]
        p[0] = FunctionBlock( p.parser, *self._buildterms(p, terms) )

    def p_interfaceblock_1( self, p ) :
        """interfaceblock   : INTERFACE NEWLINES INDENT script DEDENT"""
        terms = [ (INTERFACE,1), (NEWLINES, 2), (INDENT,3), p[4], (DEDENT,5) ]
        p[0] = InterfaceBlock( p.parser, *self._buildterms(p, terms) )

    def p_interfaceblock_2( self, p ) :
        """interfaceblock   : INTERFACE NEWLINES INDENT DEDENT"""
        terms = [ (INTERFACE,1), (NEWLINES, 2), (INDENT,3), None, (DEDENT,4) ]
        p[0] = InterfaceBlock( p.parser, *self._buildterms(p, terms) )

    #-- Control blocks  ( if-elif-else / for / while )

    def p_ifelfiblock_1( self, p ) :
        """ifelfiblock  : ifblock"""
        p[0] = IfelfiBlock( p.parser, None, p[1], None, None )

    def p_ifelfiblock_2( self, p ) :
        """ifelfiblock  : ifelfiblock elifblock"""
        p[0] = IfelfiBlock( p.parser, p[1], None, p[2], None )

    def p_ifelfiblock_3( self, p ) :
        """ifelfiblock  : ifelfiblock elseblock"""
        p[0] = IfelfiBlock( p.parser, p[1], None, None, p[2] )

    def p_ifblock_1( self, p ) :
        """ifblock      : IF NEWLINES INDENT script DEDENT"""
        terms = [ (IF,1), (NEWLINES, 2), (INDENT,3), p[4], (DEDENT,5) ]
        p[0] = IfBlock( p.parser, *self._buildterms(p, terms) )

    def p_ifblock_2( self, p ) :
        """ifblock      : IF NEWLINES INDENT DEDENT"""
        terms = [ (IF,1), (NEWLINES, 2), (INDENT,3), None, (DEDENT,4) ]
        p[0] = IfBlock( p.parser, *self._buildterms(p, terms) )

    def p_elifblock_1( self, p ) :
        """elifblock    : ELIF NEWLINES INDENT script DEDENT"""
        terms = [ (ELIF,1), (NEWLINES,2), (INDENT,3), p[4], (DEDENT,5) ]
        p[0] = ElifBlock( p.parser, *self._buildterms(p, terms) )

    def p_elifblock_2( self, p ) :
        """elifblock    : ELIF NEWLINES INDENT DEDENT"""
        terms = [ (ELIF,1), (NEWLINES,2), (INDENT,3), None, (DEDENT,4) ]
        p[0] = ElifBlock( p.parser, *self._buildterms(p, terms) )

    def p_elseblock_1( self, p ) :
        """elseblock    : ELSE NEWLINES INDENT script DEDENT"""
        terms = [ (ELSE,1), (NEWLINES,2), (INDENT,3), p[4], (DEDENT,5) ]
        p[0] = ElseBlock( p.parser, *self._buildterms(p, terms) )

    def p_elseblock_2( self, p ) :
        """elseblock    : ELSE NEWLINES INDENT DEDENT"""
        terms = [ (ELSE,1), (NEWLINES,2), (INDENT,3), None, (DEDENT,4) ]
        p[0] = ElseBlock( p.parser, *self._buildterms(p, terms) )

    def p_forblock_1( self, p ) :
        """forblock     : FOR NEWLINES INDENT script DEDENT"""
        terms = [ (FOR,1), (NEWLINES,2), (INDENT,3), p[4], (DEDENT,5) ]
        p[0] = ForBlock( p.parser, *self._buildterms(p, terms) )

    def p_forblock_2( self, p ) :
        """forblock     : FOR NEWLINES INDENT DEDENT"""
        terms = [ (FOR,1), (NEWLINES,2), (INDENT,3), None, (DEDENT,4) ]
        p[0] = ForBlock( p.parser, *self._buildterms(p, terms) )

    def p_whileblock_1( self, p ) :
        """whileblock   : WHILE NEWLINES INDENT script DEDENT"""
        terms = [ (WHILE,1), (NEWLINES,2), (INDENT,3), p[4], (DEDENT,5) ]
        p[0] = WhileBlock( p.parser, *self._buildterms(p, terms) )

    def p_whileblock_2( self, p ) :
        """whileblock   : WHILE NEWLINES INDENT DEDENT"""
        terms = [ (WHILE,1), (NEWLINES,2), (INDENT,3), None, (DEDENT,4) ]
        p[0] = WhileBlock( p.parser, *self._buildterms(p, terms) )

    def p_error( self, p ):
        if p:
            column = self.ttllex._find_tok_column( p )
            self._parse_error( 'before: %s ' % (p.value,),
                               self._coord(p.lineno, column) )
        else:
            self._parse_error( 'At end of input', '' )

class Coord( object ):
    """ Coordinates of a syntactic element. Consists of:
        - File name
        - Line number
        - (optional) column number, for the Lexer
    """
    def __init__( self, file, line, column=None ):
        self.file   = file
        self.line   = line
        self.column = column

    def __str__( self ):
        str = "%s:%s" % (self.file, self.line)
        if self.column :
            str += ":%s" % self.column
        return str
