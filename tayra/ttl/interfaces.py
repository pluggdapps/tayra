from zope.interface import Interface

class ITayraTags( Interface ):

    def handlers():
        """Return a dictionary of tag->handler, where the handler is expected
        to have the following signature
            handler( mach, tagname, specifiers, style, attrs tagfinish )
        """

class ITTLPlugins( Interface ):

    def implementers():
        """Return a list of ttl file urls either as absolute path or as,
        <packagename:file/path>. These template files are expected to
        implement interfaces, and hence they will be compile and executed to
        register their interfaces with ZCA.
        """
        return []
