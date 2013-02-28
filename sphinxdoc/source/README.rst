What is Tayra template ?
========================

Tayra is a full-featured abstract markup language to template web documents.
It is primarily inspired from 
`mako-templates <http://www.makotemplates.org/>`_ and
`HAML <http://haml-lang.com/>`_ (especially the indentation based
markup definitions). Although it is young and relatively a new kid among
the old-timers, it can be considered as the evolutionary next step for some of
them. And probably it is the only templating language that allows developers
to build and distribute their templates as plugins, not to mention the fact
that tayra's implementation itself is heavily based on plugins.

Example,

.. code-block:: ttl

    <div .pluggdappsfooter>

    <div>
      powered by pluggdapps, 
      <span {font-style : italic}> ${counts['plugins']} plugins
      implenting
      <span {font-style : italic}> ${counts['interfaces']} interfaces

    @while navigate :
      @@crumbsname, crumbsurl = navigate.pop(0)

      <li .crumbs>
        <a .crumbname "${crumbsurl or ''}"> ${crumbsname}
        <ul .menu>

          @for name, url in sorted( crumbsmenu[crumbsname] ) :
            <li .item> <a "${url}"> ${name}

      @if navigate :
        <li .crumbsep> &raquo;

Features
--------

- concise and beautiful syntax.
- based on pluggdapps component architecture.
- leverages on pluggdapps' configuration system.
- pluggable tag handlers for custom tag elements.
- compiles down to optimal python code and optionally memcached. Also possible
  to persist the intermediate python code to avoid re-compilation in case of
  server restart.
- works with python 3.x.
- has full unicode support.
- full programmability available via,

  - expression substitution with optional escape encoding.
  - control-blocks like if-elif-else.
  - looping contructs like for / while.
  - python statements.

- template abstraction using function blocks, with its own local scope.
- import other template scripts into the local namespace and access their
  functions
- template inheritance for re-usable web-layouts.
- extensible filter blocks.
- and unique ability to create template plugins, distribute them as
  separate package.
- easy to debug. when used with pluggdapps' ``CatchAndDebug`` pugin, exception
  tracebacks are tweaked to directly point to the correct line in the
  template.

Getting it
----------

There are multiple ways to install tayra and the easiest way is using
easy_install.

.. code-block:: bash

  # -Z to do unzipped install. The reason for installing it
  #    in un-zipped form is to make use of the command line tool.
  # -U to upgrade install
  easy_install tayra

  # If beautify_html configuration option is desired,
  easy_install beautifulsoup4 

  # To compile sphinx documentation
  easy_install sphinx

**Install from source code**,

Alternately, you can obtain the source code,

- downloading the `tar.gz <http://pypi.python.org/pypi/tayra>`_
- cloning from one of the many places mentioned below.

.. code-block:: bash

  hg clone https://code.google.com/p/tayra/
  # or
  hg clone https://bitbucket.org/prataprc/tayra
  # or 
  git clone https://github.com/prataprc/tayra.git

tayra uses mercurial as native repository.

After untarring the source package, or cloning the source repository into
your local machine, install source package by executing,

.. code-block:: bash

  > sudo python ./setup.py install
  > sudo python ./setup.py develop # to install the development version

License
-------

Tayra is distributed under `GPLv3 license <http://www.gnu.org/licenses/>`.

**Requires : Linux, Python-3.x, Pluggdapps, PLY.**

Using it as python library
--------------------------

.. code-block:: python

    pa = Pluggdapps.boot( None )
    compiler = pa.query_plugin( pa, ISettings, 'ttlcompiler' )
    # Compile
    code = compiler.compilettl( file=ttlfile )
    # Load
    module = compiler.load( code, context=context )
    # Generate
    html = compiler.generatehtml( module, context )

  
Development
-----------

Tayra template language is defined as a bunch of meta syntax that can be
extended and customised using plugins. Developers can author plugins
implementing one or more interfaces specified by the tayra-package. Tayra's
plugin system is based on pluggdapps component architecture.

It is always better to setup the development tree under a virtual environemnt.
To begin with, first checkout the source tree from the latest repository tree
and then use the ``make`` command to create a development environment.

.. code-block:: bash

  cd tayra
  make develop

which,

- sets-up a virtual environment under ``tayra-env/`` directory.
- Installs tayra under the virtual environment in development
  mode ``python ./setup.py develop``

.. code-block:: bash

  source ./tayra-env/bin/activate # To start using the tayra package
  make bdist_egg        # For creating binary distribution
  make sdist            # For creating source distribution
  make test             # To test the package
  make upload           # To build the egg and upload it into pypi

- The .egg package will be availabe under dist/ directory
- If you enable ['beautify_html'] option, you will have to install
  beautifulsoup4 package.

