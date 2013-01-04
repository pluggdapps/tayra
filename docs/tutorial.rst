{{ Toc( float='right' ) }}

It starts with your .ttl file, where ''ttl'' stands for tayra template language.
Open your favorite editor and we will start writing our first template.
Our first template is going to be a welcome message to this world.

h3. HTML and indentation

{{{ Code ttl

<!-- file name : eg1.ttl -->

<html>
  <head>
  <body>
    <p> hello world
}}}

A note on tags and indentation. HTML tags are nested, hence child elements are
enforced to use 2-space indentation relative to their parent, and there is no
need to close HTML tags with closing-tag syntax, like </html> or </head>.

Let us now translate this to a html document,

{{{ Code bash

# Assuming that tayra is available in your environment,
$ tayra/tyr.py eg1.ttl

}}}

above command translates //eg1.ttl// into //eg1.html// along with an
intermediate file //eg1.ttl.py//, it is by executing eg1.ttl.py under a
template context we get the final .html output. Identical .ttl files will
generate identical .ttl.py intermediate file, but the final .html output
depends on template context. Now let us look at html output.

{{{ Code html
# { 'background-color' : '#FFF' }

<!-- file name : eg1.html -->

<html>
  <head></head>
  <body>
    <p> hello world</p>
  </body>
</html>
}}}

Now, we will add couple of attributes to paragraph tag that contains the
//hello world// text.

{{{ Code ttl

<!-- File name : eg1.ttl -->

<html>
  <head>
  <body>
    <p#welcome.intro.highlight> hello world
}}}

# ''#welcome'' attributes the tag with id-name //welcome// and
# ''.intro.highlight'' attributes the tag with class-names //intro// and
  //highlight//. And our translated html looks like

{{{ Code html
# { 'background-color' : '#FFF' }

<!-- File name : eg1.ttl -->

<html>
  <head></head>
  <body>
    <p id="welcome" class="intro highlight"> hello world</p>
  </body>
</html>
}}}

h3. Standard specifiers

Specifiers are tokens applied to tagnames. White-space separated atoms and
strings immediately following the tagname are also considered as specifier
tokens. While any number of specifier tokens can be defined by tag handlers
responsible for translating a given tag element, there are few that are standard
and common to all tag elements. They are,
# ''id'', an atom prefixed by ''hash (#)''.
# ''class'', an atom prefixed by ''dot (.)''.
# ''name'', an atom prefixed by ''colon (:)''.

As the name suggests the standard specifier tokens are translated to their
respective tag attributes. For example the following snippet of template,

{{{ Code ttl

<!-- File name : eg2.ttl -->

<p#welcome.intro.highlight> hello world
<a:anchor-name "http://gnu.org"> gnu is not unix
}}}

gets translated to,

{{{ Code ttl
# { 'background-color' : '#FFF' }

<!-- File name : eg2.ttl -->

<p id="welcome" class="intro highlight"> hello world </p>
<a name="anchor-name" href="http://gnu.org"> gnu is not unix </a>
}}}


h3. Expression substitution

While translating to HTML output, templates can insert dynamic content using
expression substitution. Expressions to be substituted are enclosed within
''${ ... }'', where, expressions within curly brackets are nothing but python
expression. Any valid python expression is equally valid here. Note that the
final value emitted by the expression will be converted to string and replace
them as it is inside the output html.

{{{ Code ttl

<!-- File name : eg3.ttl -->

@@ content = "hello world, %s times"
@@ rawhtml = "HTML snippet, <pre> hello world </pre>"
@@ html = "Install couchdb using command <pre> sudo apt-get install couchdb </pre>"
<div>
  ${ content % 5 }
  ${ rawhtml | h }
  ${ html | n }
}}}

Above example defines 3 variables //content//, //rawhtml//, //html// and
substitutes their value inside the //div// element.
# In the first case, //content// is simple text content and does not require
  any escape filtering to be applied on the result. Output is calculated by
  evaluating the expression and final value is substituted after converting it
  to string.
# Second case is expected to display an example HTML snippet, hence it must be
  escaped to prevent user agents, like browser, from interpreting the HTML
  snippet, instead of displaying them. Suffix parameter ''h'' following the pipe
  syntax will invoke HTML escaping on the value emitted by expression.
# Third case demonstrates special highlighting for a shell command, as
  pre-formated text, where, unlike the previous one must prevent all escape
  filtering on the final value, which is accomplished by ''n'' suffix.

