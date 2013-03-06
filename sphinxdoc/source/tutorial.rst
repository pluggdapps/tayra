Tutorial
========

This article provides an overview of everything that you, as a template
designer, can do with tayra. If you are just starting with tayra for the first
time you may want to go through the `getting started <./gettingstarted.html>`_
page first. If you are a developer looking forward to extend tayra language
please refer to `development <./develop.html>`_ page. For more involved 
features in tayra refer to articles,

  * `template directive <./directives.html>`_
  * `filter blocks <./filter_blocks.html>`_
  * `page layout using template inheritance <./template_layout.html>`_
  * `implementing and distributing template plugins <./template_plugins.html>`_

You can go through them once you are comfortable with basic features explained
here.

What is there in Tayra ?
------------------------

The objective of tayra templating is to create concise, beautiful and highly
re-usable HTML templates for web. Although it is in the beginning
stage, we hope it has succeeded in solving many problems towards that end.
Here is a basic list of features and functions available from tayra,

``Pluggable tag handlers``,
  Every HTML tag can define its own micro-syntax, and corresponding HTML
  translations are handled by tag-plugins.

``concise``,
  Inspired by HAML's syntax, tayra uses indentation, shortcuts and wiki
  markups to generate HTML documents.

``expression substitution``,
  Substitute dynamic content anywhere in your document using python
  expression. While substituting text, it can be escaped with one or more 
  filters by suffixing the expression with a pipe operator and a filter-list.
  Expression substitution is implemented via plugins and each expression in
  the template script can be targeted to specific plugin.

``python-statements``,
  Throw python statements any where inside the template script. When defined
  inside a template-function or interface-method, the statements are confined
  to the scope of the function.

``control blocks``,
  Make use of control blocks like ``if-elif-else``, to conditionally select
  portions of template and ``for/while`` loop to repeat blocks of template
  script.

``functions``,
  Abstract re-usable blocks of templates into functions with its own local
  scope and local-context. It is possible to define a library of template
  functions and use them else where.

``filter blocks``,
  Intersperse template script with non-template text using filter-blocks.
  Filter blocks are defined and processed by plugins implementing
  :class:`tayra.interfaces.ITayraFilterBlock` interface. Since filter-blocks
  take part in multi-pass compilation of template scripts it is possible to
  define filters that are tightly integrate with the core language.

``inheritance``,
  There is a simple yet powerful idea of inheritance, whereby templates
  can have a long chain of inheritance from the base layout. A template
  module in the chain can refer to inheriting or inherited templates using the 
  ``parent`` and ``next`` namespace, while ``this`` namespace provide the
  magic of overriding.

``Template plugins``
  Probably, Tayra is the only templating language that enable developers to 
  build and distribute templates as plugins. And those who want to use 
  template-plugins can simply query for them.

``Configuration``,
  Tayra uses pluggdapps component architecture and plugins in tayra leverages
  on pluggdapps configuration system.

General layout of template script
---------------------------------

For those who are starting with web-templating,

* Start writing your template just like your HTML page. Except that you don't
  have to supply the closing tag. ``</...>`` is not required.
* Always remember the indentation. Child elements are always indented by 2
  spaces.

That is all is required to write your first template.

Template script contain directives and scriptlines, directives must come
in the beginning of the document, followed by template script. Template
scripts are made up of tags, statements, comments, textlines, functions,
control-blocks like `if-elif-else`, `for` `while` and filter-blocks.

Expression-substitution can be applied pretty much anywhere in the document
with few exceptions like, inside comments and control statements.

Tag definitions can be abstracted into functions with its own local context.
Tags that are not part of any function or interface-api will be grouped under
the function name **body**, defined implicitly. It is by making a call
to body(), that the final html is generated and returned, the call is
automatically done by tayra APIs.

.. code-block:: ttl

    @doctype html

    <html lang="en">
    <head>
      <title> My Webpage

    <body>
      <ul #navigation>
        @for item in navigation :
          <li> <a "${ item.href }"> ${ item.caption }

      <h1> My Webpage
      ${ a_variable }

Shortcuts inside tag definitions
--------------------------------

