# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

from pygments.lexer        import RegexLexer, bygroups, using
from pygments.token        import *
from pygments.lexers.agile import PythonLexer
from pygments.lexers.web   import CssLexer, JavascriptLexer, HtmlLexer

from tayra.lexer    import TTLLexer

# TODO :
#   Detailed highlighting for directives.

class TemplateLexer( RegexLexer ):
    name = 'ttl'
    aliases = ['tayra-template', 'tayratemplate', 'ttl']
    filenames = ['*.ttl']

    pylex = using(PythonLexer)
    csslex = using(CssLexer)
    jslex = using(JavascriptLexer)

    #-- RegEx patterns
    text      = r'[^\s]+'
    ws        = r'\s+'
    exprsubst = r'(?<!\\)(\$\{)([^}\\]*(?:\\.[^}\\]*)*)(\})'

    # Directive patterns
    diropen  = r'(@)(doctype|body|import|from|inherit|implement)'

    # Single line statements
    statement = r'(@@)([^\r\n\\]*(?:\\\n[^\r\n\\]*)*)$'

    # Tag blocks
    tagmodifs = r'!'
    tagopen   = r'(<)(%s?)(\s*[\w:]+)' % tagmodifs

    # Program blocks
    prgsuffx  = r'(?=:[ \t]*$)(:[ \t]*)$'
    blocknms  = r'def|if|elif|else|for|while'
    interface = r'(^@)(interface)(.*?)' + prgsuffx
    pyblock   = r'(@)(%s)(.*?)%s' % (blocknms, prgsuffx)

    # Filter blocks
    fbsuffx   = r'(?=:py:\s*)(:)(py)(:)'
    openfbpy  = r'(:)(py)(:)'
    fbtext    = r'(.+?)' + fbsuffx

    tokens = {
        'root': [
        ],
        'root': [
            ( TTLLexer.commentline, Comment ),
            # Directives
            ( diropen, bygroups(Punctuation, Keyword.Reserved), 'directive' ),
            # Statements
            ( statement, bygroups(Punctuation, pylex) ),
            ( TTLLexer.cmtopen, Comment, 'comment' ),
            # Script
            # ( r'<\s*script\s*', Name.Tag, ('script-content', 'tag')),
            # ( r'<\s*style\s*', Name.Tag, ('style-content', 'tag')),
            # Blocks
            ( tagopen, bygroups(Name.Tag, Operator, Name.Tag), 'tag' ),
            ( interface, bygroups(Punctuation,Keyword.Reserved,pylex,Text) ),
            ( pyblock, bygroups(Punctuation, Keyword, pylex, Text) ),
            ( exprsubst, bygroups(Operator,  pylex, Operator) ),
            # filter-blocks
            ( openfbpy, bygroups(Keyword, Name.Attribute, Keyword), 'fbpy' ),
            # Normal text
            ( r'&\S*?;', Name.Entity),
            ( text, Text ),
            ( ws, Whitespace ),
        ],
        'comment': [
            ( TTLLexer.cmtclose, Comment, '#pop' ),
            ( TTLLexer.cmttext, Comment ),
        ],
        'tag': [
            ( r'\s+', Text ),
            ( r'#[\w-]+', Keyword.Declaration ),    # id
            ( r'\.[\w:\.-]+', Keyword.Class ),      # class
            ( r'(\{)([^\}]*)(\})', bygroups(Operator, String, Operator) ),
            ( r'[\w:-]+\s*=', Name.Attribute, 'attr' ),
            ( r'[^\s>]+', Name.Attribute ), # Attribute-token
            ( exprsubst, bygroups(Operator,  pylex, Operator) ),
            ( r'/?\s*>', Name.Tag, '#pop' ),
        ],
        'directive' : [
            ( r'[ \t]+', Text ),
            ( r'([^\s]+\s*=)(,?)', Name.Attribute, 'attr' ),
            # Attribute-token
            ( r'([^\s]+)(,?)', bygroups(Name.Attribute, Punctuation) ),
            ( r'[\r\n]', Text, '#pop'),
         ],
        'fbpy': [
            (fbtext, bygroups(pylex,Keyword,Name.Attribute,Keyword), '#pop'),
        ],
        'attr': [
            ( '".*?"', String, '#pop' ),
            ( "'.*?'", String, '#pop' ),
            ( r'[^\s>]+', String, '#pop' ),
        ],
        'script-content': [
            ( r'[^\r\n]+', jslex,  ),
            ( r'[\r\n]+', Name.Tag ),
            ( r'^$', Name.Tag, '#pop' ),
        ],
        'style-content': [
            ( r'[^\r\n]+', csslex ),
            ( r'[\r\n]+', Name.Tag ),
            ( r'^$', Name.Tag, '#pop' ),
        ],
    }

    # def get_tokens( self, text ):
    #     for x in super().get_tokens( text ) :
    #         print( x )
