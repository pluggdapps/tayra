Release changes
===============

0.2dev
------

* Documentation

0.1dev
------

Initial version of tayra.  A non-exhaustive list of features and functions
available from tayra.

* ``expression substitution``, substitute dynamic content anywhere in your
  document using python expression.
* ``escaping text``, while substituting text, it can be escaped with one or
  more filters. While escape-filters themselves can be added as plugins to tayra.
* ``filter blocks``, process non-template text and substitute the filter block
  with processed text (optional). One such example can be a block of python code
  that need to do some ``view`` related processing. And ofcourse one can 
  create any many types of filter-blocks (plugins !!)
* ``control blocks``, make use of control blocks like ``if-elif-else``, to
  conditionally select portions of templates. And ``for/while`` loop to repeate
  blocks of template text.
* ``functions``, abstract re-usable blocks of templates into functions with its
  own local scope and local-context.
* ``import templates``, import templates from other parts of the source tree
  into the current template's namespace and access their function blocks.
* ``inheritance``, there is a simple yet powerful idea of inheritance, whereby
  templates can have a long chain of inheritance from the base layout. A
  template module in the chain can access any other inheriting or inherited
  templates using the ``parent`` and ``next`` namespace, while ``self``
  namespace provides you the magic of overriding.
* ``how to use``, Can be used via its well-defined API or from command line.
