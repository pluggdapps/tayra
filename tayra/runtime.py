# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy


"""
Run-time engine, a stack machine interpreting instructions generated by 
:class:`tayra.codegen.InstrGen`. Instructions are nothing but methods on the
stack machine object.

References automatically made available in a template script.
-------------------------------------------------------------

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
object, template-module. Having a refence to template-module allows developers
to access global variables and functions defined in the module.

In case if a template script is part of an inheritance chain, then, attribute
references on the template-module will propogate towards the top of the chain
until an attribute is found in one of the base module.

``_compiler``,
    Refers to :class:`tayra.compiler.TTLCompiler` plugin instance.

``_context``,
    Refers to the context dictionary.

``_ttlhash``,
    Refers to the hash value generated from template text.

``_ttlfile``,
    File name of template script.

``__compiler``,
    Temporary variable that is optionally created for compiling and importing
    library templates. Refers to a :class:`tayra.compiler.TTLCompiler` plugin
    instance.

``__ttlcode``,
    Temporary variable that is optionally created while importing library
    templates.

``<Implemented-interfaces>``,
    When a template script implements an interface, interface name and plugin
    name will also be made available in the global context.

Other than this every template script will have the following standard imports

.. code-block :: python
    :linenos:

    import imp
    from   io                   import StringIO
    from   pluggdapps.plugin    import Plugin, implements
    import pluggdapps.utils     as h
    from   tayra                import BaseTTLPlugin
"""

import re

import pluggdapps.utils     as h

from   tayra.lexer      import TTLLexer
from   tayra.interfaces import ITayraTags, ITayraExpression, ITayraFilterBlock

__traceback_hide__ = True

