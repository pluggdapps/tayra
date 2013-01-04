The following is the purpose and reason for building `tayra`,
    An integrated web templating environment.

* Define a CSS extension language similar to SCSS.
* Define a html templating language in line with HAML.
* Implement them using parser grammar. Once mature the core implementation
  can be ported to C and bolted with many other general pupose languages like
  Java, Ruby, PHP etc ...
* Create integration points to write JavaScript snippets inside the template.
  Integration points should be extensible to other languages like CoffeScript.
* Plugin architecture : Syntax to define interface specifications and 
  implementation of interface specifications.
* Provide syntax and grammar for higher level abstractions, similar to macros
  and extensions in `eazytext`.
