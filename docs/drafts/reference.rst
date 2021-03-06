{{ Toc( float='right' ) }}

The following is a non-exhaustive narrative reference of tayra template
language. 

The following are key ideas behind tayra templating language.
# Tayra is a text processing language, more specifically it is suited for
  HTML or XML templating.
# All programmable expressions, statements and other language-like concepts
  are nothing but pure python, wrapped with convenient syntax.
# TTL (Tayra Template Language) files are compiled into python text containing
  stack-machine instructions, interpreted using a stack machine object.
# Language syntax is just a glue logic to access a plugin framework that does
  most of the heavy lifting. There are atleast three interface specifications
  for plugins to implement their logic.
# Almost every aspect of language functionalities (except the programmable
  parts) are extensible via plugins.
# A key strength in tayra templates is that it is possible to create template
  blocks as plugins and distribute them as packages. Tayra package comes with
  initialization routines that can be used to pre-load the template plugins,
  using setup-tools. If this initialization is not done
  explicitly, it will be automatically done when compiling a .ttl file. Once
  template-plugins are loaded, they can be queried and consumed to generate
  final HTML.

First let us define couple of terms that will keep recurring through out the
text,

: indentation ::
  HTML is all about nested tags and text content. A HTML document is naturally
  organised as a tree with a root-node. Hence tayra took its inspiration
  from HAML (rails community) and imposes a strict indentation between
  parent tag and its children. Each indentation level takes up 2 blank-space,
  thus, for a child tag that is nested 3 levels deep should have 6
  blank-spaces. The indentation syntax is followed very strictly unless
  otherwise explicitly mentioned.
: tag ::
  A tag in a .ttl text has an exact correspondence to HTML tags. It starts with
  ''<'', a //tagname// followed by a sequence of //attributes//
  (name,value pairs) finally ends with ''>''. Other than this, it can also
  contain, //expressions//, //specifiers// and //styles// within its
  angle-brackets. Since indentation is enforced, there is no need to close the
  tag with ''</...>'' markup, like in HTML.
: expressions ::
  A key requirement in dynamically generating HTML page, is to be able to
  substitute variable content inside the template. In tayra, like many other
  templating language, substitution is performed using [<PRE ${ ... } >]
  syntax. Text between //${// and //}// will be interpreted as python
  expression, and value emitted by the expression shall be string-ified.
: specifiers ::
  Specifiers are tokens (more specifically atoms and strings) that can be
  specified inside a tag element. There are standard specifiers that are common
  to all ttl tag elements. Also, corresponding tag-handlers can define their
  own specifier syntax.
: style ::
  //style// attribute is often used attribute in HTML (there are guidelines
  suggesting to separate styling into CSS file, nevertheless!), hence a
  special syntax is provided off-the-shelf, [<PRE { ... }>]. Text between
  curly brace will be interpreted as the element's style.
: attributes ::
  Tag attributes are same as attributes defined by HTML. They will be translated
  as it is.
: tag-handlers ::
  Tag handlers are plugins that handle ttl tag elements. If no tag-handlers are
  registered for the //tagname//, a default handler will be used to translate
  the tag element in safest possible way.
: directives ::
  Directives are meta constructs that provide more information on how to
  interpret rest of the TTL text. Specifying document-type, importing other ttl
  files, inheritance and plugin definition are possible through directives.
: statements ::
  Statements are programmable logic that spans an entire line and typically
  starts with ''@'' or ''@@''. If you are starting a new line with ''@'' that
  is not a statement, it must be escaped using backslash.
: comment ::
  Two types of commenting are allowed, one that will be translated along with
  ttl text and the other that will be ignored silently.
: filter-blocks ::
  Filter blocks are blocks of text that does not follow indentation rules and
  have their own parsing logic.
: global context ::
  Global context is the context passed by the caller while translating .ttl
  documents into HTML text. Since tayra embeds python programming within the
  template document, it is possible to create side-effects to global context
  using globals() or using //pycode//, with global token, filter-block.
: local context ::
  Functions and Interfaces can create a local context of its own during
  execution. Even the root level template text that is not part of any function
  or interface will be processed under an implicitly defined function
  //body()//.
: .ttl ::
  File extensions containing tayra templates. These templates can be compiled
  into an intermediate //.py// file which can then be loaded and executed
  (with context) to generate the final .html file.

Before continuing we will see how a snippet of ttl text looks like,

{{{ Code ttl
<div> Brief incomplete and mostly wrong history of programming languages
  looted from,
  <a "http://james-iry.blogspot.com/2009/05/brief-incomplete-and-mostly-wrong.html">
    here.
  <ul>
    <li> 1972 - Dennis Ritchie invents a powerful gun that shoots both forward
      and backward simultaneously. Not satisfied with the number of deaths and
      permanent maimings from that invention he invents C and Unix.
    <li>
      1991 - Dutch programmer Guido van Rossum travels to Argentina for a 
      mysterious operation. He returns with a large cranial scar, invents Python,
      is declared Dictator for Life by legions of followers, and announces to
      the world that "There Is Only One Way to Do It." Poland becomes nervous.
}}}


