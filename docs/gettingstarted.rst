Getting started
===============

There are multiple ways to install tayra and the easiest way is using
``pip``.

.. code-block:: bash
    :linenos:

    # -Z to do unzipped install. The reason for installing it
    #    in un-zipped form is to make use of the command line tool.
    # -U to upgrade install
    $ pip install tayra

    # if beautify_html configuration option is desired,
    $ pip install beautifulsoup4 

    # generate sphinx documentation
    $ pip install sphinx

**Install from source code**,

Alternately, you can obtain the source code by,

- downloading the `tar.gz <http://pypi.python.org/pypi/tayra>`_
- cloning from one of the many places mentioned below.

.. code-block:: bash
    :linenos:

    $ hg clone https://code.google.com/p/tayra/
    # or
    $ hg clone https://bitbucket.org/prataprc/tayra
    # or 
    $ git clone https://github.com/prataprc/tayra.git

tayra uses mercurial as native repository.

After untarring the source package, or cloning the source repository into
your local machine, install source package by executing,

.. code-block:: bash
    :linenos:

    $ sudo python ./setup.py install
    $ sudo python ./setup.py develop # to install the development version


Using it as python library
--------------------------

.. code-block:: python
    :linenos:

    from pluggdapps.platform import Pluggdapps
    from pluggdapps.plugin   import ISettings

    pa = Pluggdapps.boot( None )    # Start pluggdapps component system.
    compiler = pa.query_plugin( pa, ISettings, 'tayra.ttlcompiler' )
    # Compile
    code = compiler.compilettl( text="<html>\n" )
    # Load
    module = compiler.load( code, context={} )
    # Generate
    html = compiler.generatehtml( module, context={} )


Command line usage
------------------

Make sure that tayra package is installed in your environment (using
pip), in which case command ``tayra`` should be available in your
path. Otherwise create a symbolic link for ``tayra`` to ``tayra/script.py``
script file from tayra package and make sure that the package is in
PYTHONPATH, like,

.. code-block:: bash
    :linenos:

    $ ln -s <site-package>/tayra/script.py $(HOME)/bin/tayra
    $ chmod +x $(HOME)/bin/tayra

    # or,
    $ ln -s <site-package>/tayra/script.py /usr/bin/tayra
    $ chmod +x $(HOME)/bin/tayra

To check whether the package is installed and available in your environment
run the test cases,

.. code-block:: bash
    :linenos:

    # After entering your virtual-environment, if any.
    $ make testall

should pass without any errors. Some useful ``tayra`` commands,

.. code-block:: bash
    :linenos:

    # Translate a template file to corresponding html file.
    $ tayra <template-file>

    # For more help one the command line tool.
    $ tayra --help


Start templating
----------------

It starts with your .ttl file, where ''ttl'' stands for tayra template 
language. Open your favorite editor and we will start writing our first
template. In the long tradition of programming, let us welcome this world,

.. code-block:: ttl
    :linenos:

    ## File name : eg1.ttl

    <html>
      <head>
      <body>
        <p> hello world

Let us now translate this to a html document,

.. code-block:: bash
    :linenos:

    # Assuming that tayra is available in your environment,
    $ tayra eg1.ttl

which looks like,

.. code-block:: html
    :linenos:

    <html>
      <head></head>
      <body>
        <p> hello world</p>
      </body>
    </html>

Now, we will add an id and couple of class attributes to the paragraph tag that
contains the `hello world` text.

.. code-block:: ttl
    :linenos:

    ## File name : eg1.ttl

    <html>
      <head>
      <body>
        <p #welcome .intro.highlight> hello world

- `#welcome` attributes the tag with id-name `welcome`,
- `.intro.highlight` attributes the tag with class-names `intro` and
  `highlight`. And our translated html looks like

.. code-block:: html
    :linenos:

    <html>
      <head></head>
      <body>
        <p id="welcome" class="intro highlight"> hello world</p>
      </body>
    </html>

Tayra sand pit
--------------

This section explains how to setup tayra locally and play with templates.

* tayra depends on `pluggdapps`.
* create a virtual environment.
* enter the virtual environment.
* setup pluggdapps and tayra package.

Above sequence of steps are suggested by following bash script.

.. code-block:: bash
    :linenos:

    # Setting up virtual environment for python 3.x ...
	$ echo
	$ virtualenv --python=python3.2 env
    $ source env/bin/activate   # Enter the virtual environment
	$ pip install pluggdapps tayra

    $ mkdir -p $HOME/dev/tayra-sandpit
    $ cd $HOME/dev/tayra-sandpit

inside the sandpit directory create as many templates (save them as .ttl files)
as you want and compile them to html files,

.. code-block:: bash
    :linenos:

    # Make sure that you are inside the `virtual environment`

    # Translate a template file to corresponding html file.
    $ tayra <template-file>

    # For more help one the command line tool.
    $ tayra --help

to supply context for template files, use the ``-c`` switch in the command
line,
    
.. code-block:: bash
    :linenos:

    $ tayra tables.ttl -c context.py.file

above example used a template file - `tables.ttl` and a context file -
`context.py.file`. Context file should contain a single python object, a
dictionary, providing template context as key, value pairs.

.. code-block:: python
    :linenos:
    
    # context.py.file dictionary of context
    { 'rows' : 10,
      'cols' : 20
    }

and the template file in the above example, `tables.ttl` might look like,

.. code-block:: ttl
    :linenos:

    <html>
      <head>
      <body>
        <table>
          @for i in range(rows) :
            <tr>
              @for j in range(cols) :
                <td>


Integration with other tools
----------------------------

**vim**

TTL plugin is available for vim and downloaded from
`here <http://www.vim.org/scripts/script.php?script_id=4464>`_.

**pygments**

If you are going to use pygments for highlighting source code with HTML and
CSS styles, there is a lexer available `tayra.ext.ttlpygments` for that. The
lexer is not yet part of `pygments` package, so make sure that `tayra` package 
is installed in your environment along with `pygments` package so that the
lexer automatically gets detected.

**pluggdapps web framework**

--TBD--
