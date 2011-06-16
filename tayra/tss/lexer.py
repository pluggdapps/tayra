#! /usr/bin/env python

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

"""Lexing rules for Tayra Style Sheets"""

# -*- coding: utf-8 -*-

# Gotcha :
#   1. Enabling optimize screws up the order of regex match (while lexing)
#      Bug in PLY ???
#   2. `nmchar` and `nmstart` supports Case-insensitive identifiers (seems to
#   be not in sync with CSS spec. ??
# Notes  :
#   1. The first grammar was defined using CSS's forward compatible grammar
#   rules. But the parse tree did not have much information ready-made. So
#   switched to CSS3 grammar rules
# Todo   :


import re, sys, logging

import ply.lex
from   ply.lex          import TOKEN

from   tayra.tss.ast    import *

log = logging.getLogger( __name__ )

class TSSLexer( object ) :
    """A lexer for the Tayra Style Sheets.
        build() To build   
        input() Set the input text
        token() To get new tokens.
    The public attribute filename can be set to an initial filaneme, but the
    lexer will update it upon #line directives."""

    ## -------------- Internal auxiliary methods ---------------------

    def _error( self, msg, token ):
        print "Error in file %r ..." % self.filename
        loct = self._make_tok_location( token )
        self.error_func and self.error_func( self, msg, loct[0], loct[1] )
        self.lexer.skip( 1 )
        log.error( "%s %s" % (msg, token) )
    
    def _find_tok_column( self, token ):
        i = token.lexpos
        while i > 0:
            if self.lexer.lexdata[i] == '\n': break
            i -= 1
        return (token.lexpos - i) + 1
    
    def _make_tok_location( self, token ):
        return ( token.lineno, self._find_tok_column(token) )

    def _incrlineno( self, token ) :
        newlines = len( token.value.split('\n') ) - 1
        if newlines > 0 : token.lexer.lineno += newlines
    
    ## --------------- Interface methods ------------------------------

    def __init__( self, error_func=None, conf={}, filename='', ):
        """ Create a new Lexer.
        error_func :
            An error function. Will be called with an error message, line
            and column as arguments, in case of an error during lexing.
        """
        self.error_func = error_func
        self.filename = filename
        self.conf = conf

    def build( self, **kwargs ) :
        """ Builds the lexer from the specification. Must be called after the
        lexer object is created. 
            
        This method exists separately, because the PLY manual warns against
        calling lex.lex inside __init__"""
        self.lexer = ply.lex.lex(
                        module=self,
                        reflags=re.UNICODE | re.IGNORECASE,
                        **kwargs
                     )

    def reset_lineno( self ) :
        """ Resets the internal line number counter of the lexer."""
        self.lexer.lineno = 1

    def input( self, text ) :
        """`text` to tokenise"""
        self.lexer.input( text )
    
    def token( self ) :
        """Get the next token"""
        tok = self.lexer.token()
        return tok 

    # States
    states = ()

    ## Tokens recognized by the TSSLexer
    tokens = (
        'S', 'COMMENT', 'IMPORT_SYM', 'PAGE_SYM', 'MEDIA_SYM',
        'FONT_FACE_SYM', 'CHARSET_SYM', 'NAMESPACE_SYM', 'IMPORTANT_SYM',
        'ATKEYWORD',
        'URI', 'CDO', 'CDC', 'INCLUDES', 'DASHMATCH',
        'HASH',
        'PERCENTAGE', 'NUMBER', 'EMS', 'EXS',
        'LENGTH', 'ANGLE', 'TIME', 'FREQ',
        #'DIMEN',
        'STRING', 'FUNCTION', 'IDENT',
        'UNICODERANGE',
        'DLIMIT',

        # Single character token 
        'PLUS', 'GT', 'LT', 'TILDA', 'COMMA', 'COLON', 'MINUS', 'EQUAL', 'DOT',
        'STAR', 'SEMICOLON', 'FWDSLASH',
        'OPENBRACE', 'CLOSEBRACE', 'OPENSQR', 'CLOSESQR',
        'OPENPARAN', 'CLOSEPARAN',
    )
    
    # CSS3 tokens

    h           = r'[0-9a-f]'
    w		    = r'[ \t\r\n\f]*'
    nl          = r'\n|\r\n|\r|\f'
    num		    = r'([0-9]+|[0-9]*\.[0-9]+)'
    nonascii    = r'[\200-\377]'
    unicode_    = r'(\\[0-9a-f]{1,6}[ \t\r\n\f]?)'
    escape		= unicode_ + r'|' r'(\\[ -~\200-\377])'
    nmstart		= r'[a-z_]'     r'|' + nonascii + r'|' + escape
    nmchar		= r'[a-z0-9_-]' r'|' + nonascii + r'|' + escape
    string1		= r'("([\t !\#$%&(-~]|\\' + nl+ r"|'|" + nonascii + r'|' + escape + r')*")'
    string2		= r"('([\t !\#$%&(-~]|\\" + nl+ r'|"|' + nonascii + r"|" + escape + r")*')"
    string		= r'(' + string1 + r'|' + string2 + r')'
    ident		= r'[-]?(' + nmstart + r')(' + nmchar + r')*'
    name		= r'(' + nmchar + r')+'
    url		    = r'([!\#$%&*-~]|' + nonascii + r'|' + escape +r')*'
    range_      = r'\?{1,6}|[0-9a-f](\?{0,5}|[0-9a-f](\?{0,4}|' + \
                  r'[0-9a-f](\?{0,3}|[0-9a-f](\?{0,2}|[0-9a-f](\??|[0-9a-f])))))'

    def t_S( self, t ) :
        r'[ \t\r\n\f]+'
        self._incrlineno( t )
        return t

    def t_COMMENT( self, t ) :
        r'\/\*[^*]*\*+([^/][^*]*\*+)*\/'
        return t

    def t_IMPORT_SYM( self, t ) :
        r'@import'
        return t

    def t_PAGE_SYM( self, t ) :
        r'@page'
        return t

    def t_MEDIA_SYM( self, t ) :
        r'@media'
        return t

    def t_FONT_FACE_SYM( self, t ) :
        r'@font-face'
        return t

    def t_CHARSET_SYM( self, t ) :
        r'@charset'
        return t

    def t_NAMESPACE_SYM( self, t ) :
        r'@namespace'
        return t

    @TOKEN( r'!' + w + 'important' )
    def t_IMPORTANT_SYM( self, t ) :
        self._incrlineno( t )
        return t

    # Gotcha : Browser specific @-rules
    @TOKEN( r'@' + ident )
    def t_ATKEYWORD( self, t ) :
        return t

    # Gotcha : Confirmance issue : urls are not comfirming to string format
    #@TOKEN( r'url\(' + w + string + w + r'\)' )
    @TOKEN( r'url\([^)]*\)' )
    def t_URI( self, t ) :
        self._incrlineno( t )
        return t

    def t_CDO( self, t ) :
        r'<!--'
        return t

    def t_CDC( self, t ) :
        r'-->'
        return t

    def t_INCLUDES( self, t ) :
        r'~='
        return t

    def t_DASHMATCH( self, t ) :
        r'\|='
        return t

    @TOKEN( r'\#' + name )
    def t_HASH( self, t ) :
        return t

    @TOKEN( num + r'em' )
    def t_EMS( self, t ) :
        return t

    @TOKEN( num + r'ex' )
    def t_EXS( self, t ) :
        return t

    @TOKEN( num + r'px' )
    def t_LENGTH_PX( self, t ) :
        t.type = 'LENGTH'
        t.value = (LENGTH_PX, t.value)
        return t

    @TOKEN( num + r'cm' )
    def t_LENGTH_CM( self, t ) :
        t.type = 'LENGTH'
        t.value = (LENGTH_CM, t.value)
        return t

    @TOKEN( num + r'mm' )
    def t_LENGTH_MM( self, t ) :
        t.type = 'LENGTH'
        t.value = (LENGTH_MM, t.value)
        return t

    @TOKEN( num + r'in' )
    def t_LENGTH_IN( self, t ) :
        t.type = 'LENGTH'
        t.value = (LENGTH_IN, t.value)
        return t

    @TOKEN( num + r'pt' )
    def t_LENGTH_PT( self, t ) :
        t.type = 'LENGTH'
        t.value = (LENGTH_PT, t.value)
        return t

    @TOKEN( num + r'pc' )
    def t_LENGTH_PC( self, t ) :
        t.type = 'LENGTH'
        t.value = (LENGTH_PC, t.value)
        return t

    @TOKEN( num + r'deg' )
    def t_ANGLE_DEG( self, t ) :
        t.type = 'ANGLE'
        t.value = (ANGLE_DEG, t.value)
        return t

    @TOKEN( num + r'rad' )
    def t_ANGLE_RAD( self, t ) :
        t.type = 'ANGLE'
        t.value = (ANGLE_RAD, t.value)
        return t

    @TOKEN( num + r'grad' )
    def t_ANGLE_GRAD( self, t ) :
        t.type = 'ANGLE'
        t.value = (ANGLE_GRAD, t.value)
        return t

    @TOKEN( num + r'ms' )
    def t_TIME_MS( self, t ) :
        t.type = 'TIME'
        t.value = (TIME_MS, t.value)
        return t

    @TOKEN( num + r's' )
    def t_TIME_S( self, t ) :
        t.type = 'TIME'
        t.value = (TIME_S, t.value)
        return t

    @TOKEN( num + r'Hz' )
    def t_FREQ_HZ( self, t ) :
        t.type = 'FREQ'
        t.value = (FREQ_HZ, t.value)
        return t

    @TOKEN( num + r'kHz' )
    def t_FREQ_KHZ( self, t ) :
        t.type = 'FREQ'
        t.value = (FREQ_KHZ, t.value)
        return t

    #@TOKEN( num + ident )
    #def t_DIMEN( self, t ) :
    #    return t

    @TOKEN( num + r'%' )
    def t_PERCENTAGE( self, t ) :
        return t

    @TOKEN( num )
    def t_NUMBER( self, t ) :
        return t

    @TOKEN( string )
    def t_STRING( self, t ) :
        self._incrlineno( t )
        return t

    @TOKEN( ident + r'\(' )
    def t_FUNCTION( self, t ) : 
        return t

    @TOKEN( ident )
    def t_IDENT( self, t ) :
        return t

    @TOKEN( r'U\+' + h + r'{1,6}-' + h + r'{1,6}' )
    def t_UNICODERANGE_S( self, t ) : 
        t.type = 'UNICODERANGE'
        t.value = t.value
        return t

    @TOKEN( r'U\+' + range_ )
    def t_UNICODERANGE_C( self, t ) : 
        t.type = 'UNICODERANGE'
        t.value = t.value
        return t

    t_PLUS          = r'\+'
    t_GT            = r'>'
    t_LT            = r'<'
    t_TILDA         = r'~'
    t_COMMA         = r','
    t_COLON         = r':'
    t_MINUS         = r'-'
    t_EQUAL         = r'='
    t_DOT           = r'\.'
    t_STAR          = r'\*'
    t_SEMICOLON     = r';'
    t_FWDSLASH      = r'\/'
    t_OPENBRACE     = r'\{'
    t_CLOSEBRACE    = r'\}'
    t_OPENSQR       = r'\['
    t_CLOSESQR      = r'\]'
    t_OPENPARAN     = r'\('
    t_CLOSEPARAN    = r'\)'
    t_DLIMIT        = r'[&\?\|!]'

    def t_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)


def _fetchtoken( tsslex, stats ) :
    tok = tsslex.token()
    if tok :
        val = tok.value[1] if isinstance(tok.value, tuple) else tok.value
        #print "- %20r " % val,
        #print tok.type, tok.lineno, tok.lexpos
        stats.setdefault( tok.type, [] ).append( tok.value )
    return tok

if __name__ == "__main__":
    def errfoo( lex, msg, a, b ) :
        print msg, a, b
        sys.exit()
    
    if len(sys.argv) > 1 :
        stats = {}
        for f in sys.argv[1:] :
            print "Lexing file %r ..." % f
            tsslex = TSSLexer( errfoo, filename=f )
            tsslex.build()
            tsslex.input( open(f).read() )
            tok = _fetchtoken( tsslex, stats )
            while tok :
                tok = _fetchtoken( tsslex, stats )

        #for k, v in stats.items() :
        #    print k
        #    print v
