0.42dev
-------

``Wed May 29, 2013``

- CHANGELOG.rst and TODO.rst are web-friendly.

- Removed unwanted glob-patterns from MANIFEST.in

- Sphinx documentation, min-width is set to 970px.

- TTLCompiler compiler implements `pluggdapps.interfaces.ITemplate` interface.

- ``@import`` is now used for importing python modules and ``@include`` is now
  used for importing TTL template-modules. Test cases added to verify this.

- Bug fixes while making h.packagedin() calls.


0.41dev
-------

``Tue May 21, 2013``

- Catalog of configuration settings for tayra plugins is automatically
  generated using pluggapps' ``pa-script`` and sphinx-documented.

- From tayra command line -c switch accepts a context file containing a
  python dictionary as context, which is supplied as template context.

- Plugins are referred using its canonical-name.

- Moved sphinx documentation to docs/ directory.

0.4dev
------

``Tue Mar 12, 2013``

- support inline tags along with text. Eg, 
  ``<div> hello world <span> how are you``

- Tags can also be nested in a text line. Eg,
  ``First name : <inptext :firstname>``

- Added `tagspan` and `textspan` grammar to support nested tags in the same
  line.

- Added @@return statement, where template functions can return objects
  other than template code. A corresponding popobject() instruction is added.

- Template plugins can define configuration settings using ConfigDict and
  default_settings method. Although settings value must always be
  string. ``ISettings`` methods added for BaseTTL and other plugins
  implemented in tayra.

- Package info (package() entry point) returns list of template plugins
  available in tayra package.

- Lexer preserves the token and its line no in ttl text while passing them to
  the parser.

- Line no information from lexer are coded in the intermediate python file
  in debug mode to accurately map exceptions to the correct line in the
  ttl-file.

- Revamped filter block handling in ast and pycode.

- Codegen used __traceback_decorator__ to map exceptions to ttl file location.

- Improved vim-plugin for TTL filetype.

- Expression substitution is made pluggable. Any text within the ``${ ... }``
  syntax is now handled by a runtime plugin implementing `ITayraExpression`
  interface.

- TTLCompiler['expression.default'] configuration parameter specifies
  the default `ITayraExpression` plugin to handle the expression.

- To invoke a specific plugin, ``${-<name> ... }``,
  where <name> is the plugin name to handle expression substitution.

- Renamed TTLCompiler['use_tag_plugins'] to TTLCompiler['tag.plugins'].

- ITayraEscFilter specification is merged with ITayraExpression interface
  specification.

- TayraExpression plugin `py` added. This plugin is configured as the default
  handler for expression substitution.

- TayraExpression plugin `evalpy` added.

- Added test cases for pluggable expression substitution feature.

Instead of blindly importing all utility functions from pluggdapps.utils,
these functions are first imported, individually, into tayra.utils and
then populated into a container object. This container object is finally made
available in template context as ``h``. Eg, ::

    <head>
    <body>
        ${ h.parsecsv( 'one, two, three' ) }
        ${ h.parsecsvlines( 'one, \\n two,
        three' ) }
        ${ dir(h) }


0.3dev
------

``Sat Jan 05, 2013``

- Migrating tayra to pluggdapps component system.
- Migrating tayra to python 3.2
- Updated test cases and benchmarks to this revision.

0.2dev
------

``Tue Dec 06, 2011``

- Documentation

0.1dev
------

``Sat Nov 05, 2011``

Initial version of tayra.  A non-exhaustive list of features and functions
available from tayra.

- ``expression substitution``, substitute dynamic content anywhere in your
  document using python expression.

- ``escaping text``, while substituting text, it can be escaped with one or
  more filters. While escape-filters themselves can be added as plugins to 
  tayra.

- ``filter blocks``, process non-template text and substitute the filter block
  with processed text (optional). One such example can be a block of python code
  that need to do some ``view`` related processing. And ofcourse one can 
  create any many types of filter-blocks (plugins !!)

- ``control blocks``, make use of control blocks like ``if-elif-else``, to
  conditionally select portions of templates. And ``for/while`` loop to repeate
  blocks of template text.

- ``functions``, abstract re-usable blocks of templates into functions with its
  own local scope and local-context.

- ``import templates``, import templates from other parts of the source tree
  into the current template's namespace and access their function blocks.

- ``inheritance``, there is a simple yet powerful idea of inheritance, whereby
  templates can have a long chain of inheritance from the base layout. A
  template module in the chain can access any other inheriting or inherited
  templates using the ``parent`` and ``next`` namespace, while ``self``
  namespace provides you the magic of overriding.

- ``how to use``, Can be used via its well-defined API or from command line.
