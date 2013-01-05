Directives
==========

Directives are meta statements that come in the beginning of template script.
They suggest the compiler to interpret rest of the document in particular ways.
They are also used to import other templates, define / use plugins that are
defined else where. A directive always comes in the beginning and starts with
**@** and ends with a newline.

@doctype directive
------------------

This directive can be used to specify html document's DTD 
(Document-Type-Definition). Available doctypes are are,

.. code-block:: html

    @doctype xml
    @doctype xhtml+rdfa1.0
    @doctype xhtml1.1mobile
    @doctype xhtml1.1basic
    @doctype xhtml1.1
    @doctype xhtml1.0frameset
    @doctype xhtml1.0strict
    @doctype xhtml1.0transitional
    @doctype html4.01frameset
    @doctype html4.01strict
    @doctype html4.01transitional
    @doctype html

If template document does not have doctype specification, it is assumed
as, ``@doctype html``. For more information on doctypes refer
`here <http://www.w3schools.com/tags/tag_doctype.asp>`_

doctype directive also supports an attribute specification called ``charset``.
When a template document is composed using a un-common character-encoding,
developers can specify charater-encoding like,

.. code-block:: html

    @doctype html charset='latin1'    

@body directive
---------------

As mentioned else where, tags that are not part of any function or interface-api
will be grouped under the function named **body** which is defined implicitly,
and a call to **body()** will return the final html text.

Given this design, it is also possible to define a call signature for the
implicitly generated **body()** function using the body-directive.

The text following **@body** till the end of directive will be interpreted as
function signature for **body()**. Function signature must be specified in
python syntax like,

.. code-block:: html

    @body id, cls, style='{}'
    <div #${id} .${cls} {${style}}>

Subsquently while evaluating the template file using API interface,

.. code-block:: python

    pa = Pluggdapps.boot( None )
    compiler = pa.query_plugin( pa, ISettings, 'ttlcompiler' )
    # Compile
    code = compiler.compilettl( file=ttlfile )
    context = {}    # Template context
    context.update( _bodyargs=['id_attribute_value', 'class_attribute_value'] )
    context.update( _bodykwargs={ 'style' : "color : blue;" } )
    # Load
    module = compiler.load( code, context=context )
    # Generate
    html = compiler.generatehtml( module, context )

@import directive
-----------------

Template scripts can be abstracted into functions and organised as a library.
The library templates can be imported in other template scripts using 
**@import** directive, specifying which template file to be imported and the 
name to access the template module.

.. code-block:: html

    @import etsite:templates/_base/elements.ttl as e ;
    @import os, sys;

    @def body_leftpane() :
      ${e.leftpane( menupane )}

Here elements.ttl is imported as a template module and refered as ``e``. The
template module contains a function called ``leftpane(...)`` which is called
further down in the script.

Also note that templates can import python's standard library modules and
refer them in the template script, that is, where ever python code is allowed.

@inherit directive
------------------

HTML designers normally template their pages based on layouts. A layout 
defines base structure of all the pages in the site or web-application
and each page is composed based on one or more templates stacked on top of
each other.

For example, pages can have its layout as header, footer, and
left / right panes provided by a base template called `base.ttl`. Subsequently,
templates stacked on top of the base template defines more detailed structure
for each page.

In Tayra, templates can be stacked on a base template by inheriting them, which
enables designers to abstract and organize their templates in more interesting
ways. This section explains the syntax of **@inherit** directive to
declare template inheritance, more details on how inheritance works and its
usage will be discussed in a separate article.

.. code-block:: html

    @inherit app:templates/_base/base.ttl ;

    @def hd_styles() :
      ${ parent.hd_styles() }
      <style text/css>
        table.config {
          width : 95%;
          margin : 0px auto;
        }

Inherit directive just accepts a single parameter which is the location of
parent template. Once the directive is declared, the inheriting template can
override functions defined in the parent template.

@implement directive
--------------------

Interfaces are central to template plugins and interface specifications are
defined as python class in python modules. Template plugins are template-script
implementing one or more interface specifications. They can do so by first
declaring it using **@implement** directive, like,

.. code-block:: python

    @implement tayra.interfaces:ITestInterface as testinterface;

    @interface ITestInterface.render( args, kwargs ) :
      <div> interface successfully invoked

In the above example, ``tayra.interfaces`` is a python module containing
``ITestInterface`` specification. An interface specification is a python class
deriving from pluggdapps' :class:`Interface` base class and documents a
collection of attributes and methods, which are to be implemented by template
plugins.

**@implement** directive declares that this ttl template implements
``ITestInterface`` defining methods specified in them. To implement interface
methods, **@interface** statement can to be used. They are similar **@def**
statement, but with a semantic meaning that the function abstracts an
interface method defined in the statement. In the above example, template
script implements ``render()`` method specified in ``ITestInterface``.

