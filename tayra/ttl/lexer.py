#! /usr/bin/env python

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2010 SKR Farms (P) LTD.

"""Lexing rules for Tayra Template Language"""

# -*- coding: utf-8 -*-

# Gotcha :
# Notes  :
# Todo   :


import re, sys, logging

import ply.lex
from   ply.lex          import TOKEN, LexToken

from   tayra.ttl.ast    import *

log = logging.getLogger( __name__ )
INDENTSPACE = 2

class LexError( Exception ) :
    pass

class TTLLexer( object ) :
    """A lexer for the Tayra Template language
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
    
    def _lextoken( self, type_, value ) :
        tok = LexToken()
        tok.type = type_
        tok.value = value
        tok.lineno = self.lexer.lineno
        tok.lexpos = self.lexer.lexpos
        return tok

    def _preprocess( self, text ) :
        # Replace `\ ESCAPEd new lines'.
        text = text.replace( '\\\n', '' )
        text = text.replace( '\\\r\n', '' )
        return text

    def _addtokens( self, tok ) :
        tok = tok if isinstance(tok, list) else [ tok ]
        self.ttltokens.extend( tok )

    def _unwind_indentstack( self ) :
        while self.indentstack :
            x = self.indentstack.pop(-1)
            self._addtokens( self._lextoken(x[0], x[1]) )
        self.currindent = ''

    def _onemptyindent( self, token ) :
        if len(token.lexer.lexdata) == token.lexer.lexpos :
            return
        elif token.lexer.lexdata[token.lexer.lexpos] != ' ':
            self._unwind_indentstack()
    
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
        self.currindent = ''
        self.indentstack = []
        self.ttltokens = []

    def build( self, **kwargs ) :
        """ Builds the lexer from the specification. Must be called after the
        lexer object is created. 
            
        This method exists separately, because the PLY manual warns against
        calling lex.lex inside __init__"""
        self.lexer = ply.lex.lex(
                        module=self,
                        reflags=re.MULTILINE | re.UNICODE | re.IGNORECASE,
                        **kwargs
                     )

    def reset_lineno( self ) :
        """ Resets the internal line number counter of the lexer."""
        self.lexer.lineno = 1

    def input( self, text ) :
        """`text` to tokenise"""
        text = self._preprocess( text )
        self.lexer.input( text )
    
    def token( self ) :
        """Get the next token"""
        tok = self.poptoken()
        tok = self.lexer.token() if tok == None else tok
        if tok == None and self.indentstack :
            self._unwind_indentstack()
            tok = self.poptoken()
        return tok 

    def poptoken( self ) :
        tok = self.ttltokens.pop(0) if self.ttltokens else None
        return tok

    # States
    states = ( 
        ( 'tag', 'exclusive' ),
        ( 'style', 'exclusive' ),
        ( 'exprs', 'exclusive' ),
        ( 'comment', 'exclusive' ),
    )

    ## Tokens recognized by the TTLLexer
    tokens = (
        'STATEMENT', 'PASS', 'EMPTYSPACE', 'INDENT', 'DEDENT',

        # `exprs` state
        'OPENEXPRS', 'STRING',
        
        # `tag` state
        'TAGOPEN', 'TAGEND', 'TAGCLOSE', 'EQUAL', 

        # `style` state
        'OPENBRACE',

        # `comment` state
        'COMMENTOPEN', 'COMMENTTEXT', 'COMMENTCLOSE',

        # directives
        'DOCTYPE', 'CHARSET', 'BODY', 'IMPORTAS', 'IMPLEMENT', 'INHERIT',
        'USE',
        'FUNCTION', 'INTERFACE', 'FILTER', 
        'IF', 'ELIF', 'ELSE', 'FOR', 'WHILE',

        #
        'SQUOTE', 'DQUOTE', 'NEWLINES', 'S', 'ATOM', 'TEXT',
        'CLOSEBRACE', 'SPECIALCHARS',
    )
    
    # special lines, pattern [ \t]*[!<@:]....

    # Special chars
    spchars      = r'[${]'
    tags_spchars = r'[/$]'
    styl_spchars = r'[${]'

    # Suffix definition for lookahead match for text
    style_text_s= r'(?!\}|\$\{)'                # till style_close, exprs_open
    tabspace    = r' \t'

    commentopen = r'[%s]*<!--' % tabspace
    commentclose= r'-->[%s]*(\n|\r\n)*' % tabspace
    commenttext = r'(.|[\r\n])+?(?=-->)'        # Non greedy
    commentline = r'[%s]*\#\#[^\r\n]*(\n|\r\n)*' % tabspace
    statement   = r'@@[^\r\n]*(\n|\r\n)+'
    pass_       = r'@@pass(\n|\r\n)+'
    emptyspace  = r'^[%s]+(\n|\r\n)+' % tabspace
    indent      = r'^[ ]+'
    nl          = r'[\r\n]+'
    spac        = r'[%s]*' % tabspace
    space       = r'[%s]+' % tabspace
    whitespac   = r'[\r\n%s]*' % tabspace
    whitespace  = r'[\r\n%s]+' % tabspace
    atom        = r'[a-zA-Z0-9\._\#-]+'
    tagname     = r'[a-zA-Z0-9]+'
    text        = r'[^\r\n<${]+'
    tag_text    = r'[^%s\r\n/>${"\'=]+' % tabspace
    style_text  = r'[^\r\n${}]+'
    exprs_text  = r'[^\r\n}"\']+'
    string      = r'"(.|[\r\n])*?"|\'(.|[\r\n])*?\''    # Non greedy

    # Suffix definition for lookahead match for prolog / statement tails.
    suffix1     = r'(?=;[%s]*(\n|\r\n)+);[%s]*(\n|\r\n)+' % (tabspace, tabspace)
    suffix2     = r'(?=:[%s]*(\n|\r\n)+):[%s]*(\n|\r\n)+' % (tabspace, tabspace)

    doctype     = r'^!!!.*?' + suffix1
    charset     = r'^@charset.*?' + suffix1
    body        = r'^@body.*?' + suffix1
    importas    = r'^@import.*?' + suffix1
    implement   = r'^@implement.*?' + suffix1
    inherit     = r'^@inherit.*?' + suffix1
    use         = r'^@use.*?' + suffix1

    interface   = r'^@interface.*?' + suffix2

    function    = r'@function.*?' + suffix2
    if_         = r'@if.*?' + suffix2
    elif_       = r'@elif.*?' + suffix2
    else_       = r'@else.*?' + suffix2
    for_        = r'@for.*?' + suffix2
    while_      = r'@while.*?' + suffix2
    filter_     = r':fb-'+atom

    prunews     = '!'
    pruneindent = '%'
    openexprs   = r'\$\{'
    gtend       = r'/>'
    lt          = r'<[%s]?' % prunews
    gt          = r'[%s%s]?>' % (prunews, pruneindent)
    equal       = r'='
    squote      = r"'"
    dquote      = r'"'
    semicolon   = r';'
    openbrace   = r'\{'
    closebrace  = r'\}'

    tagopen     = lt+tagname+whitespac
    wssemicolonws = whitespac+semicolon+whitespac
    tagend      = whitespac+gtend+spac
    tagclose    = whitespac+gt+spac

    # TTL Tokens

    @TOKEN( commentline )
    def t_COMMENTLINE( self, t ) :
        self._onemptyindent(t)
        return None

    @TOKEN( commentopen )
    def t_COMMENTOPEN( self, t ) :
        t.lexer.push_state( 'comment' )
        return t

    @TOKEN( statement )
    def t_STATEMENT( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( pass_ )
    def t_PASS( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( doctype )
    def t_DOCTYPE( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( charset )
    def t_CHARSET( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( body )
    def t_BODY( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( importas )
    def t_IMPORTAS( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( implement )
    def t_IMPLEMENT( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( inherit )
    def t_INHERIT( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( use )
    def t_USE( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( interface )
    def t_INTERFACE( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( emptyspace )
    def t_EMPTYSPACE( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( indent )
    def t_INDENT( self, t ) :
        value = t.value
        currlevel = len(self.currindent)
        if (len(value) > currlevel) and ( (len(value) % INDENTSPACE) == 0 ) :
            # Open Indentation
            openingby = ' ' * (len(value) - currlevel)
            self._addtokens([ self._lextoken('INDENT', openingby) ])
            self.indentstack.append( ('DEDENT', openingby ) )
            self.currindent = t.value
        elif (len(value) < currlevel) and ( (len(value) % INDENTSPACE) == 0 ) :
            # Close Indentation
            closingby = ' ' * (currlevel - len(value))
            while closingby and self.indentstack :
                x = self.indentstack.pop(-1)
                if len(closingby) >= len(x) :
                    self._addtokens( self._lextoken(x[0], x[1]) )
                    closingby = closingby[: -len(x[1]) ]
                elif len(closingby) < len(x) :
                    raise Exception( 'Indentation is more than expected' )
            if closingby :
                raise Exception( 'Unexpected indentation' )
            self.currindent = t.value
        elif len(value) != currlevel :
            raise LexError( 'Indentation should be %s spaces' % INDENTSPACE )
        return self.poptoken()

    @TOKEN( function )
    def t_FUNCTION( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( filter_ )
    def t_FILTER( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( if_ )
    def t_IF( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( elif_ )
    def t_ELIF( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( else_ )
    def t_ELSE( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( for_ )
    def t_FOR( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( while_ )
    def t_WHILE( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    @TOKEN( tagopen )
    def t_TAGOPEN( self, t ) :
        t.lexer.push_state( 'tag' )
        self._incrlineno(t)
        return t

    @TOKEN( openexprs )
    def t_OPENEXPRS( self, t ) :
        t.lexer.push_state( 'exprs' )
        return t

    @TOKEN( nl )
    def t_NEWLINES( self, t ) :
        self._incrlineno(t)
        self._onemptyindent(t)
        return t

    #@TOKEN( space )
    #def t_S( self, t ) :
    #    return t

    @TOKEN( spchars )
    def t_SPECIALCHARS( self, t ) :
        return t

    @TOKEN( text )
    def t_TEXT( self, t ) :
        return t

    @TOKEN( openexprs )
    def t_exprs_OPENEXPRS( self, t ) :               # <---- `exprs` state
        return t

    @TOKEN( closebrace )
    def t_exprs_CLOSEBRACE( self, t ) :
        t.lexer.pop_state()
        return t

    @TOKEN( nl )
    def t_exprs_NEWLINES( self, t ) :
        self._incrlineno(t)
        return t

    #@TOKEN( space )
    #def t_exprs_S( self, t ) :
    #    return t

    @TOKEN( string )
    def t_exprs_STRING( self, t ) :
        self._incrlineno(t)
        return t

    @TOKEN( exprs_text )
    def t_exprs_TEXT( self, t ) :
        return t

    @TOKEN( tagopen )
    def t_tag_TAGOPEN( self, t ) :                   # <---- `tag` state
        self._incrlineno(t)
        return t

    @TOKEN( tagend )
    def t_tag_TAGEND( self, t ) :
        t.lexer.pop_state()
        self._incrlineno(t)
        return t

    @TOKEN( tagclose )
    def t_tag_TAGCLOSE( self, t ) :
        t.lexer.pop_state()
        self._incrlineno(t)
        return t

    @TOKEN( openexprs )
    def t_tag_OPENEXPRS( self, t ) :
        t.lexer.push_state( 'exprs' )
        return t

    @TOKEN( squote )
    def t_tag_SQUOTE( self, t ) :
        return t

    @TOKEN( dquote )
    def t_tag_DQUOTE( self, t ) :
        return t

    @TOKEN( equal )
    def t_tag_EQUAL( self, t ) :
        return t

    @TOKEN( whitespac+openbrace )
    def t_tag_OPENBRACE( self, t ) :
        self._incrlineno(t)
        t.lexer.push_state( 'style' )
        return t

    @TOKEN( nl )
    def t_tag_NEWLINES( self, t ) :
        self._incrlineno(t)
        return t

    @TOKEN( space )
    def t_tag_S( self, t ) :
        return t

    @TOKEN( atom )
    def t_tag_ATOM( self, t ) :
        return t

    @TOKEN( tag_text )
    def t_tag_TEXT( self, t ) :
        return t

    @TOKEN( tags_spchars )
    def t_tag_SPECIALCHARS( self, t ) :
        return t

    @TOKEN( whitespac+openbrace )
    def t_style_OPENBRACE( self, t ) :              # <---- `style` state
        return t

    @TOKEN( closebrace+whitespac )
    def t_style_CLOSEBRACE( self, t ) :
        t.lexer.pop_state()
        return t

    @TOKEN( openexprs )
    def t_style_OPENEXPRS( self, t ) :
        t.lexer.push_state( 'exprs' )
        return t

    @TOKEN( nl )
    def t_style_NEWLINES( self, t ) :
        self._incrlineno(t)
        return t

    #@TOKEN( space )
    #def t_style_S( self, t ) :
    #    return t

    @TOKEN( style_text )
    def t_style_TEXT( self, t ) :
        return t

    @TOKEN( styl_spchars )
    def t_style_SPECIALCHARS( self, t ) :
        return t

    @TOKEN( commentopen )
    def t_comment_COMMENTOPEN( self, t ):           # <---- `comment` state
        return t

    @TOKEN( commentclose )
    def t_comment_COMMENTCLOSE( self, t ):
        self._incrlineno(t)
        t.lexer.pop_state()
        self._onemptyindent(t)
        return t

    @TOKEN( commenttext )
    def t_comment_COMMENTTEXT( self, t ):
        self._incrlineno(t)
        return t

    def t_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    def t_tag_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    def t_exprs_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    def t_style_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    def t_comment_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

def _fetchtoken( ttllex, stats ) :
    tok = ttllex.token()
    if tok :
        val = tok.value[1] if isinstance(tok.value, tuple) else tok.value
        print "- %20r " % val,
        print tok.type, tok.lineno, tok.lexpos
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
            ttllex = TTLLexer( errfoo, filename=f )
            ttllex.build()
            ttllex.input( open(f).read() )
            tok = _fetchtoken( ttllex, stats )
            while tok :
                tok = _fetchtoken( ttllex, stats )
