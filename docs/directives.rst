Directives
==========

Directives are meta statements that come in the beginning of template script.
They alter the way rest of the script is compiled and interpreted. They are
also used to import other templates and define plugins. A directive always
come in the beginning and start with **@** and ends with a newline, if
a directive had to span multiple lines escape the new-lines with back-slash.

@doctype
--------

This directive can be used to specify html document's DTD 
(Document-Type-Definition). To template a html5 document,

.. code-block:: ttl
    :linenos:

    @doctype html

This will be translated to ``<!DOCTYPE html>`` in the final html file.
Available `list <./modules/ast.html#tayra.ast.DocType>`_ of doctypes. If
template document does not have doctype specification, it is assumed
as, ``@doctype html``.

For more information on HTML doctypes refer
`here <http://www.w3schools.com/tags/tag_doctype.asp>`_. 

**character-encoding**

@doctype directive also support ``charset`` attribute that can be used to
describe template document's character-encoding. For Example.

.. code-block:: ttl
    :linenos:

    @doctype html charset='latin1'    

@body
-----

As mentioned else where, tags that are not part of any function or 
interface-api will be grouped under an implicitly defined function called
**body**. A call to **body()** will return the final html text. Given this 
design it is also possible, for those who want to integrate tayra with other
tools, to define a call signature that can be used in special cases.

The text following **@body** till the end of directive will be interpreted as
function signature for **body()**. Function signature must be specified in
python syntax like,

.. code-block:: ttl
    :linenos:

    @body id, cls, style=''

    <div #${id} .${cls} { ${style} }>

`id`, and `cls` are positional arguments, and `style` is a keyword argument.
These variables are availabe in the local scope of body function. That is,
they are available for tags that are defined outside the scope of a template
function or template interface method. Subsquently while integrating tayra
with your application,

.. code-block:: python
    :linenos:

    from pluggdapps.platform import Pluggdapps
    from pluggdapps.plugin   import ISettings

    pa = Pluggdapps.boot( None )    # Start pluggdapps component system.
    compiler = pa.query_plugin( pa, ISettings, 'ttlcompiler' )
    # Compile
    code = compiler.compilettl( file=ttlfile )

    context = {}    # Template context
    context.update( _bodyargs=['id', 'class'] )
    context.update( _bodykwargs={ 'style' : "color : blue;" } )

    # Load
    module = compiler.load( code, context=context )
    # Generate
    html = compiler.generatehtml( module, context=context )

@import
-------

Template scripts can be abstracted into functions and organised as a library.
And library templates can be imported in other template scripts using 
**@import** directive by specifying which template file to be imported and a 
name to access the template module.

.. code-block:: ttl
    :linenos:

    @import etsite:templates/_base/elements.ttl as e ;
    @import os, sys;

    @def body_leftpane() :
      ${ e.leftpane( menupane ) }

Here `elements.ttl` is imported as a template module ``e``, which can be
referred in the template script. Further down, you can notice that library
function ``leftpane(...)`` is called from the imported template module.

@inherit directive
------------------

HTML designers normally template their pages based on layouts. A layout 
defines base structure of all the pages in the site or web-application
and each page is composed based on one or more templates stacked on top of
each other.

For example, pages can have its layout as header, footer, and
left / right panes, defined by a base template called `base.ttl`. Subsequently,
templates stacked on top of the base template can add more structure / content
to each element of the layout.

In Tayra, templates can be stacked on a base template by inheriting them, which
enables designers to abstract and organize their templates in more interesting
ways. This section explains the syntax of **@inherit** directive to
declare template inheritance, find `more details <./template_layout.html>`_ on
how inheritance works.

.. code-block:: ttl
    :linenos:

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

.. code-block:: ttl
    :linenos:

    @doctype html
    @implement tayrakit.interfaces:ITTLFooter as PluggdappsFooter

    @interface ITTLFooter.render( self, counts ):
      <div .pluggdappsfooter>
        <div>
          powered by pluggdapps, 
          <span {font-style : italic}> ${counts['plugins']} plugins
          implenting
          <span {font-style : italic}> ${counts['interfaces']} interfaces


In the above example, ``tayrakit.interfaces`` is a python module containing
``ITTLFooter`` specification. An interface specification is a python class
deriving from pluggdapps' :class:`pluggdapps.plugin.Interface` base class and
documents a collection of attributes and methods, which are to be implemented
by template plugins.

**@implement** directive declares that this ttl template implements
``ITTLFooter`` defining methods specified in them. To implement interface
methods, **@interface** statement can to be used. They are similar **@def**
statement, but with a semantic meaning that the function abstracts an
interface method defined in the statement. In the above example, template
script implements ``render()`` method specified in ``ITTLFooter``. 

For more information on template inheritance refer to this
`article <./template_plugins.html>`_.
