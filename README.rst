What is Tayra template ?
========================

Tayra templating is a full-featured abstract markup language used to describe
web-documents. It is primarily inspired from
`mako-templates <http://www.makotemplates.org/>`_ and
`HAML <http://haml-lang.com/>`_ (especially the indentation based
markup definitions). Although it is young and relatively a new kid among
the old-timers, it can be considered as the evolutionary next step for some of
them ( if not all :) ). And probably it is the only templating
language that allows developers to build and distribute their templates
as plugins, not to mention the fact that tayra's implementation itself is
heavily based on plugins. We will finish this short introduction by stating
that, inspite of being a younger sibling to its likes, it is faster than many
of them.

You can learn more and hack into its guts at
`google-code <http://code.google.com/p/tayra/>`_

Some interesting features in tayra are,

* concise and beautiful syntax.
* pluggable tag handlers for custom tag elements.
* full programmability available via,
  ** expression substitution
  ** control-blocks like if-elif-else
  ** looping contructs like for / while
* templates abstraction using function blocks, with its own local scope.
* import other template files into the local namespace and access their
  functions
* template inheritance for re-usable web-layouting.

And the unique ability to write template plugins, package and 
distribute them.

Quicklinks
----------

* `README <http://tayra.pluggdapps.com/readme>`_
* `CHANGELOG <http://tayra.pluggdapps.com/changelog>`_
* `Track tayra development `google-code <http://code.google.com/p/tayra/>`_
* If you have any queries, suggestions
  `discuss with us <http://groups.google.com/group/pluggdapps>`_

Documentation
-------------

* `Tayra reference <http://tayra.pluggdapps.com/reference>`_

Installation
------------

There are multiple ways to install tayra and the easiest way is by 
easy_install.

.. code-block:: bash

  # -Z to do unzipped install. The reason for installing it
  #    in un-zipped form is to make use of the command line tool.
  # -U to upgrade install
  easy_install -Z -U tayra

**Install from source code**,

You can obtain the source code by, downloading the latest 
`tar.gz <http://pypi.python.org/pypi/tayra`_ or cloning from mercurial 
repositories.

.. code-block:: bash

  hg clone https://code.google.com/p/tayra/
  # or
  hg clone https://bitbucket.org/prataprc/tayra

After untarring the source package, or cloning the source repository into
your local machine, install source package by executing,

.. code-block:: bash

  > sudo python ./setup.py install
  > sudo python ./setup.py develop # to install the development version

Command line usage
------------------

Make sure that tayra package is installed in your environment (using
easy_install) or available via ``PYTHONPATH``.  **tayra/tyr.py** script under
tayra-package can be used as command line tool. Either invoke it from its
original path, or create a symbolic link to a bin/ directory.

script-file:    <site-package>/tayra/tyr.py

symbolic link to your binary path, like,

.. code-block:: bash

    ln -s <site-package>/tayra/tyr.py $(HOME)/bin/tyr.py
    # or,
    ln -s <site-package>/tayra/tyr.py /usr/bin/tyr.py

Once `tyr.py` is available as an executable command and `tayra` module 
in your python path, use the command-line tool, like,

.. code-block:: bash

  # A corresponding .html file will be generated in the same directory
  tyr.py <template-file>
  # For more help, try
  tyr.py -h

Using it as python library
--------------------------

.. code-block:: python
    from   tayra  import Renderer

    # `ttlloc` specifies the path to template file, ttlloc is interpreted as
    # relative path or asset specification format
    # `ttlconfig` passes the configuration parameters
    r = Renderer( ttlloc=ttlloc, ttlconfig=ttlconfig )
    # Context is python dictionary that will be imported into template namespace
    html = r( context=context )
    codecs.open( htmlfile, mode='w', encoding=encoding).write( html )

    # To pass template text directly (instead of file-path)
    r = Renderer( ttltext=ttltext, ttlconfig=ttlconfig )
    html = r( context=context )

  
Development
-----------

It is always better to setup the development tree under a virtual environemnt.
To begin with, first checkout the source tree from the latest repository tree
and then use the ''make'' command to create a development environment.

.. code-block:: bash
  cd tayra
  make develop

which,
* sets-up a virtual environment under // tayra-env/ // directory.
* Installs tayra under the virtual environment in development mode,
  [<PRE python ./setup.py develop >]

.. code-block:: bash
  source ./tayra-env/bin/activate # To start using the tayra package
  make bdist_egg        # For creating binary distribution
  make sdist            # For creating source distribution
  make test             # To test the package
  make upload           # To build the egg and upload it into pypi

The .egg package will be availabe under dist/ directory
