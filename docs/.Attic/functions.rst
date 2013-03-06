Template functions
==================

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
