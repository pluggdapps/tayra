.. _glossary:

Glossary
========

.. glossary::
  :sorted:

  .ttl
    File containing tayra template script. These templates can be compiled
    into an intermediate **.py** file which can then be loaded and executed,
    with context, to generate the final .html file.

  attributes
    Attributes are key,value pairs. They follow the same syntax defined by 
    HTML attributes and are translated as it is.

  comment
    Two types of commenting are allowed, one that will be translated along with
    template script and the other that will be silently ignored. The former
    type is defined using HTML comment syntax and the later type starts with a
    double hash **##** and spans a single line.

  directives
    Directives are meta constructs that provide more information on how to
    interpret rest of the template script. Specifying document-type, importing
    other ttl files, inheriting a base layout, plugin definition are possible
    through directives.

  escape filtering
    Before substituting an evaluated expressio they are string-ified and 
    optionally piped through filter handlers. Typically these filters will 
    perform actions like html encoding, url encoding etc ...

  expressions
    A key requirement in templated HTML page is to be able to substitute 
    variable content based on the context. In tayra, like many other 
    templating language, substitution is performed using **${ ... }**
    syntax. Text between **${** and **}** will be interpreted as python
    expression, and the value emitted by the expression will be string-ified
    and filtered before substituted in HTML output.

  filter-blocks
    Blocks of text that starts and ends with its own syntax, does not follow 
    indentation rules and have their own parsing logic. New type of filter
    blocks can be defined and extended by plugins. Plugins implementing filter
    blocks directly take part in compilation passes.

  global context
    Global context is the context passed by the caller while translating .ttl
    documents into HTML text. Since tayra embeds python programming within the
    template document, it is possible to create side-effects to global context
    using globals() or using **:py:** filter-block.

  indentation
    HTML is all about nested tags and text content. A HTML document is
    naturally organised as a tree with a root-node. Hence tayra took its
    inspiration from HAML (of RoR) and imposes a strict indentation
    between parent tag and its children. In general, each indentation level
    takes up to 2 blank-space. Thus, for a child tag that is nested 3 levels
    deep should start with 6 blank-spaces. The indentation syntax is followed
    very strictly unless otherwise explicitly mentioned.

  interface
    Plugin interface, follows pluggdapps component architecture. Interfaces
    are called at specific points by core language, some are called during
    compile time, others are called at run-time. Plugins can implement one or
    more interfaces to extend the language definition.

  local context
    Inside templates, functions and interface methods can create a local
    context of its own during execution. Even the root level template text
    that is not part of any function or interface-method will be processed
    under an implicitly defined function called **body()**.

  plugin
    Plugins are pluggdapps components implementing one or more interfaces.
    They are the only means available to extend the language.

  specifiers
    Specifiers are tokens, strings and other structures that can be included
    inside a tag element within the angle-brackets. Some specifiers are 
    common to all tag elements while others are specific to certain tags.
    Plugins defining the tags have freedom to define their own specifier 
    syntax. Note that specifiers are delimited by whitespace.

  statements
    Statements are programmable logic, coded in python, that spans an entire
    line and typically starts with **@** or **@@**. Control block statements
    like if-elif-else and for/while starts with **@** character. Assignment
    statements start with **@@** prefix.

  style
    Style attribute is an often used attribute in HTML, hence a special syntax
    is provided off-the-shelf, **{ ... }**. Text between curly brace will be
    interpreted as the element's style.

  tag
    Typically a tag in a template text has an exact correspondence to HTML 
    tags. Plugins can also define custom tags that are concise and
    sophisticated. It starts with an angle bracket **<**, a **tagname**
    followed by a sequence of name,value pairs called **tag attributes** and
    finally ends with **>**.

    Other than this it can also contain `expressions`, `shortcut tokens`,
    `style` specifiers within the angle-brackets. Since indentation is strictly
    enforced, there is no need to close the tag with **</...>** markup, like in
    HTML. Tags are handled by plugins to generate the corresponding HTML
    output.

  tag-handlers
    Tag handlers are plugins that handle template tag elements. If no 
    tag-handlers are available for the **tagname**, a default handler will be
    used to translate the tag element in safest possible way.

  template-script
    File or string containing text scripted using tayra template language
    syntax.

  template-module
    Every template-script is compiled into a python module and more or less
    follow the semantics of a python module. The compiled template-scripts are
    interpreted as template-module.

  template-plugin
    A template-script implementing one or more interface specifications.
