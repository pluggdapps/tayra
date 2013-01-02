#! /usr/bin/env python

# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Lexing rules for Tayra Template Language"""

import re, sys, os
import ply.lex
from   ply.lex          import TOKEN, LexToken

class TTLLexer( object ) :
    """A lexer for the Tayra Template language
        build() To build   
        input() Set the input text
        token() To get new tokens.
    """
    def __init__( self, compiler ):
        """ Create a new Lexer"""
        self.compiler = compiler
        self.indent = ''
        self.indentstack = []
        self.ttltokens = []

    #---- API methods

    def build( self, **kwargs ) :
        """ Builds the lexer from the specification. Must be called after the
        lexer object is created. This method exists separately, because the
        PLY manual warns against calling lex.lex inside __init__
        """
        self.ttlfile = kwargs.pop( 'ttlfile', '<String>' )
        reflags = re.MULTILINE | re.UNICODE
        self.lexer = ply.lex.lex( module=self, reflags=reflags, **kwargs )

    def input( self, text ) :
        """`text` to tokenise. Preprocess the text before tokenising,
          * A line separator is automatically appended at the end of text.
        """
        self.lexer.input( self._preprocess( text ) + os.linesep ) #self.finish
    
    def token( self ) :
        """Get the next token"""
        tok = self.poptoken()
        tok = self.lexer.token() if tok == None else tok
        if tok == None and self.indentstack :
            self._unwind_indentstack()
            tok = self.poptoken()
        return tok 

    def reset_lineno( self ) :
        """ Resets the internal line number counter of the lexer."""
        self.lexer.lineno = 1

    def poptoken( self ) :
        tok = self.ttltokens.pop(0) if self.ttltokens else None
        return tok

    #---- States
    states = ( 
        ( 'comment', 'exclusive' ),
        ( 'filter', 'exclusive' ),
    )

    #---- Tokens
    tokens = (
        # Tokens
        'INDENT', 'DEDENT', 'NEWLINES', 'TEXT',

        # Single line
        'DOCTYPE', 'BODY', 'IMPORT', 'INHERIT', 'IMPLEMENT', 'USE',
        'COMMENTLINE', 'STATEMENT', 'TAGBEGIN',

        # Comment block
        'COMMENTOPEN', 'COMMENTTEXT', 'COMMENTCLOSE',

        # filter block
        'FILTEROPEN', 'FILTERTEXT', 'FILTERCLOSE',

        # Program blocks
        'INTERFACE', 'DECORATOR', 'FUNCTION', 'IF', 'ELIF', 'ELSE', 'FOR',
        'WHILE',
    )
    
    # Directive names
    directivenames = [
        'doctype', 'body', 'import', 'inherit', 'implement', 'use',
    ]
    
    # special lines, pattern [ \t]*[!<@:]....

    tab2space = 2
    nl        = r'(\n|\r\n|\r)[ \t\r\n]*'
    escseq    = r'(\\.)|(\\$)'
    symbol    = r'[a-zA-Z0-9_.]+'
    attrtoken = r'[a-zA-Z0-9\-_"\']+'
    attrname  = r'[a-zA-Z0-9\-_]+'
    attrvalue = \
        r'(?:"[^"\\]*(?:\\.[^"\\]*)*")'+r'|'+r"(?:'[^'\\]*(?:\\.[^'\\]*)*')"
    finish    = r'OVER!!!!@\#END-OF-TEXT\#@!!!!OVER'
    prgsuffx  = r'(?=:[ \t]*$):[ \t]*$'
    text      = r'[^\r\n\\]+'
    exprsubst = r'(?<!\\)\$\{[^}]*\}'

    # Single line statements
    statement   = r'@@[^\r\n]+$'

    # Single line comment pattern
    commentline = r'\#\#[^\r\n]*$'

    # Directive patterns
    doctype   = r'@doctype[^\r\n]*$'
    body      = r'@body[^\r\n]*$'
    importas  = r'(@import|@from)[^\r\n]*$'
    inherit   = r'@inherit[^\r\n]*$'
    implement = r'@implement[^\r\n]*$'
    use       = r'@use[^\r\n]*$'

    # Comment block patterns
    cmtopen   = r'<!--'
    cmttext   = r'(.|[\r\n])+?(?=-->)'                # Non greedy
    cmtclose  = r'-->[ \t]*$'

    # Macro blocks
    fbopen    = r':(%s):[^\r\n]*$' % attrname
    fbtext    = r'[^\r\n]+'
    fbclose   = r':(%s):[ \t]*$' % attrname

    # Program blocks
    dechar      = r'([^\(\\]|\r|\n|\r\n)'
    interface   = r'^@interface(.|\n|\r\n|\r)*?' + prgsuffx # Matches newlines
    decorator   = r'@dec[ \t]+%s\(%s*(?:\\.%s*)*\)[ \t]*'%(
                            symbol,dechar,dechar)
    function    = r'@def(.|\n|\r\n|\r)*?' + prgsuffx # Matches newlines
    if_         = r'@if.*?' + prgsuffx      # Matches newlines
    elif_       = r'@elif.*?' + prgsuffx    # Matches newlines
    else_       = r'@else.*?' + prgsuffx    # Matches newlines
    for_        = r'@for.*?' + prgsuffx     # Matches newlines
    while_      = r'@while.*?' + prgsuffx   # Matches newlines

    # Tag blocks
    tagmodifs   = r'!'
    tagchar     = r'([^>\\]|\r|\n|\r\n)'
    newtag      = r'<(%s)?%s*(?:\\.%s*)*>' % (tagmodifs, tagchar, tagchar)

    def replacetab( self, s ):
        return s.replace( '\t', ' '*self.tab2space )

    def indentby( self, here, to ):
        return ' ' * (len(here) - currlevel)

    #---- Generic tokens

    #@TOKEN( finish )
    #def t_FINISH_TEXT( self, t ) :
    #    return t

    @TOKEN( escseq )
    def t_ESCAPED( self, t ) :
        return self._onescaped( t )

    @TOKEN( nl )
    def t_NEWLINES( self, t ) :
        self._incrlineno(t)
        # Prune the single newline appended at the end.
        if t.lexer.lexpos == len(t.lexer.lexdata) :
            if t.value[-1] == '\n' :
                t.value = t.value[:-1]
            else :
                raise Exception("Expect text to end with newline ")
        # Parse indentation
        parts = t.value.splitlines()
        if parts :
            parts[-1] = self.replacetab( parts[-1] )
            self._addtokens( self._tokenize( 'NEWLINES', t.value ))
            if ( parts[-1] and parts[-1].strip() == '' and 
                 t.value[-1] not in ['\r', '\n'] ) :
                # There is some indent
                if parts[-1] > self.indent :
                    diff = len(parts[-1]) - len(self.indent)
                    self._addtokens( self._tokenize('INDENT', ' '*diff) )
                    self.indentstack.append( ('DEDENT', ' '*diff) )
                    self.indent = parts[-1]

                elif parts[-1] < self.indent :
                    while parts[-1] < self.indent :
                        if self.indentstack :
                            tokname, val = self.indentstack.pop(-1)
                            self._addtokens( self._tokenize(tokname, val) )
                            self.indent = self.indent[ :-len(val) ]
                        else :
                            self._error( 'Indentation error', t )
            else :
                # There is no indent
                self._unwind_indentstack()
        return self.poptoken()

    @TOKEN( statement )
    def t_STATEMENT( self, t ) :
        return t

    @TOKEN( commentline )                   # Single line comment
    def t_COMMENTLINE( self, t ) :
        return t

    @TOKEN( doctype )
    def t_DOCTYPE( self, t ):
        return t

    @TOKEN( body )
    def t_BODY( self, t ):
        return t

    @TOKEN( importas )
    def t_IMPORT( self, t ):
        return t

    @TOKEN( inherit )
    def t_INHERIT( self, t ):
        return t

    @TOKEN( implement )
    def t_IMPLEMENT( self, t ):
        return t

    @TOKEN( use )
    def t_USE( self, t ):
        return t

    @TOKEN( cmtopen )                   # Open a comment block
    def t_COMMENTOPEN( self, t ) :
        t.lexer.push_state( 'comment' )
        return t

    @TOKEN( fbopen )
    def t_FILTEROPEN( self, t ) :
        t.lexer.push_state( 'filter' )
        return t

    @TOKEN( interface )
    def t_INTERFACE( self, t ) :
        self._incrlineno(t)
        return t

    @TOKEN( decorator )
    def t_DECORATOR( self, t ) :
        self._incrlineno(t)
        return t

    @TOKEN( function )
    def t_FUNCTION( self, t ) :
        self._incrlineno(t)
        return t

    @TOKEN( if_ )
    def t_IF( self, t ) :
        return t

    @TOKEN( elif_ )
    def t_ELIF( self, t ) :
        return t

    @TOKEN( else_ )
    def t_ELSE( self, t ) :
        return t

    @TOKEN( for_ )
    def t_FOR( self, t ) :
        return t

    @TOKEN( while_ )
    def t_WHILE( self, t ) :
        return t

    @TOKEN( newtag )
    def t_TAGBEGIN( self, t ) :
        self._incrlineno(t)
        t.value = t.value.replace( r'\>', '>' )
        return t

    @TOKEN( text )
    def t_TEXT( self, t ) :
        return t

    #---- Comment block tokens

    @TOKEN( cmtclose )
    def t_comment_COMMENTCLOSE( self, t ):
        t.lexer.pop_state()
        return t

    @TOKEN( cmttext )
    def t_comment_COMMENTTEXT( self, t ):
        self._incrlineno(t)
        return t

    #---- Filter block tokens

    @TOKEN( fbclose )
    def t_filter_FILTERCLOSE( self, t ):
        self.lexer.pop_state()
        return t

    @TOKEN( nl )
    def t_filter_NEWLINES( self, t ):
        self._incrlineno(t)
        return t

    @TOKEN( fbtext )
    def t_filter_FILTERTEXT( self, t ):
        return t

    def t_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    def t_comment_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    def t_filter_error( self, t ):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    ## -------------- Internal auxiliary methods ---------------------

    def _error( self, msg, token ):
        loct = self._make_tok_location( token )
        self.lexer.skip( 1 )
        err = "%s in file %r : %s ..." % (self.ttlfile, msg, token)
        self.compiler.pa.logerror( err )
    
    def _find_tok_column( self, token ):
        l = len( self.lexer.lexdata[:token.lexpos].rsplit( os.linesep, 1 )[-1] )
        return l

    def _make_tok_location( self, token ):
        return ( token.lineno, self._find_tok_column(token) )

    def _incrlineno( self, token ) :
        newlines = len( token.value.split('\n') ) - 1
        if newlines > 0 :
            token.lexer.lineno += newlines
    
    def _tokenize( self, type_, value ) :
        tok = LexToken()
        tok.type = type_
        tok.value = value
        tok.lineno = self.lexer.lineno
        tok.lexpos = self.lexer.lexpos
        return tok

    def _preprocess( self, text ) :
        return text

    def _addtokens( self, tok ) :
        self.ttltokens.extend( tok if isinstance(tok, list) else [tok] )

    def _unwind_indentstack( self ) :
        while self.indent and self.indentstack :
            tokname, val = self.indentstack.pop(-1)
            self._addtokens( self._tokenize(tokname, val) )
            self.indent = self.indent[ :-len(val) ]

    def _onescaped( self, token ) :
        """If escaping the newline then increment the lexposition, but
        count the line-number.
        """
        if len(token.value) == 1 :
            self._incrlineno( token )
            token.lexer.lexpos += 1
            return None
        else :
            token = self._tokenize('TEXT', token.value[1])
            return token
    
