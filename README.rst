Tayra template
==============

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
==========

* `README <http://tayra.pluggdapps.com/dev/readme>`_
* `CHANGELOG <http://tayra.pluggdapps.com/dev/changelog>`_
* `Track tayra development `google-code <http://code.google.com/p/tayra/>`_
* If you have any queries, suggestions
  `discuss with us <http://groups.google.com/group/pluggdapps>`_

Documentation
=============

* `Tayra reference <http://tayra.pluggdapps.com/doc/markup>`_
