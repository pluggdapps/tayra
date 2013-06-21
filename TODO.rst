A roadmap of things to do
=========================

* Whitespace pruning, before and after opening tag and closing tag (for
  outerprune), use tagmodifiers like `-`, `%` `!` etc...  Document it.
 
* Write an article on converting left-recursive AST to right recursive.

* Upload the latest vim-plugin. Write an article in prataprc.github.io on
  using the plugin.

* @from directive to be supported.

* Rename ITayra* interface names to I* names. Remove the `Tayra` prefix to
  names, now that interface names are canonical.

* Example ttl files demonstrating the tokens and shortcuts implemented by
  tayra.tags.html plugin and tayra.tags.forms plugin.
 
* Create hyper link to vim-plugin in README.rst.

* Allow wiki markup as template tag contents. List of wiki markups,
    markdown, reStructuredText, Org-mode, Textile, Asciidoc

* Create hyper link reference for PLY project where ever it is mentioned in
  the document text.

* lexer rules in pygments to support TTL text. Submit ttl lexer to pygment
  project.

* There is an issue with `tayra` script file. It cannot be used from paenv
  environment, still need to use script.py. Issue is related to importing tayra
  module before importing pluggdapps module.

* Create integration points to write JavaScript snippets inside the template.
  Integration points should be extensible to other languages like CoffeScript.

* Implement tayra.decorator functions as plugins and populate the plugin
  instances in template context.

* Do not allow prolog directives after the template script has started. Add
  the condition check in parser.py

* Generate compact HTML (ugly-html) pruning of all redundant whitespaces.

* This whole utf-8-sig business is very patchy. Review the code aand fix
  it properly.

* Bug fix. Parser should pass for empty ttl files. files containing just
  directives or tags.

