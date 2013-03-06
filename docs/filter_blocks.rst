Filter blocks
=============

Filter blocks provide a way to include non-template text inside the template
script. Unlike the template syntax which follow strict indentation rules,
text inside a filter block are completely exempted from
Tayra-Template-Language syntax.

A filter block should be opened in a new-line prefixed by any number of
white-spaces, and this opening newline must always be confirmant to the
template's indentation rules. Any number of text-lines can follow the
opening-line and the text-lines can have their own syntax dictated by
corresponding filter-blocks.

A filter block is closed by a newline prefixed by any number of white-spaces
similar to the opening line.

Here is an example,

.. code-block:: ttl

    :py:
      a = 'empty'
      def insideroot_butglobal():
        return '<div> insideroot_butglobal </div>'
    :py:

    :py:
      b = '<div> insideroot_insidebody </div>'
    :py:

    ${ a } ${ insideroot_butglobal() }
    ${ b }

    @def func() :
      <div> hello world

The above example demonstrates a filter-block called **py** implemented by an
:class:`tayra.interfaces.ITayraFilterBlock` plugin called **py**. Filter
blocks are handled by plugins and the correct plugin to handle the filter
block is choosen based on the opening line's filter-block name.

Plugins handling filter-blocks, directly take part in compilation phases of the
template script and can even generate stack machine instructions
directly. We believe this open ended design will lead us to more interesting
language features, features though implemented / extended using plugin can be
tightly integrated with the language.

py filter block
---------------

The filter block allows developers to include blocks of python code inside the
template script. Note that the syntax of text inside this filter block should
follow python programming syntax.

Code block defined inside a template-function or template-method will be local
to the scope of the function or method.

Globally defined code blocks will be interpreted in the global scope and the
side effects created by the code block will be available to all function and
methods defined in the template script.

To learn how to extend filter blocks with a plugin, refer to
ITayraFilterBlock section in this `article <./develop.html>`_.
