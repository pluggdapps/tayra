Glossary of terms
=================

``indentation``,
  HTML is all about nested tags and text content. A HTML document is naturally
  organised as a tree with a root-node. Hence tayra took its inspiration
  from HAML (rails community) and imposes a strict indentation between
  parent tag and its children. In general, each indentation level takes up
  2 blank-space. Thus, for a child tag that is nested 3 levels deep should
  have 6 blank-spaces. The indentation syntax is followed very strictly unless
  otherwise explicitly mentioned.

``tag``,
  A tag in a template text has an exact correspondence to HTML tags. It starts
  with an angle bracket **<**, a **tagname** followed by a sequence of
  name,value pairs called **tag attributes** and finally ends with **>**.

  Other than this it can also contain `expressions`, `shortcut tokens`,
  `style` specifiers within the angle-brackets. Since indentation is strictly
  enforced, there is no need to close the tag with **</...>** markup, like in
  HTML. Tags are handled by plugins to generate the corresponding HTML output,
  plugins can define custom tags that are concise and sophisticated.

``expressions``,
  A key requirement in dynamically generating HTML page, is to be able to
  substitute variable content inside the template. In tayra, like many other
  templating language, substitution is performed using **${ ... }**
  syntax. Text between **${** and **}** will be interpreted as python
  expression, and the value emitted by the expression will be string-ified and
  filtered before substituted in HTML output.

``specifiers``,
  Specifiers are tokens, strings and other structures that can be included
  inside a tag element. There are standard specifiers for attributes common to
  all tag elements. Also, corresponding tag-handlers can define their own 
  specifier syntax.

``style``,
  Style attribute is an often used attribute in HTML (there are guidelines
  suggesting to separate styling into CSS file, nevertheless!), hence a
  special syntax is provided off-the-shelf, **{ ... }**. Text between
  curly brace will be interpreted as the element's style.

``attributes``,
  Tag attributes are same as attributes defined by HTML. They will be
  translated as it is.

``tag-handlers``,
  Tag handlers are plugins that handle template tag elements. If no 
  tag-handlers are available for the **tagname**, a default handler will be
  used to translate the tag element in safest possible way.

``directives``,
  Directives are meta constructs that provide more information on how to
  interpret rest of the template script. Specifying document-type, importing
  other ttl files, inheriting a base layout, plugin definition are possible
  through directives.

``statements``,
  Statements are programmable logic that spans an entire line and typically
  starts with **@** or **@@**. Control block statements like if-elif-else and
  for/while starts with **@** character.

``comment``,
  Two types of commenting are allowed, one that will be translated along with
  template script and the other that will be silently ignored.

``filter-blocks``,
  Filter blocks are blocks of text that does not follow indentation rules and
  have their own parsing logic.

``global context``,
  Global context is the context passed by the caller while translating .ttl
  documents into HTML text. Since tayra embeds python programming within the
  template document, it is possible to create side-effects to global context
  using globals() or using **:py:** filter-block.

``local context``,
  Functions and Interfaces can create a local context of its own during
  execution. Even the root level template text that is not part of any function
  or interface-method will be processed under an implicitly defined function
  called **body()**.

``.ttl``,
  File extension for files containing tayra template script. These templates
  can be compiled into an intermediate **.py** file which can then be loaded
  and executed (with context) to generate the final .html file.

``template-script``
  File or string containing text scripted using tayra template language
  syntax.

``template-module``
  Every template-script is compiled into a python module and more or less
  follow the semantics of a python module. The compiled template-scripts are
  interpreted as template-module.

``template-plugin``
  A template-script implementing one or more interface specifications.