h3. Configuration

Many parts of tayra template engine is configurable by providing a
dictionary of //key-value// pairs. Configuration dictionary provided by
caller program will override package default configuration. Final configuration
will be remembered by Compiler() object as ''ttlconfig''. //ttlconfig//
is chained all the way from Compiler() object to every object that are part of
the template instance, including referred templates via ''{y}@include'' and 
''{y} @inherit'' directives.

A template instance will have //Compiler()// object, //StachMachine()// object,
//InstrGen()// object, while compiling and executing a template. Complete
[[ ./config | list of configuration ]] parameters. Developers can take a look at
// tayra/\__init\__.py // module, where the default set of configuration
parameters are defined.

h3. Overview

Much of this documentation is about tayra templating language on how to
write template files (its syntax and semantics). A brief introduction to its
internals and developer guidelines are provided in the last few sections.

Tayra template document contains directives and tags, directives can be used
in the beginning of the document, following which are tags. The beginning
of tag definition is exactly similar to HTML syntax, but there is no need to
specify the end tag ( </*> ) since they are all nested using indentation
syntax. Every nested tag must be indented by ``{y}2 spaces`` from its containing
tag definition. Other than directives and tags, a document can contain,
* plain-text
* comments
* single-line python statements.
* control statements with if-elif-else, for and while constructs.
* functionalised template blocks
* plugins implementing interface API
* filter-blocks

Expression-substitution can be applied pretty much anywhere in the document
with few exceptions like, inside comments and control statements.

Tag definitions can be abstracted into functions with its own local context.
Tags that are not part of any function or interface-api will be grouped under
the function name ''body'' which is defined implicit. It is by making a call
to body(), that the final html is generated and returned, the call is
automatically done by tayra APIs.

h3. Comments

Two types of commenting are allowed, one that will be retained in the final
html text and the other type that will be silently ignored. To retain comments
in the html text, use the following syntax.

{{{ Code ttl
<!--
This file is subject to the terms and conditions defined in
file 'LICENSE', which is part of this source code package.
      Copyright (c) .... ..................
-->
}}}

Well it is similar to HTML comment syntax. These comments can be added
any-where in the document, like nested inside a tag element, function blocks,
or within text content. The other type of comment always starts with a new line
and spans through the entire line, like,

{{{ Code ttl

@function func( name ) :
  ## This comment will be silently ignored.
  <div {} >
    <a#${'idname'}.${'cls'} "http://pluggdapps.com"> hello ${name}

${ func('name') }

}}}

h3. Directives

Directives are meta commands that set-up the context to interpret rest of the
document and generate final html. They are also used to import other
templates, define / use plugins that are defined else where. A directive
typically starts with ''{y}!!!'' or ''{y}@'' and ends with ''{y};''.

h4. Document type directive

This directive can be used to specify html document's DTD
(Document-Type-Definition). Available specifications are,

{{{ Code ttl
!!! xml
!!! xhtml+rdfa 1.0 ;
!!! xhtml 1.1 mobile ;
!!! xhtml 1.1 basic ;
!!! xhtml 1.1 ;
!!! xhtml 1.0 frameset ;
!!! xhtml 1.0 strict ;
!!! xhtml 1.0 transitional ;
!!! html4.01 frameset ;
!!! html4.01 strict ;
!!! html4.01 transitional ;
}}}

If template document does not have doctype specification, it is assumed
as, [<PRE <!DOCTYPE html> >]. For more information on doctypes refer
[[ here | http://www.w3schools.com/tags/tag_doctype.asp ]].

h4. Body directive

As mentioned before, tags that are not part of any function or interface-api
will be grouped under the function named ''body'' which is defined implicit, and
a call to //body()// will return the final html text. It is also possible to
define a call signature for //body()// function using body-directive, where
text following //{y}@body// till the end of directive will be interpreted as
function signature for //body()//. Function signature must be specified in
python syntax like,

{{{ Code ttl
@body id, cls, style='{}';

<div#${id}.${cls} {${style}} >
}}}

Subsquently while evaluating the template file using API interface,

{{{ Code python

from   tayra  import Renderer

r = Renderer( ttlloc=ttlloc, ttlconfig=ttlconfig )

context = {}    # Template context
context.update( _bodyargs=[ 'id_attribute_value', 'class_attribute_value' ] )
context.update( _bodykwargs={ 'style' : "color : blue;" } )

html = r( context=context )
}}}
  

h4. Importing another template

Template functions can be organised as library files, imported as and when
needed. //{y}@include// directive specifies which template file to be imported
and the name to access the template module.

{{{ Code ttl
@include etsite:templates/_base/elements.ttl as e ;
@import os, sys;

@function body_leftpane() :
  ${e.leftpane( menupane )}
}}}

format to specify template file is same as else-where and explained
[[ ./reference#Looking up template files | here ]]. Note that @import can be
used to import python-modules.

h4. Inheriting templates

HTML designers have a pattern of templating their pages
that are stacked up on a base template. For example, pages can have its
layout as header, footer, and left / right panes. The format and
styling of such layout can be handled by a base template, subsequently
inherited by pages that wants to use the same theme. Tayra provides an 
inheritance feature (inspired by [[ mako ]] ) which enables designer to
abstract and organize their templates in more interesting ways. This section
just explains the syntax of //@inherit// directive to declare template
inheritance, more details on how inheritance works and its usage are discussed
further down in a separate section.

{{{ Code ttl
@inherit app:templates/_base/base.ttl ;

@function hd_styles() :
  ${ parent.hd_styles() }
  <style text/css>
    table.config {
      width : 95%;
      margin : 0px auto;
    }
}}}

Inherit directive just accepts a single parameter which is the location of
parent template. Once the directive is declared, the inheriting template can
override functions defined in the parent template.

h4. Implementing plugins

Interfaces are central to template plugins and interface specifications are
coded as python class.

{{{ Code ttl
@implement tayra.interfaces:ITestInterface as testinterface;

@interface ITestInterface.render( *args, **kwargs ):
  <div> interface successfully invoked
}}}

In the above example, //tayra.interfaces// is a python module containing
//ITestInterface// specification. A specification is a class deriving from
//zope.interface.Interface// base class and documents a collection of
attributes and methods, which are to be implemented by template plugins.
//{y}@implement// directive declares that this ttl template implements
//ITestInterface// defining methods specified in //ITestInterface//.
To implement interface methods, //{y}@interface// statement are to be used, as
in the above example, where //render()// method specified in //ITestInterface//
is defined.

h4. Using plugins

Following example illustrates how to use a plugin,

{{{ Code ttl
@use tayra.interfaces:ITestInterface pa as obj;

<html>
  <head>
  <body>
    ${ obj.render() }
}}}

//{y}@use// directive will query plugins implementing
//tayra.interfaces:ITestInterface// specification, by name //pa// and import
that as //obj// in template's global name-space. If plugin name is
omitted, then all plugins implementing the interface will be returned as a
list, otherwise, only plugin object by the specified name (in this example
//pa//) will be returned. It is also possible to do //expression-substitution//
for plugin name, like,

{{{ Code ttl
@use tayra.interfaces:ITestInterface ${plugin_name} as iface;
}}}

where, //plugin_name// is expected in template's context. 

``{s} -- That pretty much sums up the directives available in tayra-templates,
we will now move on to tags``

h3. Anatomy of tag definitions

As described before, tag definitions have indentation rules and follow HTML
syntax. Because of the indentation rule, it is not required to close tags
elements with end tags. Let us start with an example,

{{{ Code ttl
<ul>
  <li> Search the web using
    <a title="Go-to google" href="http://google.com"> google
    search engine.
  <li>
    You can buy books from
    <a title="Go-to amazon" href="http://amazon.com"> amazon
    with excellent discounts
}}}

In the above snippet, we will pick on the anchor tag //{s}a// and see how it
compares with HTML anchor tag definition. Except that there is no closing tag
</a>, there is no difference at all. Any text following the opening-tag is
treated as child node. Now, attribute specification is more or less same as
that of HTML attributes. Apart from this, there are other ways of defining
attributes,
* specifiers
* style

Diving a little bit into the internals, every tag definition will be handled
by a registered tag handler which will return an equivalent HTML snippet, it is
up to the tag-handler to interpret specifiers, styles and attributes.
It is theoretically possible for tag-handlers to interpret child
elements and its text content. Tag handlers are plugins, which can be selected
via config-parameters.

h4. Specifiers

Specifiers are space separated tokens or single-quoted / double-quoted strings.
They are interpreted in tag handlers to generate HTML text. Let us take the
anchor tag example in the previous example and see how specifiers can make it
more concise,

{{{ Code ttl
You can buy books from
<a#am.link.blue:highlt "http://amazon.com" title="Go-to amazon"> amazon
with excellent discounts
}}}

We see that //href="http://amazon.com" // attribute is simply replaced with
//"http://amazon.com" // string, and a sequence of tokens
//#am.link.blue:highlt//. While the interpretation of double-quoted string as
href is specific to anchor-tag handler, //#am.link.blue:highlt// is a standard
specifier syntax that is applicable to all tags and it is tranlated to,

{{{ Code ttl
You can buy books from
<a id="am" class="link blue" name="highlt" href="http://amazon.com" title="Go-to amazon"> amazon
with excellent discounts
}}}

Tag handlers can augment the specifier syntax with its own syntax. Take a look
at [[ ./tags | complete list of specifier syntax ]] that are extended by HTML
tag-handlers.

h4. Style 

Like, //id//, //class//, //name// attributes, //style// is one of the most
commonly used attributes. There is a special syntax to defined inline-styling
for elements. Continuing with the same example,

{{{ Code ttl
You can buy books from
<a#am.link.blue:highlt "http://amazon.com" {background : gray;} title="Go-to amazon"> amazon
with excellent discounts
}}}

we see that //"background: gray;"// inline-styling is added to the tag definition
right after specifier tokens before normal HTML attributes. Text between
'' {...} '' will interpreted as style value.

h4. Attributes

Attributes are defined in exactly same way as HTML attributes, including
definitions like //disabled=disabled// ... ``{y} An important point to note is
that, attributes are always defined after specifiers and styles.``

h3. Expression substitution

Templating supports stuffing dynamic content into final HTML text. Most of the
time it is done via expression substitution ''${...}'' which contains any valid
python expression. Expression will be evaluated under template's context
(including global and local), and the value emitted by the expression will be
converted to unicoded-string (based on encoding-type supplied via config
parameters) and substituted in place of ''${...}''. Expression substitution
is available pretty much any-where in the ttl text, and can span multiple lines.

{{{ Code ttl
<div#${id}.${cls} { ${style} } ${attrs}> ${text}
}}}

In the above example, we have used expression substitution to dynamically
generate value for //id//, //class//, //style// attributes and any other
attributes available in //attrs//. Including the div elements text content.

h4. Escape filters for expression substitution

After converting expression's value to string and before using the string
for substitution, it can be applied on any number of filters. The following is
an example on how to apply escape filters on expressions.

{{{ Code ttl
<div> ${ html_example | h }
}}}

''pipe (|)'' syntax can be suffixed with comma separated list of filters. In 
the above example, //h// denotes //html-escape// filter, since //html_example//
would contain html snippet that needs to be rendered without interpreting it as
html text.

: default filters ::
  Frameworks can use ``{y}escape_filter`` configuration parameter to supply a
  list of default escape filters to be applied on all expression substitution.
  Default filters shall be applied before applying filters specified via
  substitution syntax.
: filter namespace ::
  Filter names can use namespace notation to pass parameters to filters. For
  instance, above example can be changed to
  [<PRE ${ html_example | h, uni.utf-8 } >] where, //uni.utf-8// is Unicode
  decoding filter applied on the text returned by html-escape-filter. //utf-8//
  in //uni.utf-8// specifies what encoding-type must be used for Unicode
  decoding.

''{y}Standard escape filters available in tayra package''

: u ::
  Assume ``text`` as url, quote them using urllib.quote().
: uni.<encoding-type> ::
  Decode text to Unicoded string, using encoding-type provided in
  configuration parameter or using the namespace parameter supplied in 
  this filter, like, [<PRE ${ text | uni.utf-8 } >].
: x ::
  Assume ``text`` as XML, and apply escape encoding.
: h ::
  Assume ``text`` as HTML and apply escape encoding using //markupsafe.escape()//.
: t ::
  Strip (trim) white-spaces before and after ``text`` using strip().
: n ::
  Disable escape-filtering. If first value in the supplied list of escape-filter
  is //{y}n//, escape filtering will altogether be skipped and the string
  value emitted by the expression is substituted as it is.

h3. Statements and control logic

Statement, branching and looping are fundamental control-logic for structured
programming. Although tayra is a templating language, adding programmability
will help localizing view logic and algorithms within the view side of MVC (i.e)
your templates. Looping (for and while) and branching (if-elif-else) constructs
follow python statement and expression syntax. It also follows indentation rules,
only difference is that, control blocks are the usual template text and
control logic is applied on the template text.

h4. Statements

A statement is a valid python line, that will be compiled as it is without
interpreting the value emitted by them. The primary purpose of
statement is to create side-effects to global or local context.
Statements are prefixed by ''@@'' and follow indentation rules. If a statement
is defined in the scope of a function or interface, it is local to the function
with its side-effects similar to executing a statement inside python function.

h4. Alternate templates with if-elif-else

Branch control logic follow python's if-elif-else 
[[ http://docs.python.org/tutorial/controlflow.html | syntax ]] with an ''@''
prefixed to the statements, and ends as-usual with '':'' as a single line.
If statements had to span multiple lines, newlines had to be escaped. After the
statement line, one or more lines of template text must follow, all kinds of
template text are allowed except directives. In the absence of a template
block, use ''@@pass'' to pass the control block as empty. Let us see an example
ttl snippet using if-elif-else block,

{{{ Code ttl
@if a == 'pass' :
  @@pass
@elif a == 2 :
  The program, designed by Odyssey Space Research, will allow crew members to
  conduct several experiments with the phones' cameras, gyroscopes and other
@elif a == 3 :
  <abbr "World Health Organization"> WHO
  <button#id_ reset disabled makefriend "button value"/>
}}}

An mentioned earlier, template text inside branch control logic are indented 2
spaces and can contain template text, tags, statements and nested control blocks.

h4. Looping on templates

To repeat template blocks with dynamic content, use looping
constructs. There are two types of looping syntax available, ''for'' and
''while'' and both map to python's version of //for// and //while//.
Like if-elif-else logic, looping logic follow python's syntax with an ''@''
prefixed to the statements, and ends as-usual with '':'', as a single line.
If statements had to span multiple lines, newlines had to be escaped. After the
statement line, one or more lines of template text must follow, all kinds of
template text are allowed except directives. In the absence of a template
block, use ''@@pass'' to pass the control block as empty. Let us see an example
ttl snippet for and while constructs,

{{{ Code ttl
<table>
  @for i in range(100):
    <tr>
      @@j = 0
      @while j < 4 :
        <td> sample text
        @@j += 1
}}}

h3. Functions

Functions are not program functions, it is a way to abstract and reuse
templates. Functions can be called, with positional arguments and key-word
arguments, to return html text that can be substituted in the
caller's context. Functions are always called inside expression substitution
syntax ''${ ... }''. Functions also provides a local context for templates
that are encapsulated under it. Functions can be nested and follows the same
scoping rules defined by python functions. A function's definition signature
starts with ''@function'' keyword followed by spaces, then function name
(a valid python symbol), open parenthesis, followed by comma separated
positional arguments and keyword arguments, close parenthesis and ends with a
colon '':''. Syntax rules after ''@function'' keyword is exactly same as
that of python's function signature.

{{{ Code ttl

@function justtext() : 
  Google will join its biggest mobile rival, Apple, on the space trip as well.
  Apple's iPhone 4 will join a crew running an app, called "SpaceLab for iOS."

@function involved(z=10):
  <abbr "World Health Organization"> WHO
  @function nestedfunc() :
    <b!> this is nested function
    @function nestednestedfunc() :
      <em!> this is nested nested function
    ${ nestednestedfunc() }
  <button#id_ reset disabled makefriend "button value"/>
  ${ nestedfunc() }
  ${ func3() }
}}}

When functions are combined with template modules, it will provide a powerful
way to abstract and organise your view-templates.

h3. Filter blocks

Filter blocks are extension mechanism for templates. Some times tags and
indentation are not enough, other times it may come in your way while creating
nice looking templates. To overcome that, filter-block syntax is created. A
filter block should be opened in a new-line prefixed by any number of spaces
and then '':fb-<filtername>'', and ends with '':fbend'', which again should
start in a new line and must be flush with characters till end of line. Any
text inside the filter block is directly passed to the implementing plugin with
//<filtername>// as its plugin-name (yep, plugin name must be same as the
filtername specified in opening the filter block). Filter plugins can take
part in compilation phase and can even generate stack machine instructions
directly. We believe this open ended design will lead us to more interesting
language features. Another point to note is that, indentation rules are not
applicable within filter-text. Let us look at an example,

{{{ Code ttl

:fb-pycode global
  a = 'empty'
  def insideroot_butglobal():
    return '<div> insideroot_butglobal </div>'
:fbend

:fb-pycode
  b = '<div> insideroot_insidebody </div>'
:fbend

${ a } ${ insideroot_butglobal() }
${ b }

@function func() :
  <div> hello world
}}}

The above example is using ''pycode'' filter plugin that interprets filter-text
as python code, which gets evaluated inside template's body(). If pycode
filter-block is defined inside a template function, then their content will be
evalued in template function's local scope.  If you carefully look into the
above example, you might observe that the filter blocks are globally defined
(i.e) they are not part of any function, but we must remember that templates
that are defined outside functions are automatically encapsulated inside an
implicitly defined function called //body// (we explain this in previous
section). Hence, variables defined inside these filter blocks are not
accessible inside other functions like, //func//. Now, to define a block of
python code in global scope. we can simply simply pass a parameter, ''global'',
to '':fb-pycode'' filter block's opening line like in the above example.
And by doing this, variable //a// is made available in template global scope.

Didn't we say that filter blocks are open ended design that can lead to
interesting features ! //pycode// is one such feature. Although //pycode// is
implemented purely as a plugin, not being part of the core design, it can
still fiddle with the scope of execution.

h3. Inheritance

For small sites and web applications, template inheritance would not be that
exciting. But once past the toy applications, there will be serious need in
organising templates, prototyping with multiple layouts etc ... and that is
when inheritance feature will take you a long distance. Inheritance
is not new in tayra, especially if have worked with
[[ www.makotemplates.org | mako ]] templates. So, inheritance works like this,

There is a base template which will provide the body() function, called
top-level template structure, that typically defines the page layout, and the
layout simply calls template functions whose return text (html) will be
substituted inside the layout. Once the base template is defined with layout
and default set of virtual template functions, HTML pages, designed again as
templates, can inherit from base template overriding the default set of virtual
template functions. Here is an example,

{{{ Code ttl
## base.ttl
!!! xhtml 1.0 strict ;
<html>
  <head.bootstrap>
    <link image/ico "${favicon}" rel="icon">
    ${self.hd_title()}
    ${self.hd_styles()}
    ${self.hd_script()}

  <body.bootstrap>
    ${self.bd_header()}
    ${self.bd_body()}
    ${self.bd_footer()}

@function hd_title() :
  <title> ${title}

@function hd_styles():
  @@pass

@function hd_script():
  @@jqueryfile = request.static_url('bootstrap:static/jquery-1.6.2.min.js')
  @@jqlibfile = request.static_url('bootstrap:static/jqlib.js')
  <script text/javascript "${jqueryfile}">
  <script text/javascript "${jqlibfile}">

@function bd_header() :
  ${ metanav.render( cssasset=False ) }

@function bd_body():
  <div.ralign> Welcome,
    <a.fntbold "${url_prefern}"> ${ remote_user }

@function bd_footer():
  <div#footer>
    Website content copyright © by ... ...... All rights reserved.
    pluggdapps program and its documentation are licensed under "GPL version-3".
}}}

<br>

{{{ Code ttl
## index.ttl

@inherit bootstrap:templates/_base/base.ttl ;

@function hd_styles() :
  ${ parent.hd_styles() }
  <style text/css>
    .welcome {
      width : 80%;
      margin : 0px auto;
      text-align : center;
    }

@function bd_body() :
  <div#page>
    ${ parent.bd_body() }
    <div.welcome>
      Welcome to Pluggdapps, bootstrap application. The platform is currently running in
      <span.hl> ${ settings['devmod'] and 'development mode' or 'production mode' }.
      It has booted with
      <span.hl> ${ settings['bootwith'] }
      settings and uses
      <span.hl> ${ store.pluginname }
      database client, version
      <span.hl> ${ dbx_version }
      . Character encoding for this application is,
      <span.hl> ${ settings['encoding'] }.
    <div.welcome>
      If you are server administrator, you will be able to do many modification
      to the platform.
}}}

In the above example, //index.ttl// has inherited from //base.ttl//. Where,
base.ttl defines the page layout and provided default template functions that
can be overridden by inheriting templates. Thus index.ttl overrides the functions
//hd_styles()// and //bd_body()// and the HTML text supplied by these functions
will be substituted in place of [<PRE ${ self.hd_style() } >] and
[<PRE ${ self.bd_style() } >]. For functions that are not overridden by
index.ttl, the ones defined in base.ttl will be used.

Inheritance can go any level deep, (i.e) designers can have a base template
which is inherited by any number of intermediate templates and finally by the page
template. While doing inheritance, the global context is slightly modified to
help programmablity. The following //variables// are automatically made
available in the global context,

: local ::
  Always points to the current template module, the //.ttl// file.
: self ::
  Always points to the template instance with all its inheritance chained
  together. Its meaning is same as that of //self// in python objects and
  //this// in C++ objects.
: parent ::
  Refers to the template module inherited by the current template. By
  traversing the //parent// attribute, it possible to reach the top-most (base)
  template in the chain.
: next ::
  Refers to the template module in the opposite direction. By traversing the
  //next// attribute, it is possible to reach the bottom-most (page) template
  in the chain.

h3. Interface functions

Interface functions are special type of template functions that follow all the
rules of a template-function except,
* It starts with a key word ''@interface''
* Function name must be specified in namespace format which will resolve to a
  method specified in an //Interface// class residing in a python module. For
  instance, in the example mentioned bellow, //render()// is the method
  specified by the interface class //IHTMLFormSignin//. It is also important
  that ''@implement'' directive is specified in the beginning.
* The first argument to interface functions is //this//, that refers to the
  plugin instance that encapsulates this interface function definition.

{{{ Code ttl

## Implementing interface IHTMLFormSignin defined in module interfaces.py
## under package bootstrap/templates.

@implement bootstrap.templates.interfaces:IHTMLFormSignin as pa ;

@interface IHTMLFormSignin.render( this, id='', cssasset='bootstrap:static/paview_signin.css' ) :
}}}

h3. Template plugins

Probably tayra is the only web templating language that enable designers to define,
create and distribute their template code as plugins. Working with template
plugins can roughly be divided into four parts, 
# Specifying plugin interface with attributes and methods.
# Implementing one or more template plugin for already specified interface.
# Packaging and exporting template plugins, making it available in //global site
  manager//.
# Using templating plugins inside other templates.

Let us go through them step by step.

h4. Specifying template plugins as interfaces

The first step while creating a plugin is to specify an interface class, as
python script, deriving from //zope.interface:Interface//, with attributes and
methods. Once an interface is defined, any number of templates can implement
their specification. Note that python script containing interface
specification must be importable inside template files. Here is an example,

{{{ Code ttl
class IHTMLFormSignin( IHTMLNode ) :
    """Template interface for user signin-in form. Includes standard
    attributes and methods specified by IHTMLNode, with few of its own. 

    Implementing templates must attribute a class value //signin-<pluginname>//
    to parent most element of the plugin. Supports both //id// and //cssasset//
    keyword arguments specified by IHTMLNode. //Be sure to call render()
    method after initializing its action attribute//.
    """
    
    action = zope.interface.Attribute(
        """Form-Action url for posting form data"""
    )

    def __call__( *args, **kwargs ):
        """Interface-method is reserved for plugin infrastructure and acts as
        a factory of plugin-component. When an implementer (plugin) provide
        this method, then it will be deemed callable, and called upon every
        queryPlugin() matching the plugin-component.

        The return value must be a fresh clone of the plugin-component.
        """

    def render( *args, **kwargs ):
        """A standard method call to be provided by template-plugins,
        returning html snippet that will be rendered along with the page. By
        default, the following keyword arguments are supported,

        :cssasset ::
            If supported by plugins, specify css-styling as static asset file
            which will be included along with template's html result. If the
            specified file has an extension of //.xss//, its //@include//
            references will be interpreted as static-assets and included with
            the template result. //If specified as False//, resulting html will
            not include plugin style, assuming that they are done else-where in
            a site-wide CSS file.
        :id ::
            It is a convention to avoid using //id// attribute in
            template-plugins. But as an exception, this method provides an id
            keyword argument which if present will be attributed to the parent
            most element of the template plugin.

        Implementing plugins can add more keyword arguments to this method.
        """
}}}

The above specification provides an interface to render user-signin form, the
scope of which is to return a html snippet that contains a collection of
<input> elements wrapped inside a <from> element to challenge user for
credentials. Since a form element requires an URL to post the credential
information back to the server, the interface defines an attribute called
//action// to be defined by the caller.

h4. Implementing template plugins

Once an interface is specified, any number of template plugins can be
implemented by declaring an //{y}@implement// directive in the beginning of the
template file. Subsequently, the template file must define interface
methods using //{y}@interface// statement for every method specified in the
interface specification and a corresponding template block must be defined.
Note that the entire implementation must be contained within a single template
file, and the same template file can contain any number of interface
implementations, using an //@implement// directive per interface. Following
is a template file implementing //IHTMLFormSignin// interface, as a template
plugin by name ''pa''

{{{ Code ttl

@implement bootstrap.templates.interfaces:IHTMLFormSignin as pa ;

@interface IHTMLFormSignin.render( this, id='', cssasset='bootstrap:static/paview_signin.css' ) :
  <div#${id}.signin-pa>
    @if cssasset :
      <style text/css>
        ${ h.translate_xss( cssasset ) }
    <form post "${this.action}">
      <fieldset>
        <legend title="IHTMLFormSignin:pa"> User signin
        <table>
          <tr>
            <td>
              <label login> login :
            <td>
              <inptext:login autofocus>
          <tr>
            <td>
              <label password> password :
            <td>
              <inppass:password>
          <tr>
            <td>
            <td>
              <inpsub "signin">
}}}

Template interface functions must accept //this// as their first positional
argument which is exactly similar to python's //self// argument.

Plugin implementers, please note that, TTL plugins should not have any
code executing in the global context, like ``{y}fb-pycode global``, that
depends on other plugins. It is bound to fail or trigger an error.

h4. Packaging and exporting template plugins

Template-plugins will have to be automatically loaded during tayra-module
initialization. To facilitate this, a callable entry point must be defined by
packages containing template plugin, where the callable must return a list of
template file path specified in
[[ ./reference#Looking%20up%20template%20files | asset-specification format ]]. Example,

{{{ Code ini
  [tayra.plugins]
  ITTLPlugin = bootstrap.implement:TTLPlugins
}}}

Entry point //ITTLPlugin// is defined under //[tayra.plugins]// section.
To be more specific, //ITTLPlugin// is the interface specification for this
entry point. When a package has .ttl files implementing plugins, it needs to
implement //ITTLPlugin// interface and define an entry-point for the same
in its //setup.py// file.

''How template plugins are loaded''

Template plugins are loaded explicitly by calling //initplugins()// with
//ttlconfig// dictionary of configuration settings. initplugin()
will detect all packages implementing plugin interfaces, compile them and
load them. Loaded //.ttl// plugins will be saved inside ttlconfig dictionary
as //ttlplugins// key. If you are using tayra via a frame work like pyramid,
then this initialization is automatically handled by the frame-work code. Even
otherwise, when you are going to directly compile a ttl file using
//tayra-API//, plugin loading will be automatically done, if the supplied
//ttlconfig// parameter does not contain //ttlplugins// key.

h4. Using template plugins

Once template plugins are exported to global-site-manager. It can be used
else-where in any tayra template file without bothering about the actual
location of the template plugin. For example, let us create signin page which is
going to use a plugin called ''pa'' implementing IHTMLFormSignin interface,

{{{ Code ttl

@inherit bootstrap:templates/_base/base.ttl ;
@use bootstrap.templates.interfaces:IHTMLFormSignin pa as signin;

@function bd_body() :
  <div#page>
    ${ parent.bd_body() }
    @@ flashmsg =  request.session and request.session.pop_flash( 'signin' ) or ''
    <br/>
    @if flashmsg :
      <mark.flashmsg> ${ flashmsg }
    @@ signin.action = url_signin
    ${ signin.render( cssasset=False ) }

}}}

//{y} @use // directive not only queries for plugin ''pa'' implementing
//IHTMLFormSignin//, it also imports the plugin into our template's global
namespace as //signin//. All we need to do is populate the plugin's attribute
and call the render() method to get the desired HTML snippet.

h3. Developing with tayra

You can checkout the source tree, build and install tayra from that, or you can
install tayra via //easy_install// in your system environment or virtual
environment. It is always better to setup the development tree under a virtual
environment.

h4. Internal design overview

Tayra templating language is based on formal parser grammar and implemented
using formal methods of lexing and parsing (right now it is done using
[[ www.dabeaz.com/ply/ | PLY ]]). The output of the parse phase is an AST
where each node is either derived from //Terminal// class or //NonTerminal//
class. Once the AST is constructed, multi pass compilation via //headpass1//
(for meta-processing), //headpass2// (pre-processing), //generate//
(generating stack-machine instruction), //tailpass// (clean-up) is invoked,
the output of which should be a python file containing stack machine
instruction that can generate the final html based on context. //InstrGen//
class is used by AST nodes, and plugins bolted into AST, to generate
stack-machine instruction. //StackMachine// class implements the actual
stack-machine.

h4. Looking up template files

When invoked as library, using //Renderer()// API, //ttlloc// specifies the
template file to be translated, which can be in either of 2 formats,
# As relative path name to one of the lookup //directories// provided in the
  configuration parameter. Each directory in the list will be looked-up in the
  given order until a file by that path and name is found.
# As static asset, relative to package resource. For instance, if there is a
  .ttl file packaged in <site-package>/<package-name>/path/to/template.ttl,
  ttlloc can be specified as <package-name>:path/to/template.ttl

h4. Complete list of make commands

For developers who would like to check out the source tree and play with it,
can use a bunch of //make commands//, 
To begin with, first checkout the source tree from the latest repository tree
and then use the ''make'' command to create a development environment, if you

{{{ Code sh
  cd tayra
  make develop
}}}

which,
* sets-up a virtual environment under // tayra-env/ // directory.
* Installs tayra under the virtual environment in development mode,
  [<PRE python ./setup.py develop >]

To start using the tayra package, enter the virtual environment by doing,
``{c} source ./tayra-env/bin/activate ``

''To create an egg packages'',

{{{ Code bash
  make bdist_egg        # For creating binary distribution
  make sdist            # For creating source distribution
}}}

The .egg package will be availabe under dist/ directory

''To test the package'',

{{{ Code bash
  source tayra-env/bin/activate
  make test
}}}

''Finally, Build the egg and upload it into pypi''

{{{ Code bash
  make upload
}}}


h3. Miscellaneous

Tayra templating language is made up of grammars with special tokens i.e few
characters and sequence of characters are interpreted differently. Hence
template authors should take special care when using them. Sometimes, it is
required to have the special characters part of the text. This document gives an
overview of how to handle such scenarios.

Characters that are special when occuring in the begnining of a line,

* ''whitespace'', if line begins with a blank-space, it will be consumed as
  indentation, except in the following cases,
  ** comment-blocks, spanning across multiple lines
  ** filter-blocks, between ``{y}:fb-`` and ``{y}:fbend``
* ''newlines'', which has a special-meaning, since indentation is expected to
  follow them.
* ''doctype'', starts with ``{y}!!!``, will generate html DOCTYPE.
* ''directives'', start with ``{y}@``, attaches special meaning to the
  template document.

These characters and character sequences are special anywhere inside the text.

* ''commentline'',  starts with ``{y}##``, will not skipped.
* ''comment-block'', starts with ``{y}<!--`` and ends with ``-->``, will be
  present in the output html.
* ''filter-block'', starts with ``{y}:fb-`` and ends with ``{y}:fbend``,
  can be extended with plugins
* ''statements'', starts with ``{y}@@``
* ''control-blocks'', if lines that follow beginning whitespace start with
  ``{y}@`` it will be interpreted as one of the many control blocks, like,
  function, if-else, while, for.

The following characters and sequences are special within the tag definition,
that comes between ''<''...''>'',

* ''newlines'', will be consumped as whitespace separating tokes.
* ''>'', will be consumed as end of tag definition.
* ''/>'', will be consumed as self-closing end of tag definition.
* ''${...}'', expression substitution.
* '' {...} '', element styling.
* ''" or ' '', string quotes.
* ''='', token that joins attribute name and value.
* ''!>'' and ''%>'', will prune the whitespace and indentations.
* The following characters and sequences are special within tag's style
  specification, that comes between ''{'' .... ''}''
  ** ''${...}'', expression substitution.

escaping special characters,
* To escape special characters, or to break special sequence of characters, use
  escape character, ''\''. This type of escaping is applicable anywhere in the
  text.

-----

{{{ Nested 
# { 'font-size' : 'small', 'color' : 'gray' }
Document edited using Vim <br>
/* vim: set filetype=etx : */
}}}