* Bug fix. The following line creates problem.
    <td.brace1 rowspan="3" {font-size : xx-large;} > {

* Bug fix. The following expression fails, that is when using dictionary.
  ${ conf.render( {}, config ) }
  Once fixed, change template code in config.ttl of etsite, couchpysite,
  tyrsite.

* charset directive should be read and based on the character-set encoding
  the whole text must be re-read. This character set encoding specified in TTL
  text must override the encoding config-param passed by the caller program.
  Intermediate python file should also adhere to this encoding.

* What is BOM in syntax grammar ? Should this part of string encoding or lexer ?
    BOM (EF, BB, BF) syntax is not allowed in utf-8 encoding, so where ever
        codecs.open(...).read() is used stip them off.

* Looks like ':' prefix is used for XML namespace. This is in direct conflict
  with tag name specifier ':', so change it to '::' specifier syntax and 
  translate as is, ':' specifier prefix XML namespace.

* Once stripping is made available (or inline tags),
  http://localhost:5000/bootstrap/config config value must not introduce
  whitespace.

* Check paper.js (Javascript+canvas) and see how one can write plugins in
  tayra using that.

* Propose a mail to various community list explaining the exiting future
  and oppurtunities in HTML5, SVG (and associated standards) and how Tayra
  can play an important role in that.

* Document the scope of escape (\) character.

* Document the special characters that are not allowed in tag-specifiers.

* Document the special characters that are not allowed in content.

* parser.restart() and lex.restart() does not seem to be sufficient, for now
  avoiding reuse of parser and lexer objects. Find a long term solution.

* Remove ITestInterface and replace it with a valid plugin.

* Test cases / profiling / code-coverage.

* ``with`` filter block, something like

    :with: foo = 42
      ${ foo }           ... foo is 42 here
    :with:

     ... foo is not visible here any longer

* Same template might cater to different geography and hence different
  language. Provide a framework so that parts of template are translatable
  based on the language modifier (which mostly comes from HTTP request).

  There are three ways in which this framework be made accessible to template
  authors -  decorators, expression substitution, filterblocks.

* default(value, default_value=u'', boolean=False) context function,

    If the value is undefined in the context it will return the passed 
    default value, otherwise the value of the variable

* Check out Angular JS. Can tayra learn anything from them ?

* Flag error if @function is used in-place of @interface, and vice-versa.

* Flag error if an interfaced is being declared as implemented but 
  some of the methods are not implemented using @interface.

* ITTLPlugin under tayra/plugins.py is to be removed.

* Flag errors when circular inheritance or circular import/include are detected.

* Make tutorial.etx and getStarted.etx and updated reference.etx first 
  paragraph.

* SVG support, Kendo-UI and Component Art.

* Context-based compilation, context-less compilation.

* Code generation optimization.

* Global statements in ttl file should not by body local. They *must* be global.

* How are context functions (from helper file imported) into template context ?

* In ttl_cmdline, don't mix command line options with ttlconfig.

* Refactor ast.py based on `safedesc()` logic defined in Tayra styles, TSS.

* Add expression filter 'dq' and 'sq' to quote the output as string.

* White space preservation.

* Enable wiki text as content selectable using the tag's specifier. like,
    <div etx> **hello** world

* Decorator for generating HTML based on client-agent.

* Ruby's code-block style syntax to write event-handlers for tag-elements.

* Automatically detect the user-agent compatibility level with html and
  generate elements in confirmance to it. This must play safe with the
  following knobs,

  - doctype specification in ttl file
  - encoding specification in ttl file
  - language specification in ttl file
  - config params passed to compile the ttl file
  - HTTP headers (or any other real-time info available from user agent)
    denoting the user agent capabilities.

* Just saw Adobe Egdge ... Can tayra be the keyboard version for addressing
  the same market place as Adobe's ?

* Micro-templating similar to mako. This will demonstrate the true power of
  StackMachine based design.
  This requires a change in the filter-block syntax and symantics. It would be
  better if it is possible to parse the filter-block as signature + siblings.

* Implement them using parser grammar. Once mature the core implementation
  can be ported to C and bolted with many other general pupose languages like
  Java, Ruby, PHP etc ...

* Pure sandboxing in python is not entirely possible. Nevertheless pypy 
  is providing the sandboxing feature, which can be used if required. Some ideas
  for sandboxing,

  * try __builtins__ = {}
  * Avoid passing any objects via which a module object is accessible.
  * Parse the python code found in control blocks, function params,
    and exression substitution and kick out the compromising parts.

* Template authors are responsible for the code that they are writing, along
  with the plugins that they are going to use. The way in which the security
  can be breached beyond the control of the application developer is when 
  anonymous code gets evaluated in the templates context.
  
* Tayra does not use eval anywhere during the compilation process and the
  expression text in expression substitution ${ ... } is directly placed as
  python code.
  
* So as long as the developers do not use eval() anywhere in their template
  text, I guess things should be fairly safe.
  
* May be I am wrong and I would love to stand corrected.

* From stackoverflow,
  http://stackoverflow.com/questions/3558119/are-self-closing-tags-valid-in-html5
  a self-closing div will not validate. This is because a div is a normal
  element, not a void element. According to the spec, tags that cannot have
  any contents (known as void elements) can be self-closing*. This includes
  the following tags:
    area, base, br, col, command, embed, hr, img, input,
    keygen, link, meta, param, source, track, wbr
  The "/" is completely optional on the above tags, however, so <img/> is not
  different from <img>, but <img></img> is invalid.

  So tayra automatically removes any self-closing tags from TAGBEGIN token and
  subsequently tag-handlers under tayra.tags package will generate <hr/> format 
  for void-elements.

Release check-list 
------------------

- Sphinx doc quick-start, one time activity.
        sphinx-quickstart   # And follow the prompts.
        sphinx-apidoc -f -d 2 -T -o  docs/ tayra $(APIDOC_EXCLUDE_PATH)

- Change the release version in ./CHANGELOG.rst, ./tayra/__init__.py

- Update TODO.rst if any, because both CHANGELOG.rst and TODO.rst are referred
  by README.rst.

- Check whether release changelogs in CHANGELOG.rst have their release-timeline
  logged, atleast uptill the previous release.

- Update setup.py and MANIFEST.in for release

- Make sure that sphinxdoc/modules/ has all the modules that need to be
  documented.

- Enter virtual environment and upload the source into pypi.
        make upload

- Upload documentation zip.

- If ttl vim-plugin was updated, package and upload to vim script repository

- After making the release, taging the branch, increment the version number.

- Create a tag and push the tagged branch to 
    code.google.com 
    bitbucket.com
    github.com

