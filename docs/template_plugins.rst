Template plugins
================

Interfaces are central to template plugins and interface specifications are
defined as python class in python modules. Template plugins are 
template-scripts implementing one or more interface specifications. They can
do so by first declaring it using **@implement** directive, like,

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
``ITTLFooter``, defining methods specified in them.

Interface functions
-------------------

To implement interface methods, ``@interface`` statement can to be used. They
are similar ``@def`` statement, but with a semantic meaning that the function
abstracts an interface method defined in the statement,

- It starts with a key word ''@interface''
- Function name must be specified in namespace format which will resolve to a
  method specified in an ``Interface`` class residing in a python module. For
  instance, in the example mentioned above, ``render()`` is the method
  specified by the interface class ``ITTLFooter``.
- The first argument to interface functions is ``self``, that refers to the
  plugin instance that encapsulates this interface function definition.

**Using a template-plugin**

Following example illustrates how to use a plugin,

.. code-block:: ttl
    :linenos:
    
    @doctype html
    @from tayrakit.interfaces import ITTLFooter

    <html>
      <head>
        ...
      <body>
        ...
        <div .footer>
          @@ footer = _compiler.query_plugin( ITTLFooter, 'tayrakit.PluggdappsFooter' )
          @@ counts = { 'interfaces' : interfaces_no, 'plugins' : plugins_no }
          ${ footer.render( counts ) }

- First import the interface class in which we are interested in.
- Use ``_compiler`` object, implicitly available in the template's context, to
  query for plugin implementing the interface-spec. Here we are interested
  for in plugin by name `PluggdappsFooter` implementing `ITTLFooter`.
- Just use the queried plugin like any other python object inside expression
  substitution.

Packaging and exporting template plugins
----------------------------------------

Tayra used pluggdapps' component architecture to provide pluggable templates.
Note that Interfaces and Plugins are expected to be loaded during platform
boot time.

Since template files are not python files and they had to be
compile to template-modules, developers can use pluggdapps's package() entry
point to dynamically compile and load their template plugins. Let us look at
an example.

Let us say that we have started a project to create web UI took-kit and
has choosed to implement UI elements as template-plugins, under the project
directory in template files ::

    toolkit/widgets/timeline.ttl
    toolkit/widgets/twitter.ttl
    toolkit/widgets/tagcloud.ttl
    toolkit/widgets/statistics.ttl
    toolkit/widgets/world_ip_map.ttl

Now to package them as template-plugins, we will have to add an entry point in
our setup.py file like,

.. code-block:: python
    :linenos:

    entry_points={                          # setuptools
        'pluggdapps' : [
            'package=toolkit:package',
        ]
    },

And inside our toolkit/__init__.py package file, we define our entry point as,

.. code-block:: python
    :linenos:

    from tayra  import loadttls

    template_plugins = [
        'toolkit:toolkit/widgets/timeline.ttl',
        'toolkit:toolkit/widgets/twitter.ttl',
        'toolkit:toolkit/widgets/tagcloud.ttl',
        'toolkit:toolkit/widgets/statistics.ttl',
        'toolkit:toolkit/widgets/world_ip_map.ttl',
    ]

    def package( pa ) :
        """A pluggdapps package must implement this entry point. This 
        function will be called during platform pre-booting. Other than some 
        initialization stuff, like dynamically loading template plugins using 
        :func:`loadttls`, this entry point must return a dictionary of 
        key,value pairs describing the package.
        """
        loadttls( pa, template_plugins, { 'debug' : True } )
        return {}

This will make sure that template-plugins are automatically loaded by
``loadttls`` function during platform boot-up, which is when package() entry
point is called.

