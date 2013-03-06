Tayra is a full-featured abstract markup language to template web documents.
It is primarily inspired from 
`mako-templates <http://www.makotemplates.org/>`_ and
`HAML <http://haml-lang.com/>`_ (especially the indentation based
markup definitions). Probably it is the only templating language that allow
developers to build and distribute their templates as plugins, not to mention
the fact that tayra's implementation itself is heavily based on plugins.

Example,

.. code-block:: ttl

    @doctype html

    <html>
      <head>

      <body>
        <div>
          <p> <span .italics> hello world
          <p> counting to hundred, ${[ x for x in range(1, 100) ]}

            
Features
--------

- concise and beautiful syntax.
- based on pluggdapps component architecture.
- leverages on pluggdapps' configuration system.
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
- easy to debug. when used with pluggdapps' ``CatchAndDebug`` plugin, exception
  tracebacks are tweaked to directly point to faulting line in the
  template.
- pluggable tag handlers for custom tag elements.
- compiles down to optimal python code and optionally memcached. Also possible
  to persist the intermediate python code to avoid re-compilation in case of
  server restart.
- works with python 3.x.
- has full unicode support.
- lexer for generating syntax-highlighted web documents using Pygments.
- vim plugin for template scripts.
- **License:** `GPLv3 license <http://www.gnu.org/licenses/>`.
- **Requires:** Linux, Python-3.x, Pluggdapps, PLY.
- **Status:** Core design stable. Not expected to change.


.. include:: contents.rst.inc

If you can't find the information you're looking for, have a look at the
index or try to find it using the search function:

* :ref:`genindex`
* :ref:`search`