class StackMachine( object ) :
    """Stack machine instruction interpreterr. Intructions are method calls on
    this object. Supported instructions are,::
    
      indent, append, extend, pushbuf, popbuf, popbuftext, popobject,
      handletag, evalexprs, inherit

    Initializing a stack machine can be a costly operation, so to avoid 
    creating a stack machine object everytime, create it once and call
    :meth:`_init` before interpreting a new template-module.
    """

    def __init__( self, compiler ):
        self.compiler = compiler
        self.encoding = compiler.encoding
        self.tagplugins = [ compiler.qp( ITayraTags, name )
                            for name in compiler['tag.plugins'] ]
        self.tagplugins.append( compiler.qp( ITayraTags, 'tayra.Tags' ))

        self.exprplugins = { p.caname.split('.', 1)[1] : p 
                             for p in compiler.qps(ITayraExpression) }
        self.exprdefault = compiler.qp(
                            ITayraExpression, compiler['expression.default'] )

    def _init( self, ifile ):
        self.bufstack = [ [] ]
        self.ifile = ifile
        self.htmlindent = ''

    #---- Stack machine instructions

    def indent( self ) :
        """Add indentation to output HTML text."""
        return self.append( self.htmlindent )

    def upindent( self, up='' ) :
        """Increase the indentation level for subsequent HTML text by ``up``
        spaces."""
        self.htmlindent += up
        return self.htmlindent

    def downindent( self, down='' ) :
        """Decrease the indentation level for subsequent HTML text by ``down``
        spaces."""
        self.htmlindent = self.htmlindent[:-len(down)]
        return self.htmlindent

    def append( self, value ) :
        """Append ``value`` string to recently pushed buffer in the buffer
        stack."""
        self.bufstack[-1].append( value )
        return value

    def extend( self, value ) :
        """Extend recently pushed buffer in the buffer stack using ``value``
        list."""
        if isinstance(value, list) :
            self.bufstack[-1].extend( value )
        else :
            raise Exception( 'Unable to extend context stack' )

    def pushbuf( self, buf=None ) :
        """Push an empty buffer into the buffer stack."""
        buf = []
        self.bufstack.append( buf )
        return buf

    def popbuf( self ) :
        """Pop the recently pushed buffer in the buffer stack and return the
        same. Return type is a list of strings."""
        return self.bufstack.pop(-1)

    def popbuftext( self ) :
        """Same as :meth:`popbuf` and additionaly join all the string elements
        in the buffer and return the same. Return type is string."""
        x = ''.join( self.popbuf() )
        return x

    def popobject( self ):
        """Return the first element from recently pushed buffer in the buffer
        stack. Discard the remaining buffer. If recently pushed buffer is
        empty, return None."""
        lst = self.popbuf()
        return lst[0] if lst else None

    regex_tag = re.compile( 
        r'(\{[^\}]*\})|(%s=%s)|(%s)|([^ \t\r\n]+)' % (
            TTLLexer.attrname, TTLLexer.attrvalue, TTLLexer.attrvalue ))

    def handletag( self, contents, tagbegin, **kwargs ):
        """Parse ``tagbegin`` for tokens, style and attribute. Along with them
        add ``content`` to pass them to tag-plugin handlers. :meth:`append`
        the html text returned by the handler into the buffer stack.
        
        There are two types of pruning, inner-prunning (specified by <... !>)
        and outer-prunning (specified by <! ...>). Pruning modifiers are
        detected by the AST and passed as part of modifier dictionary.

        optional key-word arguments,

        ``indent``,
            Boolean to keep indentation in output html.
        ``nl``,
            String.
        ``iprune``,
            Boolean, if True, should remove all whitespaces before and after
            the content enclosed by this tag.
        ``oprune``,
            Boolean, if True, should remove all leading and trailining
            whitespaces around this tag element.
        """
        indent = kwargs.get('indent', False)
        nl = kwargs.get('nl', '')
        contents = self.iprune(contents) \
                        if kwargs.get('iprune',False) else contents
        None if kwargs.get('oprune', False) else None

        tagbegin = tagbegin.replace('\n', ' ')[1:-1]    # remove < and >
        try    : tagname, tagbegin = tagbegin.split(' ', 1)
        except : tagname, tagbegin = tagbegin, ''
        
        styles, attributes, tokens = [], [], []
        for m in self.regex_tag.finditer( tagbegin ) :
            if not m : continue
            parts = m.groups()
            parts[0] and styles.append( parts[0][1:-1].strip() )
            parts[1] and attributes.append( parts[1] )
            tokens.extend( parts[2:] )
        tokens = list( filter( None, tokens ))

        for plugin in self.tagplugins :
            html = plugin.handle( self, tagname, tokens, styles, attributes,
                                  contents )
            if html == None : continue
            self.append( html )
            break
        else :
            raise Exception("Unable to handle tag %r" % tagname)

    def evalexprs( self, name, text, filters, globals_, locals_ ) :
        """Evaluate expression ``text`` in ``globals_`` and ``locals_``
        context using plugin prefix in ``text`` or using the
        TTLCompiler['expression.default'] plugin. Convert the resulting 
        object to string, pipe them to the list of filters specified by 
        ``filters``. ``filters`` is comma separated value of escape filters 
        to be applied on the output string.
        """
        exprp=self.exprplugins['expression'+name] if name else self.exprdefault
        out = exprp.eval( self, text, globals_, locals_ )
        if not filters : return out

        filters = h.parsecsv( filters )
        if 'n' in filters : return out

        # TODO : if exprdefault and exprp are same plugin, we might end up
        # calling it twice. Try to improve the performance.
        for f in filters :
            out1 = exprp.filter( self, f, out )
            if out1 == None :
                out1 = self.exprdefault.filter( self, f, out )
            if out1 != None : 
                out = out1
                break
        return out

    def inherit( self, ttlloc, childglobals ):
        """Special instruction used by @inherit directive."""
        compiler = self.compiler()
        code = compiler.compilettl( file=ttlloc )
        # inherit module
        parent_context = childglobals['_context']
        parent_context.update({
            'this'      : childglobals['this'],
            'parent'    : None,
            'next'      : childglobals['local'],
        })
        module = compiler.load( code, context=parent_context )
        childglobals['this']._linkparent( Namespace( None, module ))
        childglobals['local'].parent = module
        return module

    def hitch( self, obj, cls, interfacefunc, *args, **kwargs ) :
        def fnhitched( self, *a, **kw ) :
            kwargs.update( kw )
            return interfacefunc( self, *(args+a), **kwargs )
        return fnhitched.__get__( obj, cls )

    def iprune(self, contents):
        return contents.strip(' \n\r\t\f')


class Namespace( object ):
    """Namespace wrapper for template-modules to traverse the interitance
    chain for referred attributes."""
    def __init__( self, parentnm, localmod ):
        self._parentnm = parentnm
        self._localmod = localmod

    def __getattr__( self, name ):
        if self._parentnm :
            return getattr(
                self._localmod, name, getattr( self._parentnm, name, None )
           )
        else :
            return getattr( self._localmod, name, None )
        
    def __setattr__( self, name, value ):
        if name in [ '_parentnm', '_localmod' ] :
            self.__dict__[name] = value
        else :
            setattr( self._localmod, name, value )
        return value

    def _linkparent( self, parentnm ):
        nm, parnm = self, self._parentnm
        while parnm : nm, parnm = parnm, parnm._parentnm
        nm._parentnm = parentnm
        return parentnm

