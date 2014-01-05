tayra.basettlplugin
-------------------

-- configuration is not supported by plugin --

tayra.expressionevalpy
----------------------

-- configuration is not supported by plugin --

tayra.expressionpy
------------------

-- configuration is not supported by plugin --

tayra.filterblockpy
-------------------

-- configuration is not supported by plugin --

tayra.html5
-----------

-- configuration is not supported by plugin --

tayra.html5forms
----------------

-- configuration is not supported by plugin --

tayra.tags
----------

-- configuration is not supported by plugin --

tayra.ttlcompiler
-----------------

helpers
    Comma separated list of python modules. These modules will be imported
    and its namespace will be merged with template context and can be
    refered as ``h.``.

nocache
    If set to True, will not persist the intermediate python file.

encoding
    Encoding to use while reading the template script file.

cache_directory
    Directory path telling the compiler where to persist (cache)
    intermediate python file.

yacctab
    PLY-Yacc option. Points to the yacc table that's used for optimized
    mode. Only if you're modifying the parser, make this point to a local
    yacc table file.

yacc_outputdir
    To change the directory in which the PLY YACC's parsetab.py file (and
    other output files) are written.

tag.plugins
    Comma separated list of tag plugins to use. Plugins in the specified
    order will be invoked to handle the template tags, so the order of the
    plugin is important.

yacc_debug
    PLY-Yacc option. Run yaccer in debug mode.

directories
    Comma separated list of directory path to look for a template file.
    Default will be current-directory.

expression.default
    Default plugin to use for evaluating text in expression substitution.
    This plugin will be used if filter() callfails in other
    ITayraExpression plugins.

optimize
    PLY Lexer/Yaccer option. For improved performance, it may be desirable
    to use Python's optimized mode (e.g., running Python with the -O
    option). However, doing so causes Python to ignore documentation
    strings. This presents special problems for lexer and parser. To
    handle this case, you can set this parameter to ``1``. For more
    information refer,  http://www.dabeaz.com/ply/ply.html#ply_nn15.

lextab
    PLY-Lexer option. Points to the lex table that's used for optimized
    mode. Only if you're modifying the lexer and want some tests to avoid
    re-generating the table, make this point to a local lex table file.

beautify_html
    Boolean, if True will generate human readable html output. Make sure
    that BeautifulSoup, beautifulsoup4, is installed. Do not enable this
    in production mode, might slow down the web page.

entry_function
    Entry point, function in python module, into compiled template script.

input_encoding
    Default input encoding for .ttl file.

memcache
    Cache the compiled python code in-memory to avoid re-compiling .ttl to
    .py file.

strict_undefined
    Boolean to raise exception for undefined context variables. If set to
    false, undefined variables will be silently digested as 'None' string.

lex_debug
    PLY-Lex option. Run lexer in debug mode.


tayra.xyztestinterface
----------------------

-- configuration is not supported by plugin --

