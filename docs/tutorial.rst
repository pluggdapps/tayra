Tutorial
========

Those who are new to web-app development could be wondering why to template
html ? If need be, why not use one of the many dynamic languages (given the
fact that most of the web-apps are written using one of them) to directly
generate the dynamic parts of a web document ?

- Composing HTML via a programming language, like, python, php, ruby, can be
  more cumbersome and could involve more coding. By the time the developer is
  satisfied with the web page, it would have gone through dozens of trials.
  A templating language is supposed to help developers focus on the look and
  feel (sometimes function) of the document and less on programming it.
- Expression substitution is probably the main feature which allows dynamic
  content to be substituted inside a template.
- Template re-use by abstracting them into function blocks.
- Many popular templating language supports control blocks like, if-else,
  and for/while loops.

What is there in Tayra ?
------------------------

The objective of tayra templating is to create concise, beautiful and highly
re-usable HTML templates for web. Although it is in the beginning
stage, we hope it has succeeded in solving many problems towards that end. To
get you started, here is a non-exhaustive list of features and functions
available from tayra.

``Pluggable tag handlers``,
  Every HTML tag can define its own micro-syntax, and the corresponding HTML
  translation are handled by tag-plugins.

``concise``,
  Inspired by HAML's syntax, tayra uses indentation, shortcuts and wiki
  markups to generate HTML documents.

``expression substitution``,
  Substitute dynamic content anywhere in your document using python
  expression. While substituting text, it can be escaped with one or more 
  filters by suffixing the expression with a pipe operator and a filter-list.
  Escape-filters are implemented as plugins thus allowing developers to define
  their own substitution-filters.

``python-statements``,
  Throw python statements any where inside the template script. When defined
  inside a template-function or interface-method, the statements are confined
  to the scope of the function.

``filter blocks``,
  Intersperse template script with non-template text using filter-blocks.
  Filter blocks are defined and processed by plugins implementing
  ITayraFilterBlock interface. Since filter-blocks take part in multi-pass
  compilation of template scripts it is possible to define filters that are
  tightly integrate with the core language. For instance, to do view-related
  computations, ``:py:`` filter-block can be used.

``control blocks``,
  Make use of control blocks like ``if-elif-else``, to conditionally select
  portions of template and ``for/while`` loop to repeat blocks of template
  script.

``functions``,
  Abstract re-usable blocks of templates into functions with its own local
  scope and local-context. It is possible to define a library of template
  functions and use them else where.

``import templates``,
  Like mentioned above developers can create a library of template functions
  and use them in other template files by importing the library templates.

``inheritance``,
  There is a simple yet powerful idea of inheritance, whereby templates
  can have a long chain of inheritance from the base layout. A template
  module in the chain can refer to inheriting or inherited templates using the 
  ``parent`` and ``next`` namespace, while ``this`` namespace
  provides you the magic of overriding.

``Template plugins``
  Probably, Tayra is the only templating language that enable developers to 
  build and distribute templates as plugins. And those who want to use 
  template-plugins can simply query for them. Now, this one feature will 
  ensure that developers can finally get a plugin architecture without 
  compromising their MVC design pattern.

``Template-module``,
  A template script file is called template-module.

General layout of template script
---------------------------------

A template script contains directives and tags, directives must come in the
beginning of the document, following which are scripts. Template scripts are
made up of, tags, statements, comments, textlines, functions and control
blocks like `if-elif-else`, `for` and `while`.  

Tag definitions are exactly similar to HTML syntax, but there is no need to
specify the end tag ( </...> ) since they are all nested using indentation
syntax.

Expression-substitution can be applied pretty much anywhere in the document
with few exceptions like, inside comments and control statements.

Tag definitions can be abstracted into functions with its own local context.
Tags that are not part of any function or interface-api will be grouped under
the function name **body** which is defined implicitly. It is by making a call
to body(), that the final html is generated and returned, the call is
automatically done by tayra APIs.

.. code-block:: html

    <!-- file name : eg1.ttl -->

    <html>
      <head>
      <body>
        <a title="Go-to google" href="http://google.com"> google

A note on tags and indentation. HTML tags are nested, hence child elements are
forced to use indentation relative to their parent. And because indentation
clearly defines parent and children, there is no need to close HTML tags with
closing-tag syntax, like </html> or </head>.

Let us now translate this to a html document,