Shotcuts are tokens for tag attributes. Like the example above some attributes
are common to all tags, like, ``id`` (tokens prefixed with **#**) and 
``class`` (tokens separated by **.**) shortcuts have common syntax for
all tags. While other tokens can be specific to individual tags. Plugins
implementing :class:`tayra.interfaces.ITayraTag` interface is responsible for
translating shortcuts to corresponding tag-attributes. Following is a list of
common shortcuts,

- ``id``, an atom prefixed by **hash (#)**.
- ``class``, an atom prefixed by **dot (.)**. More than one class-names can be
  supplied by separating them by **dot (.)**.
- ``name``, an atom prefixed by **colon (:)**.
- ``style``, any random text enclosed between open-brace and a closing-brace.

Here is an example,

.. code-block:: ttl

    <!-- File name : eg2.ttl -->

    <p #welcome .intro.highlight> hello world
    <a :anchor-name "http://gnu.org" {color : red}> gnu is not unix

Other than shortcuts, regular html attribute syntax is also supported inside
the tag.

Expression substitution and statements
--------------------------------------

Expression substitution is, more or less, allowed anywhere inside the template
script. While translating to HTML output, templates can insert dynamic content
using expression substitution. Expressions are enclosed within **${ ... }**,
where text within curly braces are interpreted as python expression.
Expression will be evaluated, converted to string, piped through filters
(if supplied) and the result is substituted in the final html. Any valid
python expression is equally valid here. Other than expressions, a full
python statement, in a single line, can be used in the template by prefixing
them with **@@**. Let us see an example for this,

Escape filtering

  Like mentioned before final value emitted by the python expression will be
  converted to string before substituting them in HTML output. But before
  substituting the string, it is possible to apply one or more filters on the
  output string. Filters are applied in the specified order.


.. code-block:: ttl

    <!-- File name : eg3.ttl -->

    @@ content = "hello world, %s times"
    @@ rawhtml = "HTML snippet, <pre> hello world </pre>"
    @@ html = "Install couchdb <pre> sudo apt-get install couchdb </pre>"
    <div>
      ${ content % 5 }
      ${ rawhtml | h }
      ${ html | n }

Above example defines 3 variables ``content``, ``rawhtml``, ``html`` and
substitutes their value inside the **div** element. It is also possible to
substitute variables that come from web application context. Note that 
assignments in python are statements, so they are not allowed inside 
expression-substitution syntax.

- In the first case, **content** is simple text and does not require
  any escape filtering to be applied on the result. Output is calculated by
  evaluating the expression and final value is substituted after converting it
  to string.

- Second case is expected to display an example HTML snippet, hence it must be
  escaped to prevent user agents, like browser, from interpreting the HTML
  snippet instead of displaying them. Suffix parameter **h** following the
  pipe syntax will invoke HTML escaping on the value emitted by expression.

- Third case demonstrates special highlighting for a shell command as
  pre-formated text, where, unlike the previous example, we must prevent all 
  escape filtering on the final value, which is accomplished by **n** suffix.

The above example when translted to html, will look like,

.. code-block:: html

    <div >
      hello world, 5 times
      HTML snippet, &lt;pre&gt; hello world &lt;/pre&gt;
      Install couchdb using command <pre> sudo apt-get install couchdb </pre>
    </div>

Expressions are handled by plugins. Available list of expression plugins
`expressions and filtering <./expressions.html>`_.

Comments
--------

Comments can be of two forms,

- Developer comments that are silently ignored in html output.
- HTML comments that are preserved in html output.

.. code-block:: ttl

    <!--
    This file is subject to the terms and conditions defined in
    file 'LICENSE', which is part of this source code package.
          Copyright (c) .... ..................
    -->

    @def func( name ) :
      ## This comment will be silently ignored.
      <div {} >
        <a #${'idname'} .${'cls'} "http://pluggdapps.com"> hello ${name}

    ${ func( 'napster' ) }

In the above example the copyright notice will be preserved in the final HTML
output while developer comments starting with `##` will be ignored.

Control blocks
--------------

Control blocks allow to selectively include parts of template script based on
predicates. Other control blocks like `for` and `while` can be used to repeat
a block of template script based on predicates. While a python statements can be
included inside the template script by prefixing them with **@@** token,
control blocks are prefixed with **@**, and the block of template script under
the control block must be `indented to the right`. Let us see an example now,

.. code-block:: ttl

    @if bodylocal == 'pass' :
      @@pass

    @elif bodylocal == 2 :
      The program, designed by Odyssey Space Research, will allow crew members
      to conduct several experiments with the phones' cameras, gyroscopes and
      other

    @else :
      <abbr "World Health Organization"> WHO
      <button #id_ reset disabled makefriend "button value">

    <table>
      @for i in range(100) :
        <tr>
          @@j = 0
          @while j < 4 :
            <td> sample text
            @@j += 1

Above example demonstrates the use of control blocks. It uses a variable called
**bodylocal** availabe in template's context to selectively pick script blocks
based on a predicate. 

Finally, a table of 100 rows and 4 columns is generated using an outer 
variable `i` and an inner variable `j`, which gets updated on every
iteration of the outer loop.

**loop controls**

It is possible to use break and continue in loops. When break is reached,
the loop is terminated; if continue is reached, the processing is stopped and
continues with the next iteration. The following is an example,

.. code-block:: ttl

    @for user in users :
      @if user.startswith('admin-') :
        @@continue
      ...

    ## Likewise a loop that stops processing after the 10th iteration:

    @@i = 0
    @while users :
      @if i >= 10 :
        @@break
      ...

Functions
---------

Template functions are ways to abstract and reuse template script. Although the
syntax and signature of a template-function follows python rules, they do
not abstract python code, instead they abstract template script intended to
right by two spaces from function signature.

Functions can be called, with positional arguments and key-word arguments, and
return html text, which shall be substituted in the caller's context using
exrpression-substitution.

Functions are always called inside expression substitution syntax **${ ... }**.
Functions also provide a local context for template blocks that are
encapsulated under it. Functions can be nested and follows the same scoping
rules defined by python functions. A function's definition starts with a 
newline followed by one or more white-space and continues with the function
signature.

Function signature starts with **@def** keyword and ends with a **colon (:)**.

.. code-block:: ttl

    @def justtext() : 
      Google will join its biggest mobile rival, Apple, on the space trip as
      well.  Apple's iPhone 4 will join a crew running an app, called
      "SpaceLab for iOS."

    @def involved( z ):
      <abbr "World Health Organization"> ${z}
      @def nestedfunc() :
        <b> this is nested function
        @def nestednestedfunc() :
          <em> this is nested nested function
        ${ nestednestedfunc() }
      <button #id_ reset disabled makefriend "button value">
      ${ nestedfunc() }

    ${ justtext() }
    ${ involved( 'WHO' ) }

When functions are combined with template modules, it will provide a powerful
way to abstract and organise your view-templates.

Directives
----------

Directives are meta commands specified right at the top of the template script.
Here is a shotlist of directives defined by tayra,

- ``@doctype`` directive translates to `<!DOCTYPE ... >` HTML element. It can
  also have other options and parameters provided as simple tokens or
  attribute,value pair.

- ``@body`` defines positional and key-word arguments that can be passed
  to the template module while evaluating them. Note that a block of template
  script that is not a directive and that is not under a function or 
  interface-method is considered as body of the template and accessible as
  ``local.body(...)``

- ``@import`` directive to import template libraries.

- ``@inherit`` directive to define template inheritance and complex page
  layouts.

- ``@implement`` directive to define template plugins.

For detailed explanations refer to `template directives <./directives.html>`_.

Template libraries
------------------

Developers can abstract and organise their templates as a library or a
tool-kit. Since every template script is compiled and interpreted as a python
module, importing them is similar to importing a python module using
**@import** directive.

The import directive specifies which template file to be imported and the 
name to access the template module. For example,

.. code-block:: html

    @import etsite:templates/_base/elements.ttl as e ;
    @import os, sys;

    @def body_leftpane() :
      ${e.leftpane( menupane )}

Here `elements.ttl` is imported as a template module ``e``, which can be
referred in the template script. Further down, you can notice that library
function ``leftpane(...)`` is called from the imported template module.

Template context
----------------

Every template script is compiled into a template module and executed as
python program to generate the final html output. While loading and executing
the template modules it is possible to supply a dictionary of context, like
explained in this `section <./gettingstarted.html#using-it-as-python-library>`_.
In addition to that some standard set of objects are automatically made
available by the `runtime engine <./modules/runtime.html>`_. One such object
is `h <./h.html>`_ helper container object that supplies wide variety of
library functions that can be useful while scripting your templates. 

Configuration
-------------

Tayra follows configurations and settings provided by pluggdapps component
architecture. Tayra compiler is implemented as a pluggdapps plugin and hence
can be configured like configuring any other plugin under pluggdapps platform.

**A note on implementation philosopy**

- The templating engine itself is nothing but a specification of syntax
  spun around a collection of plugin framework. And advanced users may find it
  exiting that they can change and extend the behavior (to some extent even the
  syntax) of the template language. Fact is, tayra cannot even parse simple
  html
  tags by itself.

- All programmable expressions, statements and other language-like concepts
  are nothing but pure python, wrapped inside convenient syntax.

- TTL (Tayra Template Language) files are compiled into python text containing
  stack-machine instructions, interpreted using a stack machine object.

- Almost every aspect of language functionalities (except the programmable
  parts) are extensible via plugins.

- But personally I would love to do tayra-templating just for the way the 
  template code looks - concise and beautiful (thanks to HAML).
