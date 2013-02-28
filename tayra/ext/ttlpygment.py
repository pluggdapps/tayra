# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

from pygments.lexer        import RegexLexer, bygroups, using
from pygments.token        import *
from pygments.lexers.agile import PythonLexer
from pygments.lexers.web   import CssLexer, JavascriptLexer, HtmlLexer

from tayra.lexer    import TTLLexer

class TemplateLexer( RegexLexer ):
    name = 'ttl'
    aliases = ['tayra-template', 'tayratemplate', 'ttl']
    filenames = ['*.ttl']

    stmttokens = bygroups( Name.Tag, using(PythonLexer) )
    pytokens = bygroups( using(PythonLexer) )
    directivetokens = bygroups( Keyword, Name.Attribute )
    fntokens = bygroups( Keyword, using(PythonLexer), Operator )
    styletokens = bygroups( Operator, using(CssLexer), Operator )
    exprtokens = bygroups( Operator, using( pytokens ), Operator )

    symbol    = r'([a-zA-Z0-9_\-\.]+)'
    attrtoken = r'[a-zA-Z0-9\-_"\']+'
    attrname  = r'[a-zA-Z0-9\-_]+'
    attrvalue = \
        r'(?:"[^"\\]*(?:\\.[^"\\]*)*")'+r'|'+r"(?:'[^'\\]*(?:\\.[^'\\]*)*')"
    prgsuffx  = r'(?=:[ \t]*$)(:[ \t]*)$'
    text      = r'[^\<\r\n\\]+'
    exprsubst = r'(?<!\\)(\$\{)([^}]*)(\})'

    # Single line statements
    statement   = r'(@@)([^\r\n]+$)'

    # Directive patterns
    doctype   = r'(@doctype)([^\r\n]*)$'
    body      = r'(@body)([^\r\n]*)$'
    importas  = r'(@import|@from)([^\r\n]*)$'
    inherit   = r'(@inherit)([^\r\n]*)$'
    implement = r'(@implement)([^\r\n]*)$'
    use       = r'(@use)([^\r\n]*)$'

    # Macro blocks
    openfb    = r'(:%s:)([^\r\n]*)$' % attrname
    openfbpy  = r'(:py:)([^\r\n]*)$'
    fbtext    = r'(.+)'
    fbclose   = r'(:%s:)[ \t]*$' % attrname

    # Program blocks
    interface   = r'(^@interface)([^:]+)(:)'
    function    = r'(@def)([^:]+)(:)'
    if_         = r'(@if)(.*?)' + prgsuffx      # Matches newlines
    elif_       = r'(@elif)(.*?)' + prgsuffx    # Matches newlines
    else_       = r'(@else)(.*?)' + prgsuffx    # Matches newlines
    for_        = r'(@for)(.*?)' + prgsuffx     # Matches newlines
    while_      = r'(@while)(.*?)' + prgsuffx   # Matches newlines

    # Tag blocks
    tagmodifs   = r'!'
    tagchar     = r'([^>\\]|\r|\n|\r\n)'
    newtag      = r'(\<[^>]*\>)'
    tagbegin    = r'(<%s?)(%s)' % (tagmodifs, attrname)
    tagend      = r'>'
    tagid       = r'#%s' % attrname
    tagclass    = r'\.%s' % symbol
    tagstyle    = r'(\{)([^\}]*)(\})'
    text        = r'[^<\r\n\\]+'

    tokens = {
        'root': [
            ( statement, stmttokens ),
            ( TTLLexer.commentline, Comment ),
            # Directives
            ( doctype, directivetokens ),
            ( body, directivetokens ),
            ( importas, directivetokens ),
            ( inherit, directivetokens ),
            ( implement, directivetokens ),
            ( use, directivetokens ),
            # States
            ( TTLLexer.cmtopen, Comment, 'comment' ),
            ( openfb, directivetokens, 'fb' ),
            ( openfbpy, directivetokens, 'fbpy' ),
            # Blocks
            ( interface, fntokens ),
            ( function, fntokens ),
            ( if_,  fntokens ),
            ( elif_, fntokens ),
            ( else_, fntokens ),
            ( for_, fntokens ),
            ( while_, fntokens ),
            ( tagbegin, bygroups(Operator, Name.Tag), 'tag' ),
            ( exprsubst, exprtokens ),
            ( text, Text ),
        ],
        'comment': [
            ( TTLLexer.cmtclose, Comment, '#pop' ),
            ( TTLLexer.cmttext, Comment ),
        ],
        'fb': [
            ( fbtext, Text ),
            ( fbclose, Operator, '#pop' ),
        ],
        'fbpy': [
            ( fbtext, pytokens ),
            ( fbclose, Operator, '#pop' ),
        ],
        'tag' :[
            ( tagid, Name.Class ),
            ( tagclass, Keyword.Declaration ),
            ( exprsubst, exprtokens ),
            ( tagstyle, styletokens ),
            ( attrname, Name ),
            ( r'=', Operator ),
            ( attrvalue, String ),
            ( r'[ \t]+', Text ),
            ( tagend, Operator, '#pop' ),
        ],
    }

    def get_tokens( self, text ):
        for x in super().get_tokens( text ) :
            print( x )
