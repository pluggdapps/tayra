Template libraries
==================

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

Here elements.ttl is imported as a template module and refered as ``e``. The
template module contains a function called ``leftpane(...)`` which is called
further down in the script.

**Context for library modules**

Like mentioned before, every template script is compiled into a python module.
Likewise, a template library is also compiled into a python module. And they
are interpreted under a context, which contains predefined references like,

``_m``,
    Reference to :class:`StackMachine` instance used to generate the final
    HTML text.

``this``,
    If the caller is part of an inheritance chain, ``this`` refers to 
    script-module at the end of the inheritance chain. Other-wise, refers to
    the caller's module.

``local``,
    Refers to the library module.

``parent``,
    In case of inheriting scripts, ``parent`` will refer to the base template
    from which ``local`` template-script derives.

``next``,
    In case of inheriting scripts, ``next`` will refer to the deriving
    template-script.

``_compiler``,
    Refers to :class:`TTLCompiler` plugin instance.

``_context``,
    Refers to the context dictionary from the caller.

All names ``this``, ``local``, ``parent``, ``next`` refer to the same type of
object - template module. Having a reference to template-module allows developers
to access global variables and functions defined in the module.

In case if a template script is part of an inheritance chain, then attributes
references on the template-module will propogate towards the top of the chain
until an attributed is found in one of the base module.
