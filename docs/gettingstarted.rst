Install tayra
-------------

Installing via package management

.. code-block:: bash

  # -Z to do unzipped install. The reason for installing it in un-zipped form
  #    is to make use of the command line tool.
  # -U to upgrade install
  easy_install -Z -U tayra

**Source code**

* Download the latest tar.gz from http://pypi.python.org/pypi/tayra
* Check out hg repository from `google_code <http://code.google.com/p/tayra/>`_
  or `bit-bucket <https://bitbucket.org/prataprc/tayra>`_

.. code-block:: bash

  hg clone https://code.google.com/p/tayra/
  # or
  hg clone https://bitbucket.org/prataprc/tayra

Command line usage
------------------

Make sure that tayra package is installed in your environment (using
easy_install) or available via ``PYTHONPATH``.  ``tayra/tyr.py`` script under 
tayra-package can be used as command line tool. Either invoke it from its 
original path, or create a symbolic link to a bin/ directory.

``script-file:    <site-package>/tayra/tyr.py``

symbolic link to your binary path, like,

.. code-block:: bash

    ln -s <site-package>/tayra/tyr.py $(HOME)/bin/tyr.py
    # or,
    ln -s <site-package>/tayra/tyr.py /usr/bin/tyr.py

Once ``tyr.py`` is available as an executable command and `tayra` module 
in your python path, use the command-line tool, like,

.. code-block:: bash

  # A corresponding .html file will be generated in the same directory
  tyr.py <template-file>
  # For more help, try
  tyr.py -h

Using it as library, in python
------------------------------

.. code-block:: python

    pa = Pluggdapps.boot( None )
    compiler = pa.query_plugin( pa, ISettings, 'ttlcompiler' )
    # Compile
    code = compiler.compilettl( file=ttlfile )
    # Load
    module = compiler.load( code, context=context )
    # Generate
    html = compiler.generatehtml( module, context )

  
Start templating
----------------

It starts with your .ttl file, where ''ttl'' stands for tayra template language.
Open your favorite editor and we will start writing our first template.
Ofcourse our first template is going to be a welcome message to this world.

.. code-block:: html

    ## File name : eg1.ttl

    <html>
      <head>
      <body>
        <p> hello world

Let us now translate this to a html document,

.. code-block:: bash

    # Assuming that tayra is available in your environment,
    $ tayra/tyr.py eg1.ttl

which looks like,

.. code-block:: html

    <html>
      <head></head>
      <body>
        <p> hello world</p>
      </body>
    </html>

Now, we will add an id and couple of class attributes to the paragraph tag that
contains the `hello world` text.

.. code-block:: html

    ## File name : eg1.ttl

    <html>
      <head>
      <body>
        <p#welcome.intro.highlight> hello world

`#welcome` attributes the tag with id-name `welcome` and
`.intro.highlight` attributes the tag with class-names `intro` and
`highlight`. And our translated html looks like

.. code-block:: html

    # { 'background-color' : '#EEE' }
    <html>
      <head></head>
      <body>
        <p id="welcome" class="intro highlight"> hello world</p>
      </body>
    </html>

That is all it takes to get you started. You will know everything about 
tayra here.