{{{ Code html
# { 'background-color' : '#FFF' }

<!-- File name : eg3.ttl -->

<div >
  hello world, 5 times
  HTML snippet, &lt;pre&gt; hello world &lt;/pre&gt;
  Install couchdb using command <pre> sudo apt-get install couchdb </pre>
</div>
}}}

Expression substitution is, more or less, allowed anywhere inside the template
text.

h3. Inline styles and attributes

Like //id// and //class// attributes, //style// attribute is also often used
attribute on html elements. Using style attribute, as opposed to CSS styling
on a html element is called inline styling. Tayra defines a special syntax to
do inline-styling, '' { ... } '', where text within curly braces are
interpreted as style attributes.

{{{ Code ttl
<!-- File name : eg4.ttl -->

<div { margin : ${marginsize}px; color : blue; } > hello world
}}}

simple gets translated to,

{{{ Code ttl
<!-- File name : eg4.ttl -->

<div style="margin : 10px; color : blue;"> hello world </div>
}}}

where, //marginsize// evaluates to value 10.

h3. Directives

Directives are meta commands that can be specified right at the top of the
template file. There are several directive types defined by tayra,
# ''Document type'' directive translates to <!DOCTYPE ... > HTML element.
# ''Body directive'' defines positional and key-word arguments that can be passed
  to the template file while evaluating them.
# ''Import directive'' to import template libraries.
# ''Inherit directive'' to define template inheritance and complex page
  layouts.
# ''Implement directive'' to define template plugins
# ''use directive'' to query for template plugins and import them into template
  namespace.

To know exact details on how to use each of these directive, check out the 
[[ ./reference#Directives | directive-section ]] of
reference page.

h3. Comments

Comments can be of two forms,
# Developer comments that are silently ignored in html output.
# HTML comments that are translated as it is in html output.

{{{ Code ttl

<!-- File name : eg5.ttl -->

<!--
This file is subject to the terms and conditions defined in
file 'LICENSE', which is part of this source code package.
      Copyright (c) .... ..................
-->

@function func( name ) :
  ## This comment will be silently ignored.
  <div {} >
    <a#${'idname'}.${'cls'} "http://pluggdapps.com"> hello ${name}

${ func( 'name' ) }
}}}

Translated to,

{{{ Code html
# { 'background-color' : '#FFF' }

<!-- File name : eg5.ttl -->

<!--
This file is subject to the terms and conditions defined in
file 'LICENSE', which is part of this source code package.
      Copyright (c) .... ..................
-->

<div  >
  <a id="idname" class="cls"  href="http://pluggdapps.com" > hello name</a>
</div>
}}}

h3. Statements and control blocks

Statements are python statements and control blocks map to python if-elif-else
blocks, for blocks and while blocks. A statement starts with ''@@'' and
entirely contained in a single line, multi-line statement must be escaped for
newlines and control blocks start with ''@'' and ends with a colon '':''.
Following example will give an idea on statements and control blocks in tayra
templates,

{{{ Code ttl

@@ bodylocal = 3

@if bodylocal == 'pass' :
  @@pass
@elif bodylocal == 2 :
  The program, designed by Odyssey Space Research, will allow crew members to
  conduct several experiments with the phones' cameras, gyroscopes and other
@elif bodylocal == 3 :
  <abbr "World Health Organization"> WHO
  <button#id_ reset disabled makefriend "button value"/>

<table>
  @for i in range(100):
    <tr>
      @@j = 0
      @while j < 4 :
        <td> sample text
        @@j += 1
}}}

First line defines a variable called //bodylocal//, which is local to template
body(). Subsequently, there is a conditional block which checks for the value of
//bodylocal// and evalutes template block for matching predicate.  Finally, a
table of 100 rows and 4 columns is generated using an outer variable //i// and
an inner variable //j//, which gets initialized for every iteration of the
outer loop.

h3. Advanced Templating

''{s} To learn more on advanced templating you can check out the following sections
in the reference document''

# [[ ./reference#Functions | template functions ]]
# [[ ./reference#Filter%20blocks | filter blocks ]]
# [[ ./reference#Template%20plugins | template plugins ]]

-----

{{{ Nested 
# { 'font-size' : 'small', 'color' : 'gray' }
Document edited using Vim <br>
/* vim: set filetype=etx : */
}}}
