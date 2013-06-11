Command line script
===================

While installing the package using pip, a command line script `tayra`
is automatically created in **bin/** directory. If you are installing it
inside a virtual environment you can expect it in the directory
**<virtual-env-path>/bin/** directory. 

Once the command is available in your environment or via ``PYTHONPATH``,


.. code-block:: text
    :linenos:

    $ tayra --help
    usage: tayra [-h] [-l] [-d] [-s] [-t] [-a ARGS] [-c CONTEXT] [-g DEBUG]
                 [--version]
                 ttlfile

    Pluggdapps command line script

    positional arguments:
      ttlfile     Input template file containing tayra script

    optional arguments:
      -h, --help  show this help message and exit
      -l          Do lexical analysis of input file.
      -d          Dump translation
      -s          Show AST parse tree
      -t          Execute test cases.
      -a ARGS     Argument to template
      -c CONTEXT  Context to template
      -g DEBUG    Debug level for PLY argparser
      --version   Version information of the package


Few command line use cases,

.. code-block:: bash
    :linenos:

    # Translate a template file to corresponding html file.
    $ tayra <template-file>

    # Display the AST tree for template file.
    $ tayra -s <template-file>

    # List out put of lexical analyser for template file.
    $ tayra -l <template-file>