.. code-block:: bash

    # Assuming that tayra is available in your environment,
    $ tayra/tyr.py eg1.ttl

above command translates ``eg1.ttl`` into ``eg1.html`` along with an
intermediate file ``eg1.ttl.py``, it is by executing eg1.ttl.py under a
template context we get the final .html output. Identical .ttl files will
generate identical .ttl.py intermediate file, but the final .html output
depends on template context. Now let us look at the html output.

.. code-block:: html

    <!-- file name : eg1.html -->

    <html>
      <head></head>
      <body>
        <a title="Go-to google" href="http://google.com"> google </a>
      </body>
    </html>

In the above snippet notice that .ttl is identical to .html except for closing
tags. And any text indented from the opening-tag is treated its child elements.
Now, we will add couple of attributes to <a> tag,

.. code-block:: html

    <!-- File name : eg1.ttl -->

    <html>
      <head>
      <body>
        <a #welcome .intro.highlight title="Go-to google" 
           href="http://google.com"> google

- ``#welcome`` attributes the tag with id-name ``welcome`` and
- ``.intro.highlight`` attributes the tag with class-names ``intro``
  and ``highlight``. And our translated html looks like

.. code-block:: html

    <!-- File name : eg1.ttl -->

    <html>
      <head></head>
      <body>
        <a id="welcome" class="intro highlight" title="Go-to google" 
           href="http://google.com"> google </a>
      </body>
    </html>

Shortcuts inside tag definitions
--------------------------------

