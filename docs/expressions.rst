Expression substitution and escape filtering
============================================

Expressions can be substituted inside a template file using **${...}** syntax.
Additionally, evaluated output can be passed to filters using **${... |
<filters> }** the pipe token, where `filters` is comma separated value of
filters to be applied in specified order.

.. code-block:: ttl

    <li #crumbs>
      <a .crumbname "${crumbsurl or '' | u }"> ${crumbsname}
      <ul :menu {color : blue}>

Behind the scenes, expression substitution is handled by plugins implementing
implementing :class:`tayra.interfaces.ITayraExpression` interface. While
coding an expression inside a template script it is possible to target the
expression for specific plugin. If an expression is coded without a target
plugin then default plugin will be picked based on the configuration parameter
``TTLCompiler['expression.default']``.

py
--

Evaluate the text as python expression, convert the result to string, pass
them to supplied filter (if any) and then substitute the final output in the
final html output.

.. code-block:: ttl

    @@l = [1,2,3]

    ## Evaluating and substituting python expression
    <div> ${-py l}

Filters supported by this expression are,

u,
  Assume expression result as url and quote using urllib.parse.quote().

x,
  Assume text as XML, and apply escape encoding.

h,
  Assume text as HTML and apply html.escape( quote=True ).

t,
  Strip whitespaces before and after text using strip().

evalpy
------

Evaluate the text as python expression and ignore the result. In the final
HTMl output the expression text will be replace with an empty string.

.. code-block:: ttl

    @@l = [1,2,3]

    ## Evaluating with expression extension
    ${-evalpy l.append(10)}
    ${-evalpy l.pop(0)}
    <div> ${l}

This plugin does not support any filter methods.
