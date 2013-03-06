Template layouts
================

HTML designers normally template their pages based on layouts. A layout 
defines base structure for all pages in the site / web-application
and each page is composed based on one or more templates stacked on top of
each other.

For example, pages can have its layout as header, footer, and
left / right panes, defined by a base template called `base.ttl`. Subsequently,
templates stacked on top of the base template can add more structure / content
to each element of the layout.

In Tayra, templates can be stacked on a base template by inheriting them, which
enables designers to abstract and organize their templates in more interesting
ways. For example,

.. code-block:: ttl

    <!-- file-name base.ttl -->

    <html>
      <head .pluggdsite>
        <link image/ico "${favicon}" rel="icon">
        ${this.hd_title()}
        ${this.hd_meta()}
        ${this.hd_links()}
        ${this.hd_styles()}
        ${this.hd_script()}
      <body .pluggdsite>
        ${this.bd_header()}
        ${this.bd_body()}
        ${this.bd_footer()}

    @def hd_title() :
      <title> ${title}

    @def hd_meta() :
      @@pass

    ...
  
Is the base template that defines the layout of a html page in a
web-application. In this case the layout is made up of header, body and
footer. Along with that, page-title, page-meta-information,
.css file references, .js file references, are also defined as part of layout.

Along with the layout definition, the base template is expected to provide a
default or dummy (if there is no default behaviour) implementations for
functions like, `hd_title`, `hd_meta`, `hd_links`, `hd_styles`, `hd_script`, 
`bd_header`, `bd_body` and `bd_footer`.

Make a note that if these functions are not called on ``this`` object, then
it always refer to the template-local functions. If, on the other hand these
functions are refered on ``this`` object then, it follows the inheritance
chain. Let use see an example template inheriting our `base.ttl`,

.. code-block:: ttl

    <!-- file-name page.ttl -->

    @inherit app:templates/_base/base.ttl ;

    @def hd_styles() :
      ${ parent.hd_styles() }
      <style text/css>
        table.config {
          width : 95%;
          margin : 0px auto;
        }

    @def bd_body() :
      ${ parent.bd_body() }
      <div .features>
        <p .title>
          Pluggdapps in a nutshell, that it is today and that it will
          be tomorrow.
        <div .search>
          <inptext .search placeholder="Search features ...">
          <a .showall.fntxsmall.pointer> show-all
          <fieldset .floatr>
            <legend> Common search terms
            <div .keywords>
              <span .dsrch.pointer.ralign>plugin
              <span .dsrch.pointer.ralign>template
              <span .dsrch.pointer.ralign>web|html
              <span .dsrch.pointer.ralign>couch
              <span .dsrch.pointer.ralign>tayra
              <span .dsrch.pointer.ralign>program

**@inherit directive**

Inherit directive accepts a single parameter which is the location of
parent template, a.k.a base template. Once the directive is declared, the 
inheriting template can override functions defined in the base template.

**Inheritance and layout**

The deriving template now implements all the layout functions referred in the
base templated. If the deriving template does not have anything to fill in
particular portion of the layout, then it may not implement the
corresponding function, for instance if `page.ttl` is not interested in filling
up meta-information for the page, it can skip implementing ``hd_meta`` layout
function.

The inheritance chain for `page.ttl` can be viewed as, ::
  
    base.ttl ---> page.ttl
    
**`this` magic**

``this`` object is more or less equivalend to python's ``self`` object that
gets implicitly passed to every object method. When a template-script is part
of an inheritance chaing, ``this`` will always refer to the last, or the
bottom-most, template-script which is `page.ttl`. When a template-script is not
part of an inheritance chain ``this`` is same as ``local``. 

Whenever an attribute is referred on ``this`` object, it will walk through
the inheritance chain all the way to the top until it finds a template-script
that defines the referred attribute.

**references implicitly made available in template script**

``_m``,
    Reference to :class:`StackMachine` instance used to generate the final
    HTML text.

``this``,
    Every template script can be viewed as an object instance which can be 
    referenced using ``this``. In case of template scripts making use of 
    inheritance feature, ``this`` will always refer to the template script
    at the end of the inheritance chain.

``local``,
    For non-inheriting template scripts ``this`` and ``local`` refer to the
    same object. In case of template scripts using inheritance feature,
    unlike ``this`` symbol which refers to the template script at the end of
    the inheritance chain, ``local`` will always refer to the template script
    object in which it is used.

``parent``,
    In case of inheriting scripts, ``parent`` will refer to the base template
    from which ``local`` template script derives.

``next``,
    In case of inheriting scripts, ``next`` will refer to the deriving
    template script.

All names ``this``, ``local``, ``parent``, ``next`` refer to the same type of
object - template module. Having a reference to template-module allows
developers to access global variables and functions defined in the module.

For a more upto date documentation on template context refer to
:mod:`tayra.runtime` module.