Shotcuts are tokens for tag attributes. Like the example above some attributes
are common to all tags, like ``id`` (tokens prefixed with **#**) and 
``class`` (tokens separated by **.**), have common syntax for
all tags. While other tokens can be specific to individual tags. Plugins
implementing ITayraTag interface is responsible for translating shortcuts to
corresponding tag-attributes. Following is a list of common shortcuts,

- ``id``, an atom prefixed by **hash (#)**.
- ``class``, an atom prefixed by **dot (.)**.
- ``name``, an atom prefixed by **colon (:)**.
- ``style``, any random text enclosed between open-brace and a closing-brace.

Here is an example,

.. code-block:: html

    <!-- File name : eg2.ttl -->

    <p #welcome .intro.highlight> hello world
    <a :anchor-name "http://gnu.org" {color : red}> gnu is not unix

gets translated to,

.. code-block:: html

    <!-- File name : eg2.ttl -->

    <p id="welcome" class="intro highlight"> hello world </p>
    <a name="anchor-name" href="http://gnu.org" style="color: red">
         gnu is not unix </a>

Other than shortcuts, regular html attribute syntax is also supported inside
the tag.

Expression substitution and statements
--------------------------------------

While translating to HTML output, templates can insert dynamic content using
expression substitution. Expressions to be substituted are enclosed within
**${ ... }**, where expressions within curly brackets are nothing but python
expression. Any valid python expression is equally valid here. Note that the
final value emitted by the expression will be converted to string and inserted
in the output html. Other than expressions, a full python statement can be 
used in the template by prefixing them with **@@**. Let us see an example for 
this,

.. code-block:: html

    <!-- File name : eg3.ttl -->

    @@ content = "hello world, %s times"
    @@ rawhtml = "HTML snippet, <pre> hello world </pre>"
    @@ html = "Install couchdb <pre> sudo apt-get install couchdb </pre>"
    <div>
      ${ content % 5 }
      ${ rawhtml | h }
      ${ html | n }

Above example defines 3 variables ``content``, ``rawhtml``, ``html`` and
substitutes their value inside the **div** element. Note that assignments in
python are statements so they are not allowed inside expression-substitution
syntax.

- In the first case, **content** is simple text content and does not require
  any escape filtering to be applied on the result. Output is calculated by
  evaluating the expression and final value is substituted after converting it
  to string.

- Second case is expected to display an example HTML snippet, hence it must be
  escaped to prevent user agents, like browser, from interpreting the HTML
  snippet, instead of displaying them. Suffix parameter **h** following the pipe
  syntax will invoke HTML escaping on the value emitted by expression.

- Third case demonstrates special highlighting for a shell command, as
  pre-formated text, where, unlike the previous example, we must prevent all 
  escape filtering on the final value, which is accomplished by **n** suffix.

The final HTML output will look like,

.. code-block:: html

    <!-- File name : eg3.ttl -->

    <div >
      hello world, 5 times
      HTML snippet, &lt;pre&gt; hello world &lt;/pre&gt;
      Install couchdb using command <pre> sudo apt-get install couchdb </pre>
    </div>

Expression substitution is, more or less, allowed anywhere inside the template
text.

**Escape filtering**

Like mentioned before final value emitted by the python expression will be
converted to a string before substituted in the HTML output. But before
substituting the string, it is possible to apply one or more filters on the
output string. Some filters available along with tayra-package.

``u``,
  If substituted string is a url, quote them using urllib.quote().

``x``,
  If substituted string is XML, apply XML escape encoding.

``h``,
  If substituted string is HTML, apply HTML escape encoding.

``t``,
  Strip (trim) white-spaces before and after the substituted string using.

``n``,
  If specified then the string will substituted as it is with out applying any
  filter logic.

To including python code blocks inside the template script refer to `py
filter block <./filter_blocks.html>`_

Comments
--------

Comments can be of two forms,
- Developer comments that are silently ignored in html output.
- HTML comments that are preserved in html output.

.. code-block:: html

    <!-- File name : eg5.ttl -->

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

gets translated to,

.. code-block:: html

    <!-- File name : eg5.ttl -->

    <!--
    This file is subject to the terms and conditions defined in
    file 'LICENSE', which is part of this source code package.
          Copyright (c) .... ..................
    -->

    <div  >
      <a id="idname" class="cls"  href="http://pluggdapps.com" > hello napster
      </a>
    </div>

Directives
----------

Directives are meta commands that can be specified right at the top of the
template file. There are several directive types defined by tayra,

- ``@doctype`` directive translates to <!DOCTYPE ... > HTML element. It can
  also have other options and parameters provided as simple tokens or
  attribute,value pair.
- ``@body`` defines positional and key-word arguments that can be passed
  to the template module while evaluating them. Note that any template text that
  is not a directive and that is not under a function or method context is
  considered as body of the template and accessible as ``local.body(...)``
- ``@import`` directive to import template libraries.
- ``@inherit`` directive to define template inheritance and complex page
  layouts.
- ``@implement`` directive to define template plugins.

Control blocks
--------------

Control blocks allow to selectively include parts of template text based on
predicates. Other control blocks like `for` and `while` can be used to repeat
a block of template text based on predicates. While a python statements can be
included inside the template text prefixing them with **@@** token, control
blocks are prefixed with **@**, and the block of template script under the
control block must be indented to the right. Let us see an example now,

.. code-block:: html

    @@ bodylocal = 3

    @if bodylocal == 'pass' :
      @@pass
    @elif bodylocal == 2 :
      The program, designed by Odyssey Space Research, will allow crew members
      to conduct several experiments with the phones' cameras, gyroscopes and
      other
    @elif bodylocal == 3 :
      <abbr "World Health Organization"> WHO
      <button #id_ reset disabled makefriend "button value">

    <table>
      @for i in range(100) :
        <tr>
          @@j = 0
          @while j < 4 :
            <td> sample text
            @@j += 1

First line defines a variable called **bodylocal**, which is local to template
function body(). Subsequently, there is a conditional block which checks for
the value of **bodylocal** and evalutes template block for matching predicate.

Finally, a table of 100 rows and 4 columns is generated using an outer 
variable **i** and an inner variable **j**, which gets updated on every
iteration of the outer loop.

TODO : Document loop controls like @@pass, @@break here.

Configuration
-------------

Tayra follows configurations and settings provided by pluggdapps component
architecture. Tayra compiler is implemented as a pluggdapps plugin and hence
can be configured like configuring any other plugin under pluggdapps platform.

**A note on implementation philosopy**

- The templating engine itself is nothing but a specification of syntax
  spun around a collection of plugin framework. And advanced users may find it
  exiting that they can change and extend the behavior (to some extent even the
  syntax) of the template language. Fact is, tayra cannot even parse simple html
  tags by itself.

- All programmable expressions, statements and other language-like concepts
  are nothing but pure python, wrapped inside convenient syntax.

- TTL (Tayra Template Language) files are compiled into python text containing
  stack-machine instructions, interpreted using a stack machine object.

- Almost every aspect of language functionalities (except the programmable
  parts) are extensible via plugins.

- But personally I would love to do tayra-templating just for the way the 
  template code looks - concise and beautiful (thanks to HAML).
