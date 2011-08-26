from zope.interface import Interface

class ITayraTag( Interface ):
    """Defines the plugin that handles tag generattion. This will will be used
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

class ITayraEscapeFilter( Interface ):

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

class ITayraFilterBlock( Interface ):

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
            the filter block, [ \t]*:fb-
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

class ITTLPlugins( Interface ):
    """Plugin implementers please note that the TTL plugins should have any
    code executing in the global context (for instance, using `fb-pycode
    global`) that depends on other plugins. This will either fail or trigger
    an error.
    """

    def implementers():
        """Return a list of ttl file urls either as absolute path or as,
        <packagename:file/path>. These template files are expected to
        implement interfaces, and hence they will be compile and executed to
        register their interfaces with ZCA.
        """
        return []


#---- This interface will be used for testing

class ITestInterface( Interface ):

    def render( *args, **kwargs ):
        """Return renderable html-text"""

