# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""
The design of tayra template language is heavily based on plugins. The
lexer and parser are just a glue logic over a very sophisticated plugin
framework which does most of the language level heavy lifting. The plugin
system is based on pluggdapps component architecture, and specifies interfaces
to be implemented as plugins.
"""

from pluggdapps.plugin import Interface

__all__ = [ 'ITayraTags', 'ITayraEscapeFilter', 'ITayraFilterBlock' ]

class ITayraTags( Interface ):
    """Interface specification to translate tayra tags to HTML tags."""

    def handle( mach, tagname, tokens, styles, attributes, content ):
        """Called during runtime, translates tayra tag into HTML tags.
        Return html string.

        ``mach``,
            Stachmachine

        ``tagname``,
            Name of the tag.

        ``tokens``,
            List of tokens inside tag specification.

        ``styles``,
            List of CSS style parameters applicable on the tag.

        ``attributes``
            List of HTML attributes.

        ``content``,
            Decendants of this tag in plain string.
        """

class ITayraEscapeFilter( Interface ):
    """Interface specification for escape filtering expression substitution.
    """
    def filter( mach, name, text ):
        """Apply the filter logic to the text string and return processed
        text.

        ``mach``,
            is stack-machine instance.

        ``name``,
            name of the filter.

        ``text``
            text, result of expression substitution, to be filtered.
        """


class ITayraFilterBlock( Interface ):
    """Interface specification for filter blocks to handle blocks of template
    code that does not follow indentation rules, can potentially have a
    separate syntax to themself and they can take part in multi-pass 
    compilation.
    """

    def headpass1( igen, filteropen, filtertext, filterclose ):
        """Will be called during the `headpass` phase 1, traversing AST. Can
        optionally return a value which will then be passed to headpass2.

        ``igen``,
            object to generate instructions.

        ``filteropen``
            First line opening the filter-block without any whitespace prefix,
            and without any trailing newlines.

        ``filtertext``
            Rest of the filterblock text except the closing line.

        ``filterclose``
            Will be the syntax to end a filter block without trailing
            newlines.
        """

    def headpass2( igen, result ):
        """Will be called during the `headpass` phase 2, traversing AST. Can
        optionally return a value which will then be passed to generate.

        ``igen``,
            object to generate instructions.

        ``result``,
            Result from :meth:`headpass1`.
        """

    def generate( igen, result, *args, **kwargs ):
        """Will be called during the `generate` phase, traversing AST. Can
        optionally return a value which will then be passed to tailpass.

        ``igen``,
            object to generate instructions.

        ``result``,
            Result from :meth:`headpass2`.
        """

    def tailpass( igen, result ):
        """Will be called during the `tailpass` phase, traversing AST. Can
        optionally return a value which will then be passed to tailpass.

        ``igen``,
            object to generate instructions.

        ``result``,
            Result from :meth:`headpass2`.
        """


#---- This interface will be used for testing

class ITayraTestInterface( Interface ):

    def render( *args, **kwargs ):
        """Return renderable html-text"""
