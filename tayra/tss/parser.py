# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

"""Parser grammer for Tayra Style Sheet"""

# -*- coding: utf-8 -*-

# Gotcha : None
#   1. Do not enable optimize for yacc-er. It optimizes the rules and the
#      rule handler fails.
#   2. To provide browser compliance, `operator` non-terminal can also have,
#           colon, equal, dot, gt, ask
#      like,
#           filter : progid:DXImageTransform.Microsoft.gradient(
#                       startColorstr='#c2080b',endColorstr='#8c0408',
#                       GradientType=0 )
# Notes  :
# Todo   : 
#   1. CSS3 `media-queries` for atrules to be supported.
#   2. *-prefix for property-name is not supported since IE7.

import logging, re, sys, copy
from   types            import StringType
from   os.path          import splitext, dirname
from   hashlib          import sha1

import ply.yacc
from   tayra.tss.lexer  import TSSLexer
from   tayra.tss.ast    import *

log = logging.getLogger( __name__ )
rootdir = dirname( __file__ )

class ParseError( Exception ):
    pass

# Default Wiki page properties
class TSSParser( object ):

    def __init__( self,
                  outputdir='',
                  lex_optimize=None,
                  lextab='tayra.lextab',
                  lex_debug=None,
                  yacc_optimize=None,
                  yacctab='tayra.yacctab',
                  yacc_debug=None,
                  debug=None
                ) :
        """
        Create a new TSSParser.

        : outputdir ::
            To change the directory in which the parsetab.py file (and other
            output files) are written.
                        
        : lex_optimize ::
            PLY-Lexer option.
            Set to False when you're modifying the lexer. Otherwise, changes
            in the lexer won't be used, if some lextab.py file exists.
            When releasing with a stable lexer, set to True to save the
            re-generation of the lexer table on each run.
            
        : lextab ::
            PLY-Lexer option.
            Points to the lex table that's used for optimized mode. Only if
            you're modifying the lexer and want some tests to avoid
            re-generating the table, make this point to a local lex table file
            (that's been earlier generated with lex_optimize=True)
            
        : lex_debug ::
            PLY-Yacc option.

        : yacc_optimize ::
            PLY-Yacc option.
            Set to False when you're modifying the parser. Otherwise, changes
            in the parser won't be used, if some parsetab.py file exists.
            When releasing with a stable parser, set to True to save the
            re-generation of the parser table on each run.
            
        : yacctab ::
            PLY-Yacc option.
            Points to the yacc table that's used for optimized mode. Only if
            you're modifying the parser, make this point to a local yacc table
            file.
                        
        : yacc_debug ::
            Generate a parser.out file that explains how yacc built the parsing
            table from the grammar.
        """
        self.tsslex = TSSLexer( error_func=self._lex_error_func )
        kwargs = dict(filter(
                    lambda x : x[1] != None,
                    [ ('optimize', lex_optimize), ('debug', lex_debug) ]
                 ))
        self.tsslex.build( lextab=lextab, **kwargs )
        self.tokens = self.tsslex.tokens
        kwargs = dict(filter(
                    lambda x : x[1] != None,
                    [ ('optimize', yacc_optimize), ('debug', yacc_debug) ]
                 ))
        self.parser = ply.yacc.yacc( module=self, tabmodule=yacctab,
                                     outputdir=outputdir, **kwargs
                                   )
        self.parser.tssparser = self     # For AST nodes to access `this`
        self.debug = lex_debug or yacc_debug or debug
        self._initialize()

    def _initialize( self ) :
        self.error_propertyname_prefix = None

    def parse( self, text, filename='', debuglevel=0 ):
        """Parses Tayra Style Sheet and creates an AST tree. For every
        parsing invocation, the same lex, yacc, app options and objects will
        be used.

        : filename ::
            Name of the file being parsed (for meaningful error messages)
        : debuglevel ::
            Debug level to yacc
        """

        # Initialize
        self._initialize()
        self.tsslex.filename = filename
        self.tsslex.reset_lineno()
        self.text = text
        self.hashtext = sha1( text ).hexdigest()

        # parse and get the Translation Unit
        self.tu = self.parser.parse( self.text,
                                     lexer=self.tsslex,
                                     debug=debuglevel )
        return self.tu

    # ------------------------- Private functions -----------------------------

    def _lex_error_func( self, lex, msg, line, column ):
        self._parse_error( msg, self._coord( line, column ))
    
    def _coord( self, lineno, column=None ):
        return Coord( file=self.tsslex.filename, 
                      line=lineno,
                      column=column
               )
    
    def _parse_error(self, msg, coord):
        raise ParseError("%s: %s" % (coord, msg))

    def _printparse( self, p ) :
        print p[0], "  : ",
        for i in range(1,len(p)) :
            print p[i],
        print

    # ---------- Precedence and associativity of operators --------------------

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('right', 'UNARY'),
    )

    def _buildterms( self, p, terms ) :
        rc = []
        for t in terms :
            if t == None : 
                rc.append( None )
                continue
            elif isinstance(t, tuple) :
                cls, idx = t
                rc.append( cls(p.parser, p[idx]) )
            else :
                rc.append(t)
        return rc

    def p_tss( self, p ) :
        """tss          : stylesheets"""
        if len(p) == 2 :
            p[0] = Tss( p.parser, p[1] )
        elif len(p) == 3 :
            p[0] = Tss( p.parser, p[1] )

    def p_stylesheets_1( self, p ) :
        """stylesheets  : stylesheet"""
        p[0] = StyleSheets( p.parser, None, p[1] )

    def p_stylesheets_2( self, p ) :
        """stylesheets  : stylesheets stylesheet"""
        p[0] = StyleSheets( p.parser, p[1], p[2] )

    def p_stylesheet( self, p ) :
        """stylesheet   : charset
                        | import
                        | namespace
                        | statement
                        | cdatas"""
        p[0] = StyleSheet( p.parser, p[1] )

    def p_statement( self, p ) :
        """statement    : ruleset
                        | media
                        | atrule
                        | page
                        | font_face
                        | wc"""
        p[0] = Statement( p.parser, p[1] )

    #---- @charset 

    def p_charset( self, p ) :
        """charset      : charset_sym string SEMICOLON"""
        p[0] = Charset( p.parser, p[1], p[2], SEMICOLON(p.parser, p[3]) )

    #---- @import

    def p_import( self, p ) :
        """import       : import_sym string mediums SEMICOLON
                        | import_sym string SEMICOLON
                        | import_sym uri mediums SEMICOLON
                        | import_sym uri SEMICOLON"""
        args = [ p[1], p[2], p[3], SEMICOLON(p.parser, p[4])
               ] if len(p) == 5 else [ p[1],p[2],None,SEMICOLON(p.parser,p[3]) ]
        p[0] = Import( p.parser, *args )

    #---- @namespace

    def p_namespace_1( self, p ) :
        """namespace    : namespace_sym nmprefix string SEMICOLON
                        | namespace_sym nmprefix uri SEMICOLON"""
        x = SEMICOLON(p.parser, p[4])
        p[0] = Namespace( p.parser, p[1], p[2], p[3], x )

    def p_namespace_2( self, p ) :
        """namespace    : namespace_sym string SEMICOLON
                        | namespace_sym uri SEMICOLON"""
        x = SEMICOLON(p.parser, p[4])
        p[0] = Namespace( p.parser, p[1], None, p[2], x )

    def p_nmprefix( self, p ) :
        """nmprefix : ident"""
        p[0] = Nameprefix( p.parser, p[1] )

    #---- atrule

    # Gotcha : Handle generic at-rules
    def p_atrule_1( self, p ) :
        """atrule       : atkeyword expr block"""
        p[0] = AtRule( p.parser, p[1], expr=p[2], block=p[3] )

    def p_atrule_2( self, p ) :
        """atrule       : atkeyword expr SEMICOLON"""
        p[0] = AtRule( p.parser, p[1], expr=p[2],
                       semicolon=SEMICOLON(p.parser, p[3]) )

    def p_atrule_3( self, p ) :
        """atrule       : atkeyword block"""
        p[0] = AtRule( p.parser, p[1], block=p[2] )

    def p_atrule_4( self, p ) :
        """atrule       : atkeyword SEMICOLON"""
        p[0] = AtRule( p.parser, p[1], semicolon=SEMICOLON(p.parser, p[2]) )

    def p_atrule_5( self, p ) :
        """atrule       : atkeyword expr openbrace rulesets CLOSEBRACE"""
        c = CLOSEBRACE( p.parser, p[5] )
        p[0] = AtRule( p.parser, p[1], expr=p[2], obrace=p[3], rulesets=p[4],
                       cbrace=c )

    def p_atrule_6( self, p ) :
        """atrule       : atkeyword openbrace rulesets CLOSEBRACE"""
        c = CLOSEBRACE( p.parser, p[4] )
        p[0] = AtRule( p.parser, p[1], obrace=p[2], rulesets=p[3], cbrace=c )

    #---- media

    def p_media_1( self, p ) :
        """media        : media_sym mediums openbrace rulesets CLOSEBRACE"""
        cbrc = CLOSEBRACE( p.parser, p[5] )
        p[0] = Media( p.parser, p[1], p[2], p[3], p[4], cbrc )

    def p_media_2( self, p ) :
        """media        : media_sym mediums openbrace CLOSEBRACE"""
        cbrc = CLOSEBRACE( p.parser, p[4] )
        p[0] = Media( p.parser, p[1], p[2], p[3], None, cbrc )


    def p_mediums( self, p ) :
        """mediums      : medium
                        | mediums medium
                        | mediums comma medium"""
        if len(p) == 4 :
            args = [ p[1], p[2], p[3] ]
        else :
            args = [ p[1], None, p[2] ] if len(p) == 3 else [ None, None, p[1] ]
        p[0] = Mediums( p.parser, *args )


    def p_medium( self, p ) :
        """medium       : expr
                        | any"""
        p[0] = Medium( p.parser, p[1] )

    #---- page

    def p_page_1( self, p ) :
        """page         : page_sym IDENT pseudo_page block"""
        p[0] = Page( p.parser, p[1], IDENT(p.parser, p[2]), p[3], p[4] )

    def p_page_2( self, p ) :
        """page         : page_sym ident block
                        | page_sym pseudo_page block"""
        p[0] = Page( p.parser, p[1], None, p[2], p[3] )

    def p_pseudo_page( self, p ) :
        """pseudo_page  : COLON ident"""
        p[0] = PseudoPage( p.parser, COLON(p.parser, p[1]), p[2] )

    #---- font_face

    def p_font_face( self, p ) :
        """font_face    : font_face_sym block"""
        p[0] = FontFace( p.parser, p[1], p[2] )

    #---- ruleset

    def p_rulesets( self, p ) :
        """rulesets     : ruleset 
                        | rulesets ruleset"""
        args = [ p[1], p[2] ] if len(p) == 3 else [ None, p[1] ]
        p[0] = RuleSets( p.parser, *args )

    def p_ruleset( self, p ) :
        """ruleset      : block 
                        | selectors block"""
        args = [ p[1], p[2] ] if len(p) == 3 else [ None, p[1] ]
        p[0] = RuleSet( p.parser, *args )

    def p_selectors_1( self, p ) :
        """selectors    : selector"""
        p[0] = Selectors( p.parser, p[1], None, None )

    def p_selectors_2( self, p ) :
        """selectors    : selectors comma"""
        p[0] = Selectors( p.parser, p[1], p[2], None )

    def p_selectors_3( self, p ) :
        """selectors    : selectors comma selector"""
        p[0] = Selectors( p.parser, p[1], p[2], p[3] )

    def p_selector( self, p ) :
        """selector     : simple_selector
                        | selector simple_selector
                        | selector combinator simple_selector"""
        if len(p) == 4 :
            args = [ p[1], p[2], p[3] ]
        elif len(p) == 3 :
            args = [ p[1], None, p[2] ]
        else :
            args = [ None, None, p[1] ]
        p[0] = Selector( p.parser, *args )

    def p_simple_selector_1( self, p ) :
        """simple_selector  : element_name"""
        p[0] = SimpleSelector( p.parser, None, p[1], None )

    def p_simple_selector_2( self, p ) :
        """simple_selector  : extender"""
        p[0] = SimpleSelector( p.parser, None, None, p[1] )

    def p_simple_selector_3( self, p ) :
        """simple_selector  : simple_selector extender"""
        p[0] = SimpleSelector( p.parser, p[1], None, p[2] )

    def p_element_name_1( self, p ) :
        """element_name : ident"""
        p[0] = ElementName( p.parser, p[1] )

    def p_element_name_2( self, p ) :
        """element_name : star"""
        p[0] = ElementName( p.parser, p[1] )

    def p_extender( self, p ) :
        """extender     : hash
                        | class
                        | attrib
                        | pseudo"""
        p[0] = Extender( p.parser, p[1] )

    def p_class( self, p ) :
        """class        : DOT IDENT
                        | DOT IDENT wc"""
        x = [ (DOT, 1), (IDENT, 2) ]
        x.append( p[3] if len(p) == 4 else None )
        p[0] = Class( p.parser, *self._buildterms( p, x ) )

    def p_attrib_1( self, p ) :
        """attrib       : opensqr ident attr_oper attr_val closesqr"""
        p[0] = Attrib( p.parser, p[1], p[2], p[3], p[4], p[5] )

    def p_attrib_2( self, p ) :
        """attrib       : opensqr ident closesqr"""
        p[0] = Attrib( p.parser, p[1], p[2], None, None, p[3] )

    def p_attroper( self, p ) :
        """attr_oper    : equal
                        | includes
                        | dashmatch
                        | beginmatch
                        | endmatch
                        | contain"""
        p[0] = AttrOper( p.parser, p[1] )

    def p_attrval( self, p ) :
        """attr_val     : ident
                        | string"""
        p[0] = AttrVal( p.parser, p[1] )

    def p_pseudo( self, p ) :
        """pseudo       : COLON pseudo_name
                        | COLON COLON pseudo_name"""
        args = [ COLON(p.parser, p[1]), COLON(p.parser, p[2]), p[3] 
               ] if len(p) == 4 else [ COLON(p.parser, p[1]), None, p[2] ]
        p[0] = Pseudo( p.parser, *args )

    def p_pseudoname_1( self, p ) :
        """pseudo_name  : ident"""
        p[0] = PseudoName( p.parser, None, p[1], None )

    def p_pseudoname_2( self, p ) :
        """pseudo_name  : function simple_selector closeparan
                        | function string closeparan
                        | function number closeparan"""
        p[0] = PseudoName( p.parser, p[1], p[2], p[3] )

    #---- block

    #def p_blocks( self, p ) :
    #    """blocks       : block
    #                    | blocks block"""
    #    args = [ p[1], p[2] ] if len(p) == 3 else [ None, p[1] ]
    #    p[0] = Blocks( p.parser, *args )

    def p_block( self, p ) :
        """block        : openbrace declarations closebrace
                        | openbrace closebrace"""
        args = [ p[1], p[2], p[3] ] if len(p) == 4 else [ p[1], None, p[2] ]
        p[0] = Block( p.parser, *args )

    def p_declarations( self, p ) :
        """declarations : declaration
                        | declarations semicolon
                        | declarations semicolon declaration"""
        if len(p) == 4 :
            args = [ p[1], p[2], p[3] ]
        elif len(p) == 3 :
            args = [ p[1], p[2], None ]
        else :
            args = [ None, None, p[1] ]
        p[0] = Declarations( p.parser, *args )

    def p_declaration_1( self, p ) :
        """declaration  : ident colon expr prio
                        | ident colon expr"""
        args = [ None, p[1], p[2], p[3], p[4] 
               ] if len(p) == 5 else [ None, p[1], p[2], p[3], None ]
        p[0] = Declaration( p.parser, *args )

    def p_declaration_2( self, p ) :
        """declaration  : star ident colon expr prio
                        | star ident colon expr"""
        args = [ p[1], p[2], p[3], p[4], p[5] 
               ] if len(p) == 6 else [ p[1], p[2], p[3], p[4], None ]
        p[0] = Declaration( p.parser, *args )

    def p_prio( self, p ) :
        """prio         : important_sym"""
        p[0] = Priority( p.parser, p[1] )

    #---- expr

    def p_expr( self, p ) :
        """expr         : binaryexpr
                        | expr binaryexpr"""
        args = [ p[1], p[2] ] if len(p) == 3 else [ None,  p[1] ]
        p[0] = Expr( p.parser, *args )

    def p_binaryexpr( self, p ) :
        """binaryexpr   : term
                        | unaryexpr
                        | binaryexpr operator binaryexpr"""
        args = [ None, None, None, p[1] 
               ] if len(p) == 2 else [ p[1], p[2], p[3], None ]
        p[0] = BinaryExpr( p.parser, *args )

    def p_unaryexpr_1( self, p ) :
        """unaryexpr    : openparan expr closeparan"""
        p[0] = UnaryExpr( p.parser, None, None, (p[1], p[2], p[3]) )

    def p_unaryexpr_2( self, p ) :
        """unaryexpr    : plus term_val %prec UNARY
                        | minus term_val %prec UNARY"""
        p[0] = UnaryExpr( p.parser, p[1], p[2], None )

    def p_term( self, p ) :
        """term         : term_val
                        | string
                        | ident
                        | uri
                        | unicoderange
                        | hash"""
        # Note : here hash should be hex-color #[0-9a-z]{3} or #[0-9a-z]{6}
        # Perform the contstraint check inside the `Term` class
        p[0] = Term( p.parser, p[1])

    def p_term_val( self, p ) :
        """term_val     : number
                        | percentage
                        | ems
                        | exs
                        | length
                        | angle
                        | time
                        | freq
                        | func"""
        p[0] = TermVal( p.parser, p[1] )
                         
    #def p_term_dimen( self, p ) :
    #    """term_val     : dimen"""
    #    p[0] = TermVal( p.parser, p[1] )

    def p_func( self, p ) :
        """func         : function expr closeparan
                        | function closeparan"""
        args = [ p[1], p[2], p[3] ] if len(p) == 4 else [ p[1], None, p[2] ]
        p[0] = Func( p.parser, *args )

    # Note : `operator` should never be a `SEMICOLON`,
    #        as per CSS3 grammar only, fwdslash and comma are real operators
    def p_operator( self, p ) :
        """operator     : fwdslash
                        | comma
                        | colon
                        | dot
                        | equal
                        | gt
                        | lt
                        | plus
                        | minus
                        | star
                        | dlimit"""
        p[0] = Operator( p.parser, p[1] )

    #def p_unary_oper( self, p ) :
    #    """unary_oper   : plus
    #                    | minus"""
    #    p[0] = Unary( p.parser, p[1] )

    def p_combinator( self, p ) :
        """combinator   : plus
                        | gt
                        | tilda"""
        p[0] = Combinator( p.parser, p[1] )

    def p_cdatas( self, p ) :
        """cdatas       : cdata
                        | cdatas cdata"""
        args = [ p[1], p[2] ] if len(p) == 3 else [ None,  p[1] ]
        p[0] = Cdatas( p.parser, *args )

    def p_cdata( self, p ) :
        """cdata        : cdo cdc
                        | cdo cdata_conts cdc"""
        args = [ p[1], p[2], p[3] ] if len(p) == 4 else [ p[1], None, p[2] ]
        p[0] = Cdata( p.parser, *args )

    def p_cdata_conts( self, p ) :
        """cdata_conts  : cdata_cont
                        | cdata_conts cdata_cont"""
        args = [ p[1], p[2] ] if len(p) == 3 else [ None, p[1] ]
        p[0] = CdataConts( p.parser, *args )

    def p_cdata_cont( self, p ) :
        """cdata_cont   : expr
                        | any
                        | operator
                        | block"""
        p[0] = CdataCont( p.parser, p[1] )

    #---- Terminals with whitespace

    def p_charset_sym( self, p ) :
        """charset_sym  : CHARSET_SYM wc
                        | CHARSET_SYM"""
        t = CHARSET_SYM( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_import_sym( self, p ) :
        """import_sym   : IMPORT_SYM wc
                        | IMPORT_SYM"""
        t = IMPORT_SYM( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_namespace_sym( self, p ) :
        """namespace_sym : NAMESPACE_SYM wc
                         | NAMESPACE_SYM"""
        t = NAMESPACE_SYM( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_media_sym( self, p ) :
        """media_sym    : MEDIA_SYM wc
                        | MEDIA_SYM"""
        t = MEDIA_SYM( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_page_sym( self, p ) :
        """page_sym     : PAGE_SYM wc
                        | PAGE_SYM"""
        t = PAGE_SYM( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_font_face_sym( self, p ) :
        """font_face_sym : FONT_FACE_SYM wc
                         | FONT_FACE_SYM"""
        t = FONT_FACE_SYM( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_important_sym( self, p ) :
        """important_sym : IMPORTANT_SYM wc
                         | IMPORTANT_SYM"""
        t = IMPORTANT_SYM( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_atkeyword( self, p ) :
        """atkeyword    : ATKEYWORD wc
                        | ATKEYWORD"""
        t = ATKEYWORD( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_string( self, p ) :
        """string       : STRING wc
                        | STRING"""
        t = STRING( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_uri( self, p ) :
        """uri          : URI wc
                        | URI"""
        t = URI( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_function( self, p ) :
        """function     : FUNCTION wc
                        | FUNCTION"""
        t = FUNCTION( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_unicoderange( self, p ) :
        """unicoderange : UNICODERANGE wc
                        | UNICODERANGE"""
        t = UNICODERANGE( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_ident( self, p ) :
        """ident        : IDENT wc
                        | IDENT"""
        t = IDENT( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_number( self, p ) :
        """number       : NUMBER wc
                        | NUMBER"""
        t = NUMBER( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_percentage( self, p ) :
        """percentage   : PERCENTAGE wc
                        | PERCENTAGE"""
        t = PERCENTAGE( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_ems( self, p ) :
        """ems          : EMS wc
                        | EMS"""
        t = EMS( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_exs( self, p ) :
        """exs          : EXS wc
                        | EXS"""
        t = EXS( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_length( self, p ) :
        """length       : LENGTH wc
                        | LENGTH"""
        cls, val = p[1]
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, cls(p.parser, val), wc )

    def p_angle( self, p ) :
        """angle        : ANGLE wc
                        | ANGLE"""
        cls, val = p[1]
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, cls(p.parser, val), wc )

    def p_time( self, p ) :
        """time         : TIME wc
                        | TIME"""
        cls, val = p[1]
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, cls(p.parser, val), wc )

    def p_freq( self, p ) :
        """freq         : FREQ wc
                        | FREQ"""
        cls, val = p[1]
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, cls(p.parser, val), wc )

    def p_fwdslash( self, p ) :
        """fwdslash     : FWDSLASH wc
                        | FWDSLASH"""
        t = FWDSLASH( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_comma( self, p ) :
        """comma        : COMMA wc
                        | COMMA"""
        t = COMMA( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_hash( self, p ) :
        """hash         : HASH wc
                        | HASH"""
        t = HASH( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_equal( self, p ) :
        """equal        : EQUAL wc
                        | EQUAL"""
        t = EQUAL( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_includes( self, p ) :
        """includes     : INCLUDES wc
                        | INCLUDES"""
        t = INCLUDES( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_dashmatch( self, p ) :
        """dashmatch    : DASHMATCH wc
                        | DASHMATCH"""
        t = DASHMATCH( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_beginmatch( self, p ) :
        """beginmatch   : BEGINMATCH wc
                        | BEGINMATCH"""
        t = BEGINMATCH( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_endmatch( self, p ) :
        """endmatch     : ENDMATCH wc
                        | ENDMATCH"""
        t = ENDMATCH( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_contain( self, p ) :
        """contain      : CONTAIN wc
                        | CONTAIN"""
        t = CONTAIN( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_plus( self, p ) :
        """plus         : PLUS wc
                        | PLUS"""
        t = PLUS( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_minus( self, p ) :
        """minus        : MINUS wc
                        | MINUS"""
        t = MINUS( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_gt( self, p ) :
        """gt           : GT wc
                        | GT"""
        t = GT( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_lt( self, p ) :
        """lt           : LT wc
                        | LT"""
        t = LT( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_tilda( self, p ) :
        """tilda        : TILDA wc
                        | TILDA"""
        t = TILDA( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_colon( self, p ) :
        """colon        : COLON wc
                        | COLON"""
        t = COLON( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_semicolon( self, p ) :
        """semicolon    : SEMICOLON wc
                        | SEMICOLON"""
        t = SEMICOLON( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_star( self, p ) :
        """star         : STAR wc
                        | STAR"""
        t = STAR( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_dot( self, p ) :
        """dot          : DOT wc
                        | DOT"""
        t = DOT( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_dlimit( self, p ) :
        """dlimit       : DLIMIT wc
                        | DLIMIT"""
        t = DLIMIT( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_openbrace( self, p ) :
        """openbrace    : OPENBRACE wc
                        | OPENBRACE"""
        t = OPENBRACE( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_closebrace( self, p ) :
        """closebrace   : CLOSEBRACE wc
                        | CLOSEBRACE"""
        t = CLOSEBRACE( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_opensqr( self, p ) :
        """opensqr      : OPENSQR wc
                        | OPENSQR"""
        t = OPENSQR( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_closesqr( self, p ) :
        """closesqr     : CLOSESQR wc
                        | CLOSESQR"""
        t = OPENSQR( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_openparan( self, p ) :
        """openparan    : OPENPARAN wc
                        | OPENPARAN"""
        t = OPENPARAN( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_closeparan( self, p ) :
        """closeparan   : CLOSEPARAN wc
                        | CLOSEPARAN"""
        t = CLOSEPARAN( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_wc_1( self, p ) :
        """wc           : S
                        | wc S"""
        args = [ p[1], S(p.parser, p[2]), None 
               ] if len(p) == 3 else  [ None, S(p.parser, p[1]), None ]
        p[0] = WC( p.parser, *args )

    def p_wc_2( self, p ) :
        """wc           : COMMENT
                        | wc COMMENT"""
        args = [ p[1], None, COMMENT(p.parser, p[2])
               ] if len(p) == 3 else  [ None, None, COMMENT(p.parser, p[1]) ]
        p[0] = WC( p.parser, *args )

    def p_cdo( self, p ) :
        """cdo          : CDO wc
                        | CDO"""
        t = CDO( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    def p_cdc( self, p ) :
        """cdc          : CDC wc
                        | CDC"""
        t = CDC( p.parser, p[1] )
        wc = p[2] if len(p) == 3 else None
        p[0] = TerminalS( p.parser, t, wc )

    #---- For confirmance with forward compatible CSS

    def p_any( self, p) :
        """any          : opensqr   expr closesqr"""
        p[0] = Any( p.parser, p[1], p[2], p[3] )

    def p_error( self, p ):
        if p:
            column = self.tsslex._find_tok_column( p )
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


if __name__ == "__main__":
    import pprint, time
    
    text   = open(sys.argv[1]).read() if len(sys.argv) > 1 else "hello" 
    parser = TSSParser(
                lex_optimize=True, yacc_debug=True, yacc_optimize=False
             )
    t1     = time.time()
    # set debuglevel to 2 for debugging
    t = parser.parse( text, 'x.c', debuglevel=2 )
    t.show( showcoord=True )
    print time.time() - t1
