Extending tayra with plugins
============================

Tayra templating language defines meta syntax which can be extended by
plugins. Right now there are three interfaces, defined by the languages, that
can be used to extend the language. The interfaces are,

- :class:`ITayraTags`, to handle template tags.
- :class:`ITayraFilterBlock`, to handle filter blocks in template-script.
- :class:`ITayraEscapeFilters`, to filter expression subtitution.

Implementing plugins for tag handlers
-------------------------------------

Diving a little bit into the internals, every tag definition will be handled
by a registered tag handler which will return an equivalent HTML snippet. It is
up to the tag-handler to interpret tokens, styles and attributes inside
template tags. Tag handlers can also interpret child elements and its text 
content.

So what are tag handlers ? They are plugins implementing :class:`ITayraTags`
interface. While interpreting a template-module (the compiled output of
template-script), tayra-runtime, which is a stack machine, will invoke
:class:`ITayraTags` plugins and will substitute the return value from the
plugin in the output HTML.

Here is a sample implementation of the plugin,

Implementing plugins for escape filters
---------------------------------------

Implementing plugins for filter blocks.
---------------------------------------
