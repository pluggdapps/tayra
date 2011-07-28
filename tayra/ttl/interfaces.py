from zope.interface import Interface

class ITayraTags( Interface ):

    def handlers():
        """Return a dictionary of tag->handler, where the handler is expected
        to have the following signature
            handler( mach, tagname, specifiers, style, attrs tagfinish )
        """

class ITayraEscapeFilter( Interface ):

    def __call__( self, mach, text ):
        """Apply the filter logic to the text string and return processed
        text.

        ``mach``,
            is stach-machine instance.
        ``text``
            text to be filtered.
        """

class ITayraFilterBlock( Interface ):

    def __call__( filteropen, filtertext, filterclose ):
        """Will be called when a new filter block matches with the interface
        implementer. More specifically, the plugin will be called when a
        matching Non-terminal filter-block node is being instantiated.

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

    def implementers():
        """Return a list of ttl file urls either as absolute path or as,
        <packagename:file/path>. These template files are expected to
        implement interfaces, and hence they will be compile and executed to
        register their interfaces with ZCA.
        """
        return []

