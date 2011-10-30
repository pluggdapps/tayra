# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

"""Parser grammer for Tayra Template Language"""

# Gotcha : None
# Notes  :
# Todo   : 

import logging, re, sys, copy, codecs
from   types            import StringType
from   os.path          import splitext, dirname
from   hashlib          import sha1
from   StringIO         import StringIO
from   copy             import deepcopy

import ply.yacc
from   tayra.lexer      import TTLLexer
from   tayra.ast        import *

log = logging.getLogger( __name__ )
rootdir = dirname( __file__ )
LEXTAB = 'lextyrtab'
YACCTAB = 'parsetyrtab'

class ParseError( Exception ):
    pass

class TTLParser( object ):

    def __init__( self,
                  ttlconfig={},
                  outputdir=u'',
                  lex_debug=None,
                  yacc_debug=None,
                  debug=None
                ) :
        """
        Create a new TTLParser.

        : ttlconfig ::
            All configurations related to tayra templates, are represented in
            this object.

        : outputdir ::
            To change the directory in which the parsetab.py file (and other
            output files) are written.
                        
        : lex_debug ::
            PLY-Yacc option.

        : yacc_debug ::
            Generate a parser.out file that explains how yacc built the parsing
            table from the grammar.
        """
        self.debug = lex_debug or yacc_debug or debug
        optimize = ttlconfig.get( 'parse_optimize', False )
        lextab = ttlconfig.get( 'lextab', LEXTAB ) or LEXTAB
        yacctab = ttlconfig.get( 'yacctab', YACCTAB ) or YACCTAB
        # Build Lexer
        self.ttllex = TTLLexer( error_func=self._lex_error_func )
        kwargs = {'optimize' : optimize} if optimize else {}
        kwargs.update(debug=lex_debug)
        kwargs.update(lextab=lextab) if lextab else None
        self.ttllex.build( **kwargs )
        self.tokens = self.ttllex.tokens

        # Build Yaccer
        kwargs = {'optimize' : optimize} if optimize else {}
        kwargs.update(debug=yacc_debug)
        kwargs.update(outputdir=outputdir) if outputdir else None
        kwargs.update(tabmodule=yacctab)
        self.parser = ply.yacc.yacc( module=self, **kwargs )
        self.parser.ttlparser = self     # For AST nodes to access `this`

        # Parser initialization
        self._ttlconfig = ttlconfig
        self._initialize()

    def _initialize( self, ttlfile=None, ttlconfig={} ) :
        self.ttlfile = ttlfile
        self.ttlconfig = deepcopy( self._ttlconfig )
        self.ttlconfig.update( ttlconfig )
        self.ttllex.reset_lineno()

    def parse( self, text, ttlfile=None, ttlconfig={}, debuglevel=0 ):
        """Parse tayra templage language and creates an AST tree. For every
        parsing invocation, the same lex, yacc, app options and objects will
        be used.

        : ttlfile ::
            Name of the file being parsed (for meaningful error messages)
        : debuglevel ::
            Debug level to yacc
        """
        # Parser Initialize
        ttlfile = ttlfile if ttlfile != None else self.ttlfile
        self._initialize( ttlfile=ttlfile, ttlconfig=ttlconfig )

        self.ttllex.ttlfile = self.ttlfile = ttlfile

        # parse and get the Translation Unit
        debuglevel = self.debug or debuglevel
        self.tu = self.parser.parse( text, lexer=self.ttllex, debug=debuglevel )
        return self.tu

    # ------------------------- Private functions -----------------------------

    def _lex_error_func( self, lex, msg, line, column ):
        self._parse_error( msg, self._coord( line, column ))
    
    def _coord( self, lineno, column=None ):
        return Coord( file=self.ttllex.ttlfile, 
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
        """template : prologs"""
        p[0] = Template( p.parser, None, p[1], None )

    def p_template_2( self, p ) :
        """template : siblings"""
        p[0] = Template( p.parser, None, None, p[1] )

    def p_template_3( self, p ) :
        """template : dirtyblocks prologs siblings"""
        p[0] = Template( p.parser, p[1], p[2], p[3] )

    def p_template_4( self, p ) :
        """template : prologs siblings"""
        p[0] = Template( p.parser, None, p[1], p[2] )

    def p_template_5( self, p ) :
        """template : """
        p[0] = Template( p.parser, None, None, None )

    def p_prologs_1( self, p ) :
        """prologs  : prologs dirtyblocks prolog"""
        p[0] = Prologs( p.parser, p[1], p[2], p[3] )

    def p_prologs_2( self, p ) :
        """prologs  : prologs prolog"""
        p[0] = Prologs( p.parser, p[1], None, p[2] )

    def p_prologs_3( self, p ) :
        """prologs  : prolog"""
        p[0] = Prologs( p.parser, None, None, p[1] )

    def p_prolog( self, p ) :
        """prolog   : doctype
                    | charset
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
                    | pass
                    | tagline
                    | dirtyblocks
                    | textline
                    | interfaceblock
                    | textblock
                    | tagblock
                    | filterblock
                    | functionblock
                    | ifelfiblock
                    | forblock
                    | whileblock"""
        p[0] = Sibling( p.parser, p[1] )

    #---- Prologs

    def p_doctype( self, p ) :
        """doctype      : DOCTYPE"""
        p[0] = DocType( p.parser, DOCTYPE(p.parser, p[1]) )

    def p_charset( self, p ) :
        """charset      : CHARSET"""
        p[0] = Charset( p.parser, CHARSET(p.parser, p[1]) )

    def p_body( self, p ) :
        """body         : BODY"""
        p[0] = Body( p.parser, BODY(p.parser, p[1]) )

    def p_importas( self, p ) :
        """importas     : IMPORTAS"""
        p[0] = ImportAs( p.parser, IMPORTAS(p.parser, p[1]) )

    def p_implement( self, p ) :
        """implement    : IMPLEMENT"""
        p[0] = Implement( p.parser, IMPLEMENT(p.parser, p[1]) )

    def p_inherit( self, p ) :
        """inherit      : INHERIT"""
        p[0] = Inherit( p.parser, INHERIT(p.parser, p[1]) )

    def p_use( self, p ) :
        """use          : USE"""
        p[0] = Use( p.parser, USE(p.parser, p[1]) )

    #---- Filter block

    def p_filterblock( self, p ) :
        """filterblock      : FILTEROPEN FILTERTEXT FILTERCLOSE"""
        terms = [ (FILTEROPEN,1), (FILTERTEXT,2), (FILTERCLOSE,3) ]
        p[0] = FilterBlock( p.parser, *self._buildterms( p, terms ) )

    #---- Function block / Interface block

    def p_functionblock_1( self, p ) :
        """functionblock    : FUNCTION dirtyblocks INDENT siblings DEDENT
                            | FUNCTION INDENT siblings DEDENT"""
        terms = [ None, (FUNCTION,1), p[2], (INDENT,3), p[4], (DEDENT,5)
                ] if len(p) == 6 else [ 
                  None, (FUNCTION,1), None, (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = FunctionBlock( p.parser, *self._buildterms(p, terms) )

    def p_functionblock_2( self, p ) :
        """functionblock    : DECORATOR FUNCTION dirtyblocks INDENT siblings DEDENT
                            | DECORATOR FUNCTION INDENT siblings DEDENT"""
        terms = [ (DECORATOR,1), (FUNCTION,2), p[3], (INDENT,4), p[5], (DEDENT,6)
                ] if len(p) == 7 else [ 
                  (DECORATOR,1), (FUNCTION,2), None, (INDENT,3), p[4], (DEDENT,5) ]
        p[0] = FunctionBlock( p.parser, *self._buildterms(p, terms) )

    def p_interfaceblock( self, p ) :
        """interfaceblock   : INTERFACE dirtyblocks INDENT siblings DEDENT
                            | INTERFACE INDENT siblings DEDENT"""
        terms = [ (INTERFACE,1), p[2], (INDENT,3), p[4], (DEDENT,5)
                ] if len(p) == 6 else [ 
                  (INTERFACE,1), None, (INDENT,2), p[3], (DEDENT,4) ]
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
        """ifblock      : IF dirtyblocks INDENT siblings DEDENT
                        | IF INDENT siblings DEDENT"""
        terms = [ (IF,1), p[2], (INDENT,3), p[4], (DEDENT,5) 
                ] if len(p) == 6 else [
                  (IF,1), None, (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = IfBlock( p.parser, *self._buildterms(p, terms) )

    def p_elifblock( self, p ) :
        """elifblock    : ELIF dirtyblocks INDENT siblings DEDENT
                        | ELIF INDENT siblings DEDENT"""
        terms = [ (ELIF,1), p[2], (INDENT,3), p[4], (DEDENT,5) 
                ] if len(p) == 6 else [
                  (ELIF,1), None, (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = ElifBlock( p.parser, *self._buildterms(p, terms) )

    def p_elseblock( self, p ) :
        """elseblock    : ELSE dirtyblocks INDENT siblings DEDENT
                        | ELSE INDENT siblings DEDENT"""
        terms = [ (ELSE,1), p[2], (INDENT,3), p[4], (DEDENT,5) 
                ] if len(p) == 6 else [
                  (ELSE,1), None, (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = ElseBlock( p.parser, *self._buildterms(p, terms) )

    def p_forblock( self, p ) :
        """forblock     : FOR dirtyblocks INDENT siblings DEDENT
                        | FOR INDENT siblings DEDENT"""
        terms = [ (FOR,1), p[2], (INDENT,3), p[4], (DEDENT,5) 
                ] if len(p) == 6 else [
                  (FOR,1), None, (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = ForBlock( p.parser, *self._buildterms(p, terms) )

    def p_whileblock( self, p ) :
        """whileblock   : WHILE dirtyblocks INDENT siblings DEDENT
                        | WHILE INDENT siblings DEDENT"""
        terms = [ (WHILE,1), p[2], (INDENT,3), p[4], (DEDENT,5) 
                ] if len(p) == 6 else [
                  (WHILE,1), None, (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = WhileBlock( p.parser, *self._buildterms(p, terms) )

    #---- Template language

    def p_tagblock( self, p ) :
        """tagblock     : tagline INDENT siblings DEDENT"""
        terms = [ p[1], (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = TagBlock( p.parser, *self._buildterms( p, terms ) )

    def p_statement( self, p ) :
        """statement    : STATEMENT"""
        p[0] = Statement( p.parser, STATEMENT(p.parser, p[1]) )

    def p_pass( self, p ) :
        """pass         : PASS"""
        p[0] = Pass( p.parser, PASS(p.parser, p[1]) )

    def p_tagline_1( self, p ) :
        """tagline      : tag NEWLINES
                        | tag NEWLINES dirtyblocks"""
        terms = [ p[1], None, (NEWLINES,2), p[3] 
                ] if len(p) == 4 else [ p[1], None, (NEWLINES,2), None ]
        p[0] = TagLine( p.parser, *self._buildterms(p, terms) )

    def p_tagline_2( self, p ) :
        """tagline      : tag contents NEWLINES
                        | tag contents NEWLINES dirtyblocks"""
        terms = [ p[1], p[2], (NEWLINES,3), p[4]
                ] if len(p) == 5 else [ p[1], p[2], (NEWLINES,3), None ]
        p[0] = TagLine( p.parser, *self._buildterms(p, terms) )

    def p_textblock( self, p ) :
        """textblock    : textline INDENT siblings DEDENT"""
        terms = [ p[1], (INDENT,2), p[3], (DEDENT,4) ]
        p[0] = TextBlock( p.parser, *self._buildterms(p, terms) )

    def p_textline( self, p ) :
        """textline     : contents NEWLINES
                        | contents NEWLINES dirtyblocks"""
        terms = [ p[1], (NEWLINES,2), p[3] 
                ] if len(p) == 4 else [ p[1], (NEWLINES,2), None ]
        p[0] = TextLine( p.parser, *self._buildterms(p, terms) )

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
        """attributes   : attr"""
        args = [ None, None, p[1] ]
        p[0] = Attributes( p.parser, *args )

    def p_attributes_2( self, p ) :
        """attributes   : whitespace attr
                        | attributes whitespace attr"""
        args = [ p[1], p[2], p[3] ] if len(p) == 4 else [ None, p[1], p[2] ]
        p[0] = Attributes( p.parser, *args )

    def p_attr_1( self, p ) :
        """attr         : attrname ATOM"""
        p[0] = Attr( p.parser, p[1], ATOM(p.parser, p[2]), None )

    def p_attr_2( self, p ) :
        """attr         : attrname smartstring"""
        p[0] = Attr( p.parser, p[1], None, p[2] )

    def p_attrname_1( self, p ) :
        """attrname     : ATOM EQUAL"""
        terms = [ None, (ATOM,1), (EQUAL,2) ]
        p[0] = AttrName( p.parser, *self._buildterms(p, terms) )

    def p_attrname_2( self, p ) :
        """attrname     : exprs EQUAL"""
        terms = [ p[1], None, (EQUAL,2) ]
        p[0] = AttrName( p.parser, *self._buildterms(p, terms) )

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
        """content      : exprs"""
        p[0] = Content( p.parser, None, p[1] )

    def p_content_4( self, p ) :
        """content      : commentblocks"""
        p[0] = Content( p.parser, None, p[1] )

    #---- Specifier

    def p_specifiers_1( self, p ) :
        """specifiers   : specifier"""
        p[0] = Specifiers( p.parser, None, None, p[1] )

    def p_specifiers_2( self, p ) :
        """specifiers   : specifiers specifier"""
        p[0] = Specifiers( p.parser, p[1], None, p[2] )

    def p_specifiers_3( self, p ) :
        """specifiers   : specifiers whitespace specifier"""
        p[0] = Specifiers( p.parser, p[1], p[2], p[3] )

    def p_specifier_1( self, p ) :
        """specifier    : ATOM"""
        p[0] = Specifier( p.parser, ATOM(p.parser, p[1]), None )

    def p_specifier_2( self, p ) :
        """specifier    : TEXT"""
        p[0] = Specifier( p.parser, TEXT(p.parser, p[1]), None )

    def p_specifier_3( self, p ) :
        """specifier    : EQUAL"""
        p[0] = Specifier( p.parser, EQUAL(p.parser, p[1]), None )

    def p_specifier_4( self, p ) :
        """specifier    : SPECIALCHARS"""
        p[0] = Specifier( p.parser, SPECIALCHARS(p.parser, p[1]), None )

    def p_specifier_5( self, p ) :
        """specifier    : smartstring"""
        p[0] = Specifier( p.parser, None, p[1] )

    def p_specifier_6( self, p ) :
        """specifier    : exprs"""
        p[0] = Specifier( p.parser, None, p[1] )

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
        """strcontent   : EQUAL"""
        p[0] = StrContent( p.parser, EQUAL(p.parser, p[1]), None )

    def p_strcontent_5( self, p ) :
        """strcontent   : OPENBRACE"""
        p[0] = StrContent( p.parser, OPENBRACE(p.parser, p[1]), None )

    def p_strcontent_6( self, p ) :
        """strcontent   : whitespace"""
        p[0] = StrContent( p.parser, None, p[1] )

    def p_strcontent_7( self, p ) :
        """strcontent   : exprs"""
        p[0] = StrContent( p.parser, None, p[1] )

    #---- style

    def p_style( self, p ) :
        """style            : OPENBRACE stylecontents CLOSEBRACE
                            | OPENBRACE CLOSEBRACE"""
        terms = [ (OPENBRACE,1), p[2], (CLOSEBRACE,3)
               ] if len(p) == 4 else [ (OPENBRACE,1), None, (CLOSEBRACE,2) ]
        p[0] = Style( p.parser, *self._buildterms(p, terms) )

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
        """style_content    : TEXT"""
        terms = [ None, None, (TEXT,1), None ]
        p[0] = StyleContent( p.parser, *self._buildterms(p, terms) )
                        
    def p_style_content_3( self, p ) :
        """style_content    : SPECIALCHARS"""
        terms = [ None, None, (SPECIALCHARS,1), None ]
        p[0] = StyleContent( p.parser, *self._buildterms(p, terms) )
                        
    def p_style_content_4( self, p ) :
        """style_content    : exprs"""
        terms = [ None, None, None, p[1] ]
        p[0] = StyleContent( p.parser, *self._buildterms(p, terms) )

    #---- Exprs

    def p_exprs( self, p ) :
        """exprs            : OPENEXPRS exprs_contents CLOSEBRACE
                            | OPENEXPRS CLOSEBRACE"""
        terms = [ (OPENEXPRS,1), p[2], (CLOSEBRACE, 3) 
                ] if len(p) == 4 else [ (OPENEXPRS,1), None, (CLOSEBRACE,2) ]
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

    #def p_exprs_content_2( self, p ) :
    #    """exprs_content    : S"""
    #    terms = [ None, (S,1), None, None ]
    #    p[0] = ExprsContent( p.parser, *self._buildterms(p, terms) )

    def p_exprs_content_3( self, p ) :
        """exprs_content    : STRING"""
        terms = [ None, None, (STRING,1), None ]
        p[0] = ExprsContent( p.parser, *self._buildterms(p, terms) )

    def p_exprs_content_4( self, p ) :
        """exprs_content    : TEXT"""
        terms = [ None, None, None, (TEXT,1) ]
        p[0] = ExprsContent( p.parser, *self._buildterms(p, terms) )

    #def p_exprs_content_5( self, p ) :
    #    """exprs_content    : SPECIALCHARS"""
    #    terms = [ None, None, None, (SPECIALCHARS,1) ]
    #    p[0] = ExprsContent( p.parser, *self._buildterms(p, terms) )

    #----

    def p_dirtyblock_1( self, p ):
        """dirtyblocks  : commentblocks NEWLINES
                        | dirtyblocks commentblocks NEWLINES"""
        args = [ p[1], p[2], NEWLINES(p.parser, p[3])
               ] if len(p) == 4 else [ None, p[1], NEWLINES(p.parser, p[2]) ]
        p[0] = DirtyBlocks( p.parser, *args )

    def p_dirtyblock_2( self, p ):
        """dirtyblocks  : emptylines
                        | dirtyblocks emptylines"""
        args = [ p[1], p[2], None ] if len(p) == 3 else [ None, p[1], None ]
        p[0] = DirtyBlocks( p.parser, *args )

    def p_commentblocks( self, p ) :
        """commentblocks    : commentblock
                            | commentblocks commentblock"""
        args = [ p[1], p[2] ] if len(p) == 3 else [ None, p[1] ]
        p[0] = CommentBlocks( p.parser, *args )

    def p_commentblock( self, p ) :
        """commentblock     : COMMENTOPEN COMMENTTEXT COMMENTCLOSE
                            | COMMENTOPEN COMMENTCLOSE"""
        terms = [ (COMMENTOPEN,1), (COMMENTTEXT,2), (COMMENTCLOSE,3) 
                ] if len(p) == 4 else [(COMMENTOPEN,1), None, (COMMENTCLOSE,2)]
        p[0] = CommentBlock( p.parser, *self._buildterms( p, terms ))

    def p_emptylines( self, p ) :
        """emptylines   : EMPTYSPACE
                        | emptylines EMPTYSPACE"""
        terms = [ p[1], (EMPTYSPACE,2) 
                ] if len(p) == 3 else [ None, (EMPTYSPACE,1) ]
        p[0] = EmptyLines( p.parser, *self._buildterms( p, terms ))

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
            self._parse_error( 'At end of input', u'' )

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
    
    text   = codecs.open( sys.argv[1], encoding='utf-8' 
             ).read() if len(sys.argv) > 1 else "hello" 
    parser = TTLParser( yacc_debug=True )
    t1     = time.time()
    # set debuglevel to 2 for debugging
    t = parser.parse( text, 'x.c', debuglevel=2 )
    t.show( showcoord=True )
    print time.time() - t1
