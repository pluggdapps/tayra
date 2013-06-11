Tayra is a full-featured abstract markup language to template web documents.
It is primarily inspired from mako-templates_ and HAML_ (especially the
indentation based markup definitions). Only templating language that allow
developers to build and distribute their templates as plugins, not to mention
the fact that tayra's implementation itself is heavily based on plugins.

Example,

.. code-block:: text

    @doctype html

    <html>
      <head>
        <style text/css>
          .italics { font-style : italics; }

      <body>
        <div>
          <p> <span .italics> hello world
          <p> counting to hundred, ${[ x for x in range(1, 100) ]}

            
Features
--------

- concise and neat syntax.
- based on pluggdapps_ component system.
- leverages on `pluggdapps' configuration system`.
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
- expression substitution can be extended by plugins to interpret different
  types of expression.
- unique ability to create template plugins, distribute them as separate
  package.
- easy to debug. when used with `pluggdapps'` ``CatchAndDebug`` plugin,
  exception tracebacks are tweaked to directly point to faulting line in the
  template.
- `pluggable` tag handlers for custom tag elements.
- compiles down to optimal python code and optionally memcached. Also possible
  to persist the intermediate python code to avoid re-compilation in case of
  server restart.
- works with python 3.x.
- has full unicode support.
- lexer for generating syntax-highlighted web documents using Pygments.
- vim-plugin_ for template scripts.
- **License:** `GPLv3 license`_.
- **Requires:** Linux, Python-3.x, Pluggdapps, PLY.

  - If `beautify_html` settings is enabled for ``tayra.ttlcompiler`` plugin,
    the beautifulsoup4_ needs to be installed.

- **Status:** Core design stable. Not expected to change.

Related links
-------------

* `package documentation`_.
* changelog_.
* todo_.
* mailing-list_.

Tayra templating language is under development - you can hack the code,
contribute back with `github <https://github.com/prataprc/tayra>`_.
Note that the orginal repository is maintained with mercurial and uses hg-git
plugin to publish it on github.

.. _pluggdapps: http://pythonhosted.org/pluggdapps
.. _mako-templates: http://www.makotemplates.org
.. _HAML: http://haml-lang.com
.. _vim-plugin: http://www.vim.org/scripts/script.php?script_id=4464
.. _GPLv3 license:  http://www.gnu.org/licenses/
.. _beautifulsoup4: https://pypi.python.org/pypi/beautifulsoup4

.. _package documentation: http://pythonhosted.org/tayra
.. _changelog: http://pythonhosted.org/tayra/CHANGELOG.html
.. _todo: http://pythonhosted.org/tayra/TODO.html
.. _mailing-list: http://groups.google.com/group/pluggdapps
