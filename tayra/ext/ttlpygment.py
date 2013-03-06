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
    exprsubst = r'(?<!\\)(\$\{)(-\S*)?([^}\\]*(?:\\.[^}\\]*)*)(\})'

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

    Red = Generic.Deleted
    Str = String.Other

    tokens = {
        'root': [
            ( TTLLexer.commentline, Comment ),
            # Directives
            ( diropen, bygroups(Red, Keyword.Reserved), 'directive' ),
            # Statements
            ( statement, bygroups(Red, pylex) ),
            ( TTLLexer.cmtopen, Comment, 'comment' ),
            # Script
            # ( r'<\s*script\s*', Name.Tag, ('script-content', 'tag')),
            # ( r'<\s*style\s*', Name.Tag, ('style-content', 'tag')),
            # Blocks
            ( tagopen,
                bygroups(Operator, Operator, Name.Decorator), 'tag' ),
            ( interface, bygroups(Red, Keyword.Reserved, pylex, Text) ),
            ( pyblock, bygroups(Red, Keyword.Reserved, pylex, Text) ),
            ( exprsubst, bygroups(Red, Red, pylex, Red) ),
            # filter-blocks
            ( openfbpy, bygroups(Operator, Red, Operator), 'fbpy' ),
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
            ( r'#[\w-]+', Keyword.Type ),        # id
            ( r'\.[\w:\.-]+', Keyword.Type ),    # class
            ( r':[\w:\.-]+', Keyword.Type ),     # name
            ( r'(?<!\$)(\{)([^\}]*)(\})', bygroups(Operator, Str, Operator) ),
            ( r'[\w:-]+\s*=', Name.Attribute, 'attr' ),
            ( r'[^\s>]+', Name.Attribute ), # Attribute-token
            ( exprsubst, bygroups(Keyword, Keyword.Type, pylex, Keyword) ),
            ( r'/?\s*>', Operator, '#pop' ),
        ],
        'directive' : [
            ( r'[ \t]+', Text ),
            ( r'([^\s]+\s*=)(,?)', Name.Attribute, 'attr' ),
            # Attribute-token
            ( r'([^\s]+)(,?)', bygroups(Name.Attribute, Punctuation) ),
            ( r'[\r\n]', Text, '#pop'),
         ],
        'fbpy': [
            (fbtext, bygroups(pylex, Operator, Red, Operator), '#pop'),
        ],
        'attr': [
            ( '".*?"', Str, '#pop' ),
            ( "'.*?'", Str, '#pop' ),
            ( r'[^\s>]+', Str, '#pop' ),
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
