Development
===========

The language is defined as a bunch of meta syntax that can be extended and
customised using plugins. Developers can author plugins implementing one or
more interfaces specified in :mod:`tayra.interfaces` module. Tayra's plugin
system is based on pluggdapps component architecture.

The design is based on simple, formal methods that are easy to understand
and extend as per future needs. Language front end is based on LALR parser and
uses PLY for lexing and parsing, during parsing, Abstract Syntax Tree (AST) is
constructed using :class:`tayra.ast.Terminal` :class:`tayra.ast.NonTerminal`
base classes. A multi-pass compilation is applied on the AST, two headpasses
for preprocessing, generation pass to generate intermediate python file and a
tail pass to do post processing. Some times tail pass can be used to perform 
a delayed generation of intermediate python file. AST also supports methods to
reverse generate the source text and to print the tree to stdout for
reference.

Lexing rules are implemented in :mod:`tayra.lexer` module and parsing grammar
is implmeneted in :mod:`tayra.parser` module. 

Intermediate file is a regular python file containing imports, functions,
support code and a stack-machine. Except directives rest of the template text
gets compiled into stack-machine instructions by AST nodes.

It is always better to setup the development tree under a virtual environemnt.
To begin with, first checkout the source tree from the latest repository tree
and then use the ``make`` command to create a development environment.

.. code-block:: bash

  cd tayra
  make develop

- sets-up a virtual environment under ``tayra-env/`` directory.
- installs tayra under the virtual environment in development
  mode ``python ./setup.py develop``

List of make commands
---------------------

.. code-block:: bash

  source ./tayra-env/bin/activate # To start using the tayra package

  # Setup virtual environment under tayra-env/ directory. And installs sphinx
  # generator package.
  make develop

  # Test tayra package with standard test cases.
  make testall

  # Install other template packages for benchmark.
  make bench-setup

  # Execute the bench-mark suite. This is work in progress, you can help me to
  # setup this benchmark.
  make benchmark

  # Generate binary egg distribution.
  make bdist_egg

  # Generate source distribution. This is the command used to generate the
  # public distribution package.
  make sdist

  # Generate sphinx documentation.
  make sphinx-compile

  # Generate sphinx documentation and zip the same for package upload.
  make sphinx

  # Upload package to python cheese shop (pypi).
  make upload

  # Create vim package to upload into vim script base.
  make vimplugin

- after doing a `bdis_egg` or `sdist`, .egg packages will be availabe under
  ``dist/`` directory
- if you enable ['beautify_html'] option TTLCompiler plugin you will have to
  install ``beautifulsoup4`` package.

	
Push code to repositories
-------------------------

push-googlecode:
	hg push https://prataprc@code.google.com/p/tayra/

push-bitbucket:
	hg push https://prataprc@bitbucket.org/prataprc/tayra

push-github:
	hg bookmark -f -r default master
	hg push git+ssh://git@github.com:prataprc/tayra.git
