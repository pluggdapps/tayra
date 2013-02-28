# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""
Tayra uses pluggdapps component architecture, and heavily based on plugins. The
lexer and parser are just a glue logic over a very sophisticated plugin
framework which does most of the language level heavy lifting. This modules
contains all the interface specifications that matters to tayra language
implementation.
"""

from pluggdapps.plugin import Interface

__all__ = [ 'ITayraTags', 'ITayraEscapeFilter', 'ITayraFilterBlock' ]

class ITayraTags( Interface ):
    """Interface specification to translate template tags to HTML tags.
    Plugins implementing this interface is defined under ``tayra.tags``
    package. It is possible for developers to implement their own plugins
    to translate template tags just by configuring
    :class:`tayra.compiler.TTLCompiler` plugin.
    """

    def handle( mach, tagname, tokens, styles, attributes, content ):
        """Called during runtime, translates tayra tag into HTML tags.
        Returns html string.

        ``mach``,
            Stackmachine.

        ``tagname``,
            Name of the tag.

        ``tokens``,
            List of tokens inside tag specification.

        ``styles``,
            List of CSS style parameters applicable on the tag.

        ``attributes``
            List of HTML attributes.

        ``content``,
            Descendants of this tag in plain string.
        """


class ITayraEscapeFilter( Interface ):
    """Interface specification for escape filtering results from expression 
    substitution.
    """
    def filter( mach, name, text ):
        """Apply the filtering logic to the text string and return processed
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

    def headpass1( igen, node ):
        """Will be called during the `headpass` phase 1, traversing AST. Can
        optionally return a value which will then be passed to headpass2.

        ``igen``,
            object to generate instructions.

        ``node``
            Passes the :class:`FilterBlock` node instance. Refer to the class
            documentation to learn more about the node defintion.
        """

    def headpass2( igen, node, result ):
        """Will be called during the `headpass` phase 2, traversing AST. Can
        optionally return a value which will then be passed to generate.

        ``igen``,
            object to generate instructions.

        ``node``
            Passes the :class:`FilterBlock` node instance. Refer to the class
            documentation to learn more about the node defintion.

        ``result``,
            Result from :meth:`headpass1`.
        """

    def generate( igen, node, result, *args, **kwargs ):
        """Will be called during the `generate` phase, traversing AST. Can
        optionally return a value which will then be passed to tailpass.

        ``igen``,
            object to generate instructions.

        ``node``
            Passes the :class:`FilterBlock` node instance. Refer to the class
            documentation to learn more about the node defintion.

        ``result``,
            Result from :meth:`headpass2`.
        """

    def tailpass( igen, node, result ):
        """Will be called during the `tailpass` phase, traversing AST. Can
        optionally return a value which will then be passed to tailpass.

        ``igen``,
            object to generate instructions.

        ``node``
            Passes the :class:`FilterBlock` node instance. Refer to the class
            documentation to learn more about the node defintion.

        ``result``,
            Result from :meth:`headpass2`.
        """


#---- This interface will be used for testing

class ITayraTestInterface( Interface ):
    """Just a test specification. You can conviniently igore this."""

    def render( *args, **kwargs ):
        """Return renderable html-text"""
