# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

"""Parser grammer for Tayra Template Language"""

# -*- coding: utf-8 -*-

# Gotcha : None
# Notes  :
# Todo   : 

import logging, re, sys, copy
from   types                import StringType
from   os.path              import splitext, dirname
from   hashlib              import sha1
from   StringIO             import StringIO

import ply.yacc
from   tayra.ttl.lexer      import TTLLexer
from   tayra.ttl.ast        import *

log = logging.getLogger( __name__ )
rootdir = dirname( __file__ )

class ParseError( Exception ):
    pass

class TTLParser( object ):

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
        Create a new TTLParser.

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
        self.debug = lex_debug or yacc_debug or debug

        # Build Lexer
        self.ttllex = TTLLexer( error_func=self._lex_error_func )
        kwargs = {'optimize' : lex_optimize} if lex_optimize != None else {}
        kwargs.update({ 'debug' : lex_debug }) if lex_debug else None
        self.ttllex.build( lextab=lextab, **kwargs )
        self.tokens = self.ttllex.tokens

        # Build Yaccer
        kwargs = {'optimize' : yacc_optimize} if yacc_optimize != None else {}
        kwargs.update({ 'debug' : yacc_debug }) if yacc_debug else None
        self.parser = ply.yacc.yacc(
            module=self, tabmodule=yacctab, outputdir=outputdir, **kwargs
        )
        self.parser.ttlparser = self     # For AST nodes to access `this`

        # Parser initialization
        self._initialize()

    def _initialize( self ) :
        self.ttlfile = None
        pass

    def parse( self, text, ttlfile='', debuglevel=0 ):
        """Parse tayra templage language and creates an AST tree. For every
        parsing invocation, the same lex, yacc, app options and objects will
        be used.

        : ttlfile ::
            Name of the file being parsed (for meaningful error messages)
        : debuglevel ::
            Debug level to yacc
        """
        # Parser Initialize
        self._initialize()

        self.ttllex.ttlfile = self.ttlfile = ttlfile
        self.ttllex.reset_lineno()
        self.hashtext = sha1( text ).hexdigest()

        # parse and get the Translation Unit
        debuglevel = self.debug or debuglevel
        self.tu = self.parser.parse( text, lexer=self.ttllex, debug=debuglevel )
        return self.tu

    # ------------------------- Private functions -----------------------------

    def _lex_error_func( self, lex, msg, line, column ):
        self._parse_error( msg, self._coord( line, column ))
    
    def _coord( self, lineno, column=None ):
        return Coord( file=self.ttllex.filename, 
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
        ('left', 'SPECIFIER'),
        ('left', 'EQUAL')
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

    def p_template_1( self, p ) :
        """template : siblings"""
        p[0] = Template( p.parser, None, p[1] )

    def p_template_2( self, p ) :
        """template : prologs"""
        p[0] = Template( p.parser, p[1], None )

    def p_template_3( self, p ) :
        """template : prologs siblings"""
        p[0] = Template( p.parser, p[1], p[2] )

    def p_prologs( self, p ) :
        """prologs  : prolog
                    | prologs prolog"""
        args = [ p[1], p[2] ] if len(p) == 3 else [ None, p[1] ]
        p[0] = Prologs( p.parser, *args )

    def p_prolog( self, p ) :
        """prolog   : doctype
                    | body
                    | importas
                    | inherit
                    | implement
                    | use"""
        p[0] = Prolog( p.parser, p[1] )

    def p_siblings( self, p ) :
        """siblings : sibling
                    | siblings sibling"""
        args = [ p[1], p[2] ] if len(p) == 3 else [ None, p[1] ]
        p[0] = Siblings( p.parser, *args )

    def p_sibling( self, p ) :
        """sibling  : statement
                    | commentline
                    | interfaceblock
                    | tagline
                    | textline
                    | tagblock
                    | filterblock
                    | functionblock
                    | ifelfiblock
                    | forblock
                    | whileblock"""
        p[0] = Sibling( p.parser, p[1] )

    #---- Prologs

    def p_doctype( self, p ) :
        """doctype      : DOCTYPE whitespace"""
        p[0] = DocType( p.parser, DOCTYPE(p.parser, p[1]), p[2] )

    def p_body( self, p ) :
        """body         : BODY whitespace"""
        p[0] = Body( p.parser, BODY(p.parser, p[1]), p[2] )

    def p_importas( self, p ) :
        """importas     : IMPORTAS whitespace"""
        p[0] = ImportAs( p.parser, IMPORTAS(p.parser, p[1]), p[2] )

    def p_implement( self, p ) :
        """implement    : IMPLEMENT whitespace"""
        p[0] = Implement( p.parser, IMPLEMENT(p.parser, p[1]), p[2] )

    def p_inherit( self, p ) :
        """inherit      : INHERIT whitespace"""
        p[0] = Inherit( p.parser, INHERIT(p.parser, p[1]), p[2] )

    def p_use( self, p ) :
        """use          : USE whitespace"""
        p[0] = Use( p.parser, USE(p.parser, p[1]), p[2] )

    #---- Filter block

    def p_filterblock( self, p ) :
        """filterblock      : FILTER INDENT siblings DEDENT
                            | FILTER"""
        terms = [ (FILTER,1), (INDENT,2), p[3], (DEDENT,4) 
                ] if len(p) == 5 else [ (FUNCTION,1), None, None, None ]
        p[0] = FilterBlock( p.parser, *self._buildterms( p, terms ) )

    #---- Function block / Interface block

    def p_functionblock( self, p ) :
        """functionblock    : FUNCTION INDENT siblings DEDENT
                            | FUNCTION"""
        terms = [ (FUNCTION,1), (INDENT,2), p[3], (DEDENT,4) 
                ] if len(p) == 5 else [ (FUNCTION,1), None, None, None ]
        p[0] = FunctionBlock( p.parser, *self._buildterms(p, terms) )

    def p_interfaceblock( self, p ) :
        """interfaceblock   : INTERFACE INDENT siblings DEDENT
                            | INTERFACE"""
        terms = [ (INTERFACE,1), (INDENT,2), p[3], (DEDENT,4) 
                ] if len(p) == 5 else [ (INTERFACE,1), None, None, None ]
        p[0] = InterfaceBlock( p.parser, *self._buildterms(p, terms) )

    #---- Control blocks  ( if-elif-else / for / while )

    def p_ifelfiblock_1( self, p ) :
        """ifelfiblock  : ifblock"""
        p[0] = IfelfiBlock( p.parser, None, p[1], None, None )

    def p_ifelfiblock_2( self, p ) :
        """ifelfiblock  : ifelfiblock elifblock"""
        p[0] = IfelfiBlock( p.parser, p[1], None, p[2], None )

    def p_ifelfiblock_3( self, p ) :
        """ifelfiblock  : ifelfiblock elseblock"""
        p[0] = IfelfiBlock( p.parser, p[1], None, None, p[2] )

    def p_ifblock( self, p ) :
        """ifblock      : IF INDENT siblings DEDENT"""
        terms = [ (IF,1), (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = IfBlock( p.parser, *self._buildterms(p, terms) )

    def p_elifblock( self, p ) :
        """elifblock    : ELIF INDENT siblings DEDENT"""
        terms = [ (ELIF,1), (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = ElifBlock( p.parser, *self._buildterms(p, terms) )

    def p_elseblock( self, p ) :
        """elseblock    : ELSE INDENT siblings DEDENT"""
        terms = [ (ELSE,1), (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = ElseBlock( p.parser, *self._buildterms(p, terms) )

    def p_forblock( self, p ) :
        """forblock     : FOR INDENT siblings DEDENT"""
        terms = [ (FOR,1), (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = ForBlock( p.parser, *self._buildterms(p, terms) )

    def p_whileblock( self, p ) :
        """whileblock   : WHILE INDENT siblings DEDENT"""
        terms = [ (WHILE,1), (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = WhileBlock( p.parser, *self._buildterms(p, terms) )

    #---- Template language

    def p_tagblock( self, p ) :
        """tagblock     : tagline INDENT siblings DEDENT"""
        terms = [ p[1], (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = TagBlock( p.parser, *self._buildterms( p, terms ) )

    def p_commentline( self, p ) :
        """commentline  : COMMENT"""
        p[0] = CommentLine( p.parser, COMMENT(p.parser, p[1]) )

    def p_statement( self, p ) :
        """statement    : STATEMENT"""
        p[0] = Statement( p.parser, STATEMENT(p.parser, p[1]) )

    def p_tagline_1( self, p ) :
        """tagline      : tag NEWLINES"""
        p[0] = TagLine( p.parser, p[1], None, NEWLINES(p.parser, p[2]) )

    def p_tagline_2( self, p ) :
        """tagline      : tag contents NEWLINES"""
        p[0] = TagLine( p.parser, p[1], p[2], NEWLINES(p.parser, p[3]) )

    def p_textline( self, p ) :
        """textline     : contents NEWLINES"""
        p[0] = Textline( p.parser, p[1], NEWLINES(p.parser, p[2]) )

    #---- Tag

    def p_tag_1( self, p ) :
        """tag      : TAGOPEN specifiers style attributes TAGEND"""
        terms = [ (TAGOPEN,1), p[2], p[3], p[4], (TAGEND,5), None ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_2( self, p ) :
        """tag      : TAGOPEN specifiers style attributes TAGCLOSE"""
        terms = [ (TAGOPEN,1), p[2], p[3], p[4], None, (TAGCLOSE,5) ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_3( self, p ) :
        """tag      : TAGOPEN style attributes TAGEND"""
        terms = [ (TAGOPEN,1), None, p[2], p[3], (TAGEND,4), None ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_4( self, p ) :
        """tag      : TAGOPEN style attributes TAGCLOSE"""
        terms = [ (TAGOPEN,1), None, p[2], p[3], None, (TAGCLOSE,4) ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_5( self, p ) :
        """tag      : TAGOPEN specifiers attributes TAGEND"""
        terms = [ (TAGOPEN,1), p[2], None, p[3], (TAGEND,4), None ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_6( self, p ) :
        """tag      : TAGOPEN specifiers attributes TAGCLOSE"""
        terms = [ (TAGOPEN,1), p[2], None, p[3], None, (TAGCLOSE,4) ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_7( self, p ) :
        """tag      : TAGOPEN specifiers style TAGEND"""
        terms = [ (TAGOPEN,1), p[2], p[3], None, (TAGEND,4), None ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_8( self, p ) :
        """tag      : TAGOPEN specifiers style TAGCLOSE"""
        terms = [ (TAGOPEN,1), p[2], p[3], None, None, (TAGCLOSE,4) ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_9( self, p ) :
        """tag      : TAGOPEN style TAGEND"""
        terms = [ (TAGOPEN,1), None, p[2], None, (TAGEND,3), None ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_10( self, p ) :
        """tag      : TAGOPEN style TAGCLOSE"""
        terms = [ (TAGOPEN,1), None, p[2], None, None, (TAGCLOSE,3) ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_11( self, p ) :
        """tag      : TAGOPEN specifiers TAGEND"""
        terms = [ (TAGOPEN,1), p[2], None, None, (TAGEND,3), None ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_12( self, p ) :
        """tag      : TAGOPEN specifiers TAGCLOSE"""
        terms = [ (TAGOPEN,1), p[2], None, None, None, (TAGCLOSE,3) ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_13( self, p ) :
        """tag      : TAGOPEN attributes TAGEND"""
        terms = [ (TAGOPEN,1), None, None, p[2], (TAGEND,3), None ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_14( self, p ) :
        """tag      : TAGOPEN attributes TAGCLOSE"""
        terms = [ (TAGOPEN,1), None, None, p[2], None, (TAGCLOSE,3) ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_15( self, p ) :
        """tag      : TAGOPEN TAGEND"""
        terms = [ (TAGOPEN,1), None, None, None, (TAGEND,2), None ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    def p_tag_16( self, p ) :
        """tag      : TAGOPEN TAGCLOSE"""
        terms = [ (TAGOPEN,1), None, None, None, None, (TAGCLOSE,2) ]
        p[0] = Tag( p.parser, *self._buildterms(p, terms) )

    #---- Attributes

    def p_attributes_1( self, p ) :
        """attributes   : attr
                        | attributes whitespace attr"""
        args = [ p[1], p[2], p[3] ] if len(p) == 4 else [ None, None, p[1] ]
        p[0] = Attributes( p.parser, *args )

    def p_attr( self, p ) :
        """attr         : specifiers EQUAL smartstring %prec EQUAL"""
        p[0] = Attr( p.parser, p[1], EQUAL(p.parser, p[2]), p[3] )

    #---- Content

    def p_contents_1( self, p ) :
        """contents     : content"""
        p[0] = Contents( p.parser, None, p[1] )

    def p_contents_2( self, p ) :
        """contents     : contents content"""
        p[0] = Contents( p.parser, p[1], p[2] )

    def p_content_1( self, p ) :
        """content      : TEXT"""
        p[0] = Content( p.parser, TEXT(p.parser, p[1]), None )

    def p_content_2( self, p ) :
        """content      : SPECIALCHARS"""
        p[0] = Content( p.parser, SPECIALCHARS(p.parser, p[1]), None )

    def p_content_3( self, p ) :
        """content      : ATOM"""
        p[0] = Content( p.parser, ATOM(p.parser, p[1]), None )

    def p_content_4( self, p ) :
        """content      : S"""
        p[0] = Content( p.parser, S(p.parser, p[1]), None )

    def p_content_5( self, p ) :
        """content      : exprs"""
        p[0] = Content( p.parser, None, p[1] )

    #---- Specifier

    def p_specifiers_1( self, p ) :
        """specifiers   : specifier"""
        p[0] = Specifiers( p.parser, None, None, p[1] )

    def p_specifiers_2( self, p ) :
        """specifiers   : specifiers specifier %prec SPECIFIER"""
        p[0] = Specifiers( p.parser, p[1], None, p[2] )

    def p_specifiers_3( self, p ) :
        """specifiers   : specifiers whitespace specifier %prec SPECIFIER"""
        p[0] = Specifiers( p.parser, p[1], p[2], p[3] )

    def p_specifier_1( self, p ) :
        """specifier    : ATOM"""
        p[0] = Specifier( p.parser, ATOM(p.parser, p[1]), None, None )

    def p_specifier_2( self, p ) :
        """specifier    : smartstring"""
        p[0] = Specifier( p.parser, None, p[1], None )

    def p_specifier_3( self, p ) :
        """specifier    : exprs"""
        p[0] = Specifier( p.parser, None, None, p[1] )

    #---- SmartString

    def p_smartstring_1( self, p ) :
        """smartstring  : SQUOTE strcontents SQUOTE"""
        terms = [ (SQUOTE,1), p[2], (SQUOTE,3) ]
        p[0] = SmartString( p.parser, *self._buildterms(p, terms) )

    def p_smartstring_2( self, p ) :
        """smartstring  : SQUOTE SQUOTE"""
        terms = [ (SQUOTE,1), None, (SQUOTE,2) ]
        p[0] = SmartString( p.parser, *self._buildterms(p, terms) )

    def p_smartstring_3( self, p ) :
        """smartstring  : DQUOTE strcontents DQUOTE"""
        terms = [ (DQUOTE,1), p[2], (DQUOTE,3) ]
        p[0] = SmartString( p.parser, *self._buildterms(p, terms) )

    def p_smartstring_4( self, p ) :
        """smartstring  : DQUOTE DQUOTE"""
        terms = [ (DQUOTE,1), None, (DQUOTE,2) ]
        p[0] = SmartString( p.parser, *self._buildterms(p, terms) )

    def p_strcontents( self, p ) :
        """strcontents  : strcontent
                        | strcontents strcontent"""
        args = [ p[1], p[2] ] if len(p) == 3 else [ None, p[1] ]
        p[0] = StrContent( p.parser,*args )

    def p_strcontent_1( self, p ) :
        """strcontent   : TEXT"""
        p[0] = StrContent( p.parser, TEXT(p.parser, p[1]), None )

    def p_strcontent_2( self, p ) :
        """strcontent   : SPECIALCHARS"""
        p[0] = StrContent( p.parser, SPECIALCHARS(p.parser, p[1]), None )

    def p_strcontent_3( self, p ) :
        """strcontent   : ATOM"""
        p[0] = StrContent( p.parser, ATOM(p.parser, p[1]), None )

    def p_strcontent_4( self, p ) :
        """strcontent   : whitespace"""
        p[0] = StrContent( p.parser, None, p[1] )

    def p_strcontent_5( self, p ) :
        """strcontent   : exprs"""
        p[0] = StrContent( p.parser, None, p[1] )

    #---- style

    def p_style( self, p ) :
        """style            : OPENBRACE stylecontents CLOSEBRACE"""
        p[0] = Style(
          p.parser, OPENBRACE(p.parser, p[1]), p[2], CLOSEBRACE(p.parser, p[3])
        )

    def p_stylecontents( self, p ) :
        """stylecontents    : style_content
                            | stylecontents style_content"""
        args = [ p[1], p[2] ] if len(p) == 3 else [ None, p[1] ]
        p[0] = StyleContents( p.parser, *args )

    def p_style_content_1( self, p ) :
        """style_content    : NEWLINES"""
        terms = [ (NEWLINES,1), None, None, None ]
        p[0] = StyleContent( p.parser, *self._buildterms(p, terms) )

    def p_style_content_2( self, p ) :
        """style_content    : S"""
        terms = [ None, (S,1), None, None ]
        p[0] = StyleContent( p.parser, *self._buildterms(p, terms) )

    def p_style_content_3( self, p ) :
        """style_content    : TEXT"""
        terms = [ None, None, (TEXT,1), None ]
        p[0] = StyleContent( p.parser, *self._buildterms(p, terms) )
                        
    def p_style_content_4( self, p ) :
        """style_content    : SPECIALCHARS"""
        terms = [ None, None, (SPECIALCHARS,1), None ]
        p[0] = StyleContent( p.parser, *self._buildterms(p, terms) )
                        
    def p_style_content_5( self, p ) :
        """style_content    : exprs"""
        terms = [ None, None, None, p[1] ]
        p[0] = StyleContent( p.parser, *self._buildterms(p, terms) )

    #---- Exprs

    def p_exprs( self, p ) :
        """exprs            : OPENEXPRS exprs_contents CLOSEBRACE"""
        terms = [ (OPENEXPRS,1), p[2], (CLOSEBRACE, 3) ]
        p[0] = Exprs( p.parser, *self._buildterms(p, terms) )

    def p_exprs_contents( self, p ) :
        """exprs_contents   : exprs_content
                            | exprs_contents exprs_content"""
        args = [ p[1], p[2] ] if len(p) == 3 else [ None, p[1] ]
        p[0] = ExprsContents( p.parser, *args )

    def p_exprs_content_1( self, p ) :
        """exprs_content    : NEWLINES"""
        terms = [ (NEWLINES,1), None, None, None ]
        p[0] = ExprsContent( p.parser, *self._buildterms(p, terms) )

    def p_exprs_content_2( self, p ) :
        """exprs_content    : S"""
        terms = [ None, (S,1), None, None ]
        p[0] = ExprsContent( p.parser, *self._buildterms(p, terms) )

    def p_exprs_content_3( self, p ) :
        """exprs_content    : STRING"""
        terms = [ None, None, (STRING,1), None ]
        p[0] = ExprsContent( p.parser, *self._buildterms(p, terms) )

    def p_exprs_content_4( self, p ) :
        """exprs_content    : TEXT"""
        terms = [ None, None, None, (TEXT,1) ]
        p[0] = ExprsContent( p.parser, *self._buildterms(p, terms) )

    def p_exprs_content_5( self, p ) :
        """exprs_content    : SPECIALCHARS"""
        terms = [ None, None, None, (SPECIALCHARS,1) ]
        p[0] = ExprsContent( p.parser, *self._buildterms(p, terms) )

    #----

    def p_whitespace_1( self, p ) :
        """whitespace   : NEWLINES
                        | whitespace NEWLINES"""
        args = [ p[1], NEWLINES(p.parser, p[2]), None
               ] if len(p) == 3 else [ None, NEWLINES(p.parser, p[1]), None ]
        p[0] = WhiteSpace( p.parser, *args )

    def p_whitespace_2( self, p ) :
        """whitespace   : S
                        | whitespace S"""
        args = [ p[1], None, S(p.parser, p[2])
               ] if len(p) == 3 else [ None, None, S(p.parser, p[1]) ]
        p[0] = WhiteSpace( p.parser, *args )
                        
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


if __name__ == "__main__":
    import pprint, time
    
    text   = open(sys.argv[1]).read() if len(sys.argv) > 1 else "hello" 
    parser = TTLParser(
                lex_optimize=True, yacc_debug=True, yacc_optimize=False
             )
    t1     = time.time()
    # set debuglevel to 2 for debugging
    t = parser.parse( text, 'x.c', debuglevel=2 )
    t.show( showcoord=True )
    print time.time() - t1
