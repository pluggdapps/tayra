Extending Tayra language
========================

The language is defined as a bunch of meta syntax that can be extended and
customised using plugins. Developers can author plugins implementing one or
more interfaces specified in :mod:`tayra.interfaces` module. Tayra's plugin
system is based on pluggdapps component architecture.

The design is based on simple, formal methods that are easy to understand
and extend as per future needs. Language front end is based on LALR parser and
uses PLY for lexing and parsing, during parsing, Abstract Syntax Tree (AST) is
constructed using :class:`tayra.ast.Terminal` and 
:class:`tayra.ast.NonTerminal` base classes. A multi-pass compilation is 
applied on the AST, two headpasses for preprocessing, generation pass to 
generate intermediate python file and a tail pass to do post processing. Some 
times tail pass on a sub-tree can be used to perform a delayed generation of
intermediate python file. AST nodes also provide methods to reverse generate
the source text and to print the tree on stdout for reference.

Lexing rules are implemented in :mod:`tayra.lexer` module and parsing grammar
is implmeneted in :mod:`tayra.parser` module. 

Intermediate file is a regular python file containing imports, functions,
support code and a stack-machine. Except the directives, rest of the template
text gets compiled into stack-machine instructions by AST nodes.

Extending Tayra language
------------------------

Like mentioned above many aspects of the language are implemented using
plugins and these plugins can be customised, configured or even replaced.
Eventually we expect all the code to reside in one plugin or the other,
thereby providing maximum flexibility. Right now tayra can be extended using
the following interfaces,

**tayra.interfaces.ITayraTags**

In its simplest use case, tayra is just plain HTML without the closing
tags. But behind the scene these tag elements are parsed and passed to
ITayraTags plugins, where plugins are configured using
``TTLCompiler['use_tag_plugins']`` settings. Here is an example,

.. code-block:: ttl
    :linenos:

    <form on>
      First name : <inptext :firstname>
      <br>
      Last name  : <inptext :lastname>

uses `inptext` tag, a non-standard tag, implemented by ``TayraHTML5Forms``
plugin, where tokens within the tag definition are parsed and interpreted by
plugins and are taken into account while generating a corresponding HTML 
text. You can refer :mod:`tayra.tags.forms` module for more information on
how to implement a :class:`tayra.interfaces.ITayraTags` plugin.

**tayra.interfaces.ITayraExpression**

Expressions can be substituted inside a template file using **${...}** syntax.
Additionally, evaluated output can be passed to filters using **${... |
<filters> }** the pipe token, where `filters` is comma separated value of
filters to be applied in specified order.

.. code-block:: ttl
    :linenos:

    <li #crumbs>
      <a .crumbname "${crumbsurl or '' | u }"> ${crumbsname}
      <ul :menu {color : blue}>

Behind the scenes, expression substitution is handled by plugins implementing
implementing :class:`tayra.interfaces.ITayraExpression` interface. While
coding an expression inside a template script it is possible to target the
expression for specific plugin, like,

.. code-block:: ttl
    :linenos:

    @@l = [1,2,3]

    ## Evaluating with expression extension
    <div> ${-evalpy l.append(10)}
    <div> ${-py l}
    <div> ${-evalpy l.pop(0)}
    <div> ${l}

where, ``-evalpy`` and ``-py`` refers to plugin name. For instance ``-evalpy``
will refer to a plugin whose class name is ``TayraExpressionEvalPy``, note the
`TayraExpression` prefix in the class name. Similarly ``-py`` will refer to
plugin whose class name is ``TayraExpressionPy``. The difference between
`-eval` and `-py` is that in the former case expression is only evaluated in
the global and local scope and in the later case expression is both evaluated
and substituted.

If an expression is coded without a target plugin then default plugin will be
picked based on the configuration parameter
``TTLCompiler['expression.default']``. To learn more about expression
substitution and filtering refer to :class:`tayra.interfaces.ITayraExpression`
interface specification.

**tayra.interfaces.ITayraFilterBlock**

Filter blocks provide powerful yet a generic way to extend the template
language. Filter blocks are handled by plugins implementing
:class:`tayra.interfaces.ITayraFilterBlock` interface and they take part in
multi-pass compilation. Although filter-blocks cannot blend with ttl-language 
syntactically, they can provided features that can be closely integrated with
the template language.

``:py:`` filter block in implemented by :class:`tayra.filterblocks.pycode`
plugin. Using this developers can add python code blocks inside the template
script, both in local scope and global scope. For EG,

.. code-block:: ttl
    :linenos:

    @interface ITTLBreadCrumbs.default_settings( self ):
      :py:
      ds = h.ConfigDict()
      ds.__doc__ = "Configuration settings for `tbreadcrumbs`"

      ds['type']  = {
          'default'  : 'simple',
          'types'    : (str,),
          'options'  : ('simple', 'styled', 'collapsible', 'none'),
          'help'     : "Type of bread crumb styling."
      }
      :py:
      @@return ds

**Setting up,**

It is always better to setup the development tree under a virtual environemnt.
To begin with, first checkout latest source tree from the repository and then
use the ``make`` command to create a development environment.

.. code-block:: bash
    :linenos:

    $ cd tayra
    $ make develop

- sets-up a virtual environment under ``tayra-env/`` directory.
- installs tayra under the virtual environment in development
  mode ``python ./setup.py develop``

List of make commands
---------------------

.. code-block:: bash
    :linenos:

    $ source ./tayra-env/bin/activate # To start using the tayra package

    # Setup virtual environment under tayra-env/ directory. And installs
    # sphinx generator package.
    $ make develop

    # Test tayra package with standard test cases.
    $ make testall

    # Install other template packages for benchmark.
    $ make bench-setup

    # Execute the bench-mark suite. This is work in progress, you can
    # help me to setup this benchmark.
    $ make benchmark

    # Generate binary egg distribution.
    $ make bdist_egg

    # Generate source distribution. This is the command used to generate
    # the public distribution package.
    $ make sdist

    # Generate sphinx documentation.
    $ make sphinx-compile

    # Generate sphinx documentation and zip the same for package upload.
    $ make sphinx

    # Upload package to python cheese shop (pypi).
    $ make upload

    # Create vim package to upload into vim script base.
    $ make vimplugin

- after doing a `bdis_egg` or `sdist`, .egg packages will be availabe under
  ``dist/`` directory
- if you enable ['beautify_html'] configuration option in
  :class:`tayra.compiler.TTLCompiler` plugin you will have to install 
  ``beautifulsoup4`` package.

	
Push code to repositories
-------------------------

From source root, 

.. code-block:: bash
    :linenos:

    # for code.google.com
	$ hg push https://<username>@code.google.com/p/tayra/

    # for bitbucket.org
	$ hg push https://<username>@bitbucket.org/prataprc/tayra

To push code into github, you may need to use install `mercurial-git` package
in ubuntu. And login to git account and
`add your public-key <https://help.github.com/articles/generating-ssh-keys>`_.

.. code-block:: bash
    :linenos:

	$ hg bookmark -f -r default master
	$ hg push git+ssh://git@github.com:prataprc/tayra.git
