# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

from zope.interface import Interface

class ITayraPlugin( Interface ):
    """The design of tayra template language is heavily based on plugins. The
    lexer and parser are just a glue logic over a very sophisticated plugin
    framework which does most of the language level heavy lifting. The plugin
    architecture is based on Zope Component Architecture (ZCA) with interfaces
    specifying how plugins need to be implemented and consumed. ITayraPlugin
    acts as the base class for all of tayra's interface specifications, which
    are,
        > ITayraTag
        > ITayraEscapeFilter
        > ITayraFilterBlock
    ''Note that these interface specs. have nothing to do with template plugins
    that can be created using TTL (Tayra Template Language).''
    """

class ITayraTag( ITayraPlugin ):
    """Tayra templating is a HTML templating tool (it can also be used for any
    xml compatible markups). Assuming that you are familiar with HTML, we will
    explain how tags are generated while translating a .ttl file into .html
    format.

    Defines the plugin that handles tag generattion. This will will be used
    by the AST node, TagLine and TagBlock during every pass, i.e headpass1,
    headpass2, generate, tailpass.

    Use the `node` object for all contextual operations. There is a default
    class `TagPlugin` implementing this interface from which other tag-plugins
    can choose to derive from.
    """

    def headpass1( node, igen ):
        """Will be invoked during headpass1(). It is the reponsibility of the
        implementing class to decide how to take this pass further into the
        sub-tree. To discontinue with the headpass1() on node's children,
        return `False` other wise return `True`.

        ``node``,
            points to the AST non-terminal node instance which can be
            either TagLine() or TagBlock().
        ``igen``,
            InstrGen() object, using will the plugin will have the full power
            of generating the intermediate python code.
        """

    def headpass2( node, igen ):
        """Will be invoked during headpass2(). It is the reponsibility of the
        implementing class to decide how to take this pass further into the
        sub-tree. To discontinue with the headpass1() on node's children,
        return `False` other wise return `True`.

        ``node``,
            points to the AST non-terminal node instance which can be
            either TagLine() or TagBlock().
        ``igen``,
            InstrGen() object, using will the plugin will have the full power
            of generating the intermediate python code.
        """

    def generate( node, igen, *args, **kwargs ):
        """Will be invoked during headpass2(). It is the reponsibility of the
        implementing class to decide how to take this pass further into the
        sub-tree.

        ``node``,
            points to the AST non-terminal node instance which can be
            either TagLine() or TagBlock().
        ``igen``,
            InstrGen() object, using will the plugin will have the full power
            of generating the intermediate python code.
        """

    def tailpass( node, igen ):
        """Will be invoked during headpass1(). It is the reponsibility of the
        implementing class to decide how to take this pass further into the
        sub-tree. To discontinue with the headpass1() on node's children,
        return `False` other wise return `True`.

        ``node``,
            points to the AST non-terminal node instance which can be
            either TagLine() or TagBlock().
        ``igen``,
            InstrGen() object, using will the plugin will have the full power
            of generating the intermediate python code.
        """

    def handle( node ):
        """Called during runtime,
        return a dictionary of tag->handler, where the handler is expected
        to have the following signature
            handler( mach, tagname, specifiers, style, attrs tagfinish )
        """

class ITayraEscapeFilter( ITayraPlugin ):

    def do( self, mach, text, filterns=None ):
        """Apply the filter logic to the text string and return processed
        text.

        ``mach``,
            is stach-machine instance.
        ``text``
            text to be filtered.
        ``filterns``
            namespace used to invoke this filter implemetation.
        """

class ITayraFilterBlock( ITayraPlugin ):

    def __call__( parser, filteropen, filtertext, filterclose ):
        """Will be called when a new filter block matches with the interface
        implementer. More specifically, the plugin will be called when a
        matching Non-terminal filter-block node is being instantiated.

        ``parser``
            parser object from PLY, parser.ttlparser points to TTLParser
            instance and, ttlparser.ttlconfig will provide the configuration
            dictionary provided by the application code.
        ``filteropen``
            will be the syntax including the preceeding whitespace that starts
            the filter block, [ \t]*:fb-name
        ``filtertext``
            filter text including indentations and newlines that happen to
            come after the `filteropen`
        ``filterclose``
            will be the syntax to end a filter block including the trailing
            newlines
        """

    def headpass1( igen ):
        """Will be called during the `headpass` phase 1, traversing AST.

        ``igen``,
            object to generate instructions.
        """

    def headpass2( igen ):
        """Will be called during the `headpass` phase 2, traversing AST.

        ``igen``,
            object to generate instructions.
        """

    def generate( igen, *args, **kwargs ):
        """Will be called during the `generate` phase, traversing AST.

        ``igen``,
            object to generate instructions.
        """

    def tailpass( igen ):
        """Will be called during the `tailpass` phase, traversing AST.

        ``igen``,
            object to generate instructions.
        """

class ITTLPlugins( ITayraPlugin ):
    """
    Template-plugins will have to be automatically loaded during tayra-module
    initialization. This can happen only when there is a mechanism that provides a
    list of plugin implementers (as .ttl files) as part of package entry-point.
    Something like,
    {{{ Code ini
      [tayra.plugins]
      ITTLPlugin = bootstrap.implement:TTLPlugins
    }}}
    to be more specific, //ITTLPlugin// is the interface specification for this
    entry point.
    
    :Gotcha ::
        Plugin implementers please note that the TTL plugins should have any
        code executing in the global context (for instance, using ``{b}fb-pycode
        global``) that depends on other plugins, it is bound to fail or
        trigger an error.
    """

    def implementers():
        """Return a list of ttl file urls either as absolute path or as
        asset-specifcation, //<packagename:file/path>//. These template files
        are expected to implement template-interfaces, and hence they will be
        compiled and executed to register their interfaces with ZCA's
        global-site-manager.
        """
        return []


#---- This interface will be used for testing

class ITestInterface( Interface ):

    def render( *args, **kwargs ):
        """Return renderable html-text"""

