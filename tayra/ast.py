# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

"""Module containing Terminal and Non-terminal definitions.

The AST tree is constructed according to the parser-grammar defined in
:mod:`tayra.parser`. From the root non-terminal use the children() method on
every node to walk through the tree.
"""

import sys, re
import pluggdapps.utils as h
from   os.path          import dirname, splitext, basename

from   tayra.utils      import directive_tokens
from   tayra.interfaces import ITayraFilterBlock

# ------------------- AST Nodes (Terminal and Non-Terminal) -------------------

class Node( object ):
    """Base class for all Terminal and Non-terminal nodes. Initialize
    ``parent`` object on the node."""

    parent = None
    """Immediate non-terminal parent node."""

    parser = None
    """:class:`tayra.parser.TTLParser` instance."""

    def __init__( self, parser ):
        self.parent = None
        self.parser = parser
        if not isinstance( self, prolognodes ) :
            parser.ttlparser.prolog = False

    def children( self ):
        """Return a tuple of children for this node in the same order as
        parsed by the grammar rule. Must always be overriden by the deriving
        class.
        """
        return tuple()

    def validate( self ):
        """Validate this node and all the children nodes. Expected to be called
        before starting head-passes on the tree."""
        pass

    def headpass1( self, igen ):
        """Pre-processing phase 1, useful to implement multi-pass compilers"""
        [ x.headpass1( igen ) for x in self.children() ]

    def headpass2( self, igen ):
        """Pre-processing phase 2, useful to implement multi-pass compilers"""
        [ x.headpass2( igen ) for x in self.children() ]

    def generate( self, igen, *args, **kwargs ):
        """Code generation phase. The result must be an executable python
        script"""
        [ x.generate( igen, *args, **kwargs ) for x in self.children() ]

    def tailpass( self, igen ):
        """Post-processing phase 1, useful to implement multi-pass compilers"""
        [ x.tailpass( igen ) for x in self.children() ]

    def lstrip( self, chars ):
        """Strip the leftmost chars from the Terminal nodes. Each terminal node
        must return remaining characters. In case of the Non-terminal node,
        call all the children node's lstrip() method, until the caller
        recieves a non-empty return value.
        """
        pass

    def rstrip( self, chars ):
        """Strip the rightmost chars from the Terminal nodes. Each terminal
        node must return remaining characters. In case of the Non-terminal
        node, call all the children node's rstrip() method, until the caller
        recieves a non-empty return value.
        """
        pass

    def dump( self, context ):
        """Simply dump the contents of this node and its children node and
        return the same.
        """
        return ''.join([ x.dump(context) for x in self.children() ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        """ Pretty print the Node and all its attributes and children
        (recursively) to a buffer.
            
        ``buf``,
            Open IO buffer into which the Node is printed.
        
        ``offset``,
            Initial offset (amount of leading spaces).
        
        ``attrnames``,
            True if you want to see the attribute names in name=value pairs.
            False to only see the values.
        
        ``showcoord``,
            Do you want the coordinates of each Node to be displayed.
        """

    #---- Helper methods

    def getroot( self ):
        """Get root node traversing backwards from this `self` node."""
        node = self
        parent = node.parent
        while parent : node, parent = parent, parent.parent
        return node

    def bubbleup( self, attrname, value ):
        """Bubble up value `value` to the root node and save that as its
        attribute `attrname`"""
        rootnode = self.getroot()
        setattr( rootnode, attrname, value )

    def bubbleupaccum( self, attrname, value, to=None ):
        """Same as bubbleup(), but instead of assigning the `value` to
        `attrname`, it is appended to the list."""
        rootnode = self.getroot()
        l = getattr( rootnode, attrname, [] )
        l.append( value )
        setattr( rootnode, attrname, l )

    @classmethod
    def setparent( cls, parnode, childnodes ):
        [ setattr( n, 'parent', parnode ) 
                for n in childnodes if isinstance(n, Node) ]


class Terminal( Node ) :
    """Abstract base class for all terminal nodes. Initialize ``terminal``
    attribute"""

    terminal = ''
    """Terminal's token String."""

    lineno = None
    """Line number reference where the node starts in the text. Useful in
    debug mode."""

    def __init__( self, parser, lineno, terminal='', **kwargs ):
        Node.__init__( self, parser )
        self.lineno = lineno
        self.terminal = terminal
        [ setattr( self, k, v ) for k,v in kwargs.items() ]

    def __repr__( self ):
        return self.terminal

    def __str__( self ):
        return self.terminal

    def lstrip( self, chars ):
        """Strip off the leftmost characters from the terminal string. Return
        the remaining characters.
        """
        self.terminal = self.terminal.lstrip( chars )
        return self.terminal

    def rstrip( self, chars ):
        """Strip off the rightmost characters from the terminal string. Return
        the remaining characters.
        """
        self.terminal = self.terminal.rstrip( chars )
        return self.terminal

    def generate( self, igen, *args, **kwargs ):
        """Dump the content."""
        igen.puttext( self.dump(None) )

    def dump( self, context ):
        """Simply dump the contents of this node and its children node and
        return the same."""
        return self.terminal

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        """Pretty print the Node and all its attributes and children
        (recursively) to a buffer.
            
        ``buf``,
            Open IO buffer into which the Node is printed.
        
        ``offset``,
            Initial offset (amount of leading spaces) 
        
        ``attrnames``,
            True if you want to see the attribute names in name=value pairs.
            False to only see the values.
        
        ``showcoord``,
            Do you want the coordinates of each Node to be displayed.
        """
        lead = ' ' * offset
        buf.write(lead + '%s: %r' % (self.__class__.__name__, self.terminal))
        buf.write('\n')


class NonTerminal( Node ):      # Non-terminal
    """Abstract base class for all non-terminalnodes. Initialize ``_terms``
    and ``_nonterms``"""

    _terms = []
    """List of :class:`Terminal` nodes under this node."""

    _nonterms = []
    """List of :class:`NonTerminal` nodes under this node."""

    def __init__( self, parser, *args, **kwargs ) :
        super().__init__( parser )
        self._terms = [ x for x in args if isinstance( x, Terminal ) ]
        self._nonterms = [ x for x in args if isinstance( x, NonTerminal ) ]

    def lstrip( self, chars ):
        """Strip off the leftmost characters from children nodes. Stop
        stripping on recieving non null string."""
        value = ''
        for c in self.children() :
            value = c.lstrip( chars )
            if value : break
        return value

    def rstrip( self, chars ):
        """Strip off the rightmost characters from children nodes. Stop
        stripping on recieving non null string."""
        value = ''
        children = list(self.children())
        children.reverse()
        for c in children :
            value = c.rstrip( chars )
            if value : break
        return value

    def gencontrolblock( self, igen, parts, lineno, *args, **kwargs ):
        """Generate control blocks,
            if-elif-else, for and while loops.
        """
        line, INDENT, script, DEDENT = parts
        igen.comment( "lineno:%s" % lineno )
        igen.putstatement( line )
        if script :
            igen.codeindent( up=INDENT.terminal )
            script.generate( igen, *args, **kwargs )
            igen.codeindent( down=DEDENT.terminal )
        else :
            igen.putstatement('pass')
        return None

    def genfunction( self, igen, dline, funsign, script, *args, **kwargs ):
        """Generate function block for 
            @def and @interface.
        """
        igen.cr()
        # Generate decorator
        try :
            line, lineno = dline
            igen.comment( "lineno:%s" % lineno )
            igen.putstatement( dline )
        except : pass
        # Generate function signature
        try :
            line, lineno = funsign
            igen.comment( "lineno:%s" % lineno )
            igen.putstatement( line )
        except : pass

        igen.codeindent( up='  ' )

        # function body
        if script :
            igen.pushbuf()
            kwargs['localfunc'] = True
            script.generate( igen, *args, **kwargs )
            kwargs.pop( 'localfunc' )
        else :
            igen.putstatement('pass')

        # return from function
        igen.flushtext()
        igen.popreturn( astext=True )
        igen.codeindent( down='  ' )
        igen.cr()
        return None

    def flatten( self, attrnode, attrs ):
        """Instead of recursing through left-recursive grammar, flatten them
        into sequential list for looping on them later."""
        node, rclist = self, []

        if isinstance(attrs, str) :
            fn = lambda n : [ getattr(n, attrs) ]
        elif isinstance(attrs, (list,tuple)) :
            fn = lambda n : [ getattr(n, attr) for attr in attrs ]
        else :
            fn = attrs

        while node :
            rclist.extend( filter( None, list(fn(node))) )
            node = getattr(node, attrnode)
        rclist.reverse()
        return rclist


# ------------------- Non-terminal classes ------------------------

class Template( NonTerminal ):
    """class to handle `template` grammar."""

    def __init__( self, parser, script ):
        from tayra.parser import TTLParser
        super().__init__( parser, script )
        self.script = script
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

        self.prologs, self.scripts = [], []
        if script :
            nonterms = script.flatten( 'script', 'nonterm' )[:]
            while nonterms :
                nonterm = nonterms.pop( 0 )
                if isinstance( nonterm, prolognodes ) :
                    self.prologs.append( nonterm )
                    continue
                self.scripts.append( nonterm )
                self.scripts.extend( nonterms )
                break

        self.bodysignature = ''     # Will bubbleup during `headpass`
        self.implements = []        # [ (module, interface, pluginname), ...]
        self.interfaces = []        # [ (interface, methodname), ... ]
        self.htmlprologs = []       # [ html, html, ... ]
        self.importttls = []        # [ (ttlfile, modname), ... ]

    def children( self ):
        return self._nonterms

    def headpass1( self, igen ):
        [ x.headpass1( igen ) for x in self.prologs ]
        [ x.headpass1( igen ) for x in self.scripts ]

    def headpass2( self, igen ):
        igen.initialize()
        [ x.headpass2( igen ) for x in self.prologs ]
        [ x.headpass2( igen ) for x in self.scripts ]

    def generate( self, igen, *args, **kwargs ):
        self.ttlhash = kwargs.pop( 'ttlhash', '' )
        self.ttlfile = self.parser.ttlparser.ttlfile

        # Prolog
        [ x.generate( igen, *args, **kwargs ) for x in self.prologs ]

        # Generate the body function
        igen.cr()
        # Body function signature
        xs = [ self.bodysignature.strip(', \t'), '*args', '**kwargs' ]
        signature = ', '.join( filter( None, xs ))
        line = "def body( %s ) :" % signature
        igen.putstatement( line )
        igen.codeindent( up='  ' )
        igen.pushbuf()
        [ igen.puttext( html, force=True ) for html in self.htmlprologs ] 
        if self.scripts :
            # Body function's body
            [ x.generate( igen, *args, **kwargs ) for x in self.scripts ]
            igen.flushtext()
        else :
            igen.flushtext()
        igen.popreturn( astext=True )
        igen.codeindent( down='  ' )

    def tailpass( self, igen ):
        igen.cr()
        igen.comment( "---- Global Functions", force=True )
        super().tailpass( igen )
        igen.comment( "---- Interface functions", force=True )
        if self.implements and self.interfaces :
            igen.implement_interface( self.implements, self.interfaces )
        igen.cr()
        igen.comment( "---- Footer", force=True )
        igen.footer( self.ttlhash, self.ttlfile )
        igen.finish()

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + '-->template: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+5, attrnames, showcoord) for x in self.children()]


#---- TODO : Not used this class can be removed.
class Prolog( NonTerminal ):
    """class to handle `prolog` grammar."""

    def __init__( self, parser, prolog, nonterm ):
        super().__init__( parser, prolog, nonterm )
        self.prolog, self.nonterm = prolog, nonterm
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return self._nonterms

    def headpass1( self, igen ):
        [ x.headpass1( igen ) for x in self.flatten( 'prolog', 'nonterm' ) ]

    def headpass2( self, igen ):
        [ x.headpass2( igen ) for x in self.flatten( 'prolog', 'nonterm' ) ]

    def generate( self, igen, *args, **kwargs ):
        [ x.generate( igen, *args, **kwargs ) 
                    for x in self.flatten( 'prolog', 'nonterm' ) ]

    def tailpass( self, igen ):
        [ x.tailpass( igen ) for x in self.flatten( 'prolog', 'nonterm' ) ]

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        [x.show(buf, offset, attrnames, showcoord) for x in self.children()]


class DocType( NonTerminal ):
    """class to handle `doctype` grammar. Note that DTDs are deprecated in
    HTML5. We will have to wait and see how it evolves under HTML5.
    
    +-------------------------+-----------------------------------------------+
    | ttl doctype name        | Transted to html                              |
    +=========================+===============================================+
    | html4.01transitional    | <!DOCTYPE HTML PUBLIC                         |
    |                         | "-//W3C//DTD HTML 4.01 Transitional//EN"      |
    |                         | "http://www.w3.org/TR/html4/loose.dtd">       |
    +-------------------------+-----------------------------------------------+
    | html4.01strict          | <!DOCTYPE HTML PUBLIC                         |
    |                         | "-//W3C//DTD HTML 4.01//EN"                   |
    |                         | "http://www.w3.org/TR/html4/strict.dtd">      |
    +-------------------------+-----------------------------------------------+
    | html4.01frameset        | <!DOCTYPE HTML PUBLIC                         |
    |                         | "-//W3C//DTD HTML 4.01 Frameset//EN"          |
    |                         | "http://www.w3.org/TR/html4/frameset.dtd">    |
    +-------------------------+-----------------------------------------------+
    | xhtml1.0transitional    | <!DOCTYPE html PUBLIC                         |
    |                         | "-//W3C//DTD XHTML 1.0 Transitional//EN"      |
    |                         | "http://www.w3.org/TR/xhtml1/DTD/             |
    |                         | xhtml1-transitional.dtd">                     |
    +-------------------------+-----------------------------------------------+
    | xhtml1.0strict          | <!DOCTYPE html PUBLIC                         |
    |                         | "-//W3C//DTD XHTML 1.0 Strict//EN"            |
    |                         | "http://www.w3.org/TR/xhtml1/DTD/             |
    |                         | xhtml1-strict.dtd">                           |
    +-------------------------+-----------------------------------------------+
    | xhtml1.0frameset        | <!DOCTYPE html PUBLIC                         |
    |                         | "-//W3C//DTD XHTML 1.0 Frameset//EN"          |
    |                         | "http://www.w3.org/TR/xhtml1/DTD/             |
    |                         | xhtml1-frameset.dtd">                         |
    +-------------------------+-----------------------------------------------+
    | xhtml1.1                | <!DOCTYPE html PUBLIC                         |
    |                         | "-//W3C//DTD XHTML 1.1//EN"                   |
    |                         | "http://www.w3.org/TR/xhtml11/DTD/            |
    |                         |  xhtml11.dtd">                                |
    +-------------------------+-----------------------------------------------+
    | xhtml1.1basic           | <!DOCTYPE html PUBLIC                         |
    |                         | "-//W3C//DTD XHTML Basic 1.1//EN"             |
    |                         | "http://www.w3.org/TR/xhtml-basic/            |
    |                         | xhtml-basic11.dtd">                           |
    +-------------------------+-----------------------------------------------+
    | xhtml1.1mobile          | <!DOCTYPE html PUBLIC                         |
    |                         | "-//WAPFORUM//DTD XHTML Mobile 1.2//EN"       |
    |                         | "http://www.openmobilealliance.org/tech/DTD/  |
    |                         | xhtml-mobile12.dtd">                          |
    +-------------------------+-----------------------------------------------+
    | xhtml+rdfa1.0           | <!DOCTYPE html PUBLIC                         |
    |                         | "-//W3C//DTD XHTML+RDFa 1.0//EN"              |
    |                         | "http://www.w3.org/MarkUp/DTD/                |
    |                         | xhtml-rdfa-1.dtd">                            |
    +-------------------------+-----------------------------------------------+
    | html                    | <!DOCTYPE html>                               |
    +-------------------------+-----------------------------------------------+
    """

    dtdurls = {
      "html4.01transitional"    : (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" '
            '"http://www.w3.org/TR/html4/loose.dtd">' ),

      "html4.01strict"          : (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
            '"http://www.w3.org/TR/html4/strict.dtd">' ),

      "html4.01frameset"        : (
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" '
            '"http://www.w3.org/TR/html4/frameset.dtd">' ),

      "xhtml1.0transitional"    : (
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
            '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">' ),

      "xhtml1.0strict"          : (
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '
            '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">' ),

      "xhtml1.0frameset"        : (
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" '
            '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">' ),

      "xhtml1.1"                : (
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" '
            '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">' ),

      "xhtml1.1basic"           : (
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML Basic 1.1//EN" '
            '"http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">' ),

      "xhtml1.1mobile"          : (
          '<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.2//EN" '
          '"http://www.openmobilealliance.org/tech/DTD/xhtml-mobile12.dtd">' ),

      "xhtml+rdfa1.0"           : (
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.0//EN" '
            '"http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd">' ),

      "html"                    : '<!DOCTYPE html>',
    }

    def __init__( self, parser, directive, newlines ) :
        super().__init__( parser, directive, newlines )
        self.DIRECTIVE, self.NEWLINES = directive, newlines
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return self._terms

    def headpass1( self, igen ):
        params = directive_tokens( self.DIRECTIVE.dump(None) )
        for param in params :
            dtd = self.dtdurls.get( param, '' )
            if dtd :
                dtd += self.NEWLINES.dump(None)
                self.bubbleupaccum( 'htmlprologs', dtd )
                break
        super().headpass1( igen )

    def generate( self, igen, *args, **kwargs ):
        pass

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'doctype: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class Body( NonTerminal ):
    """class to handle ``body`` grammar."""

    def __init__( self, parser, directive, newlines ) :
        super().__init__( parser, directive, newlines )
        self.DIRECTIVE, self.NEWLINES = directive, newlines
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return self._terms

    def headpass1( self, igen ):
        self.signature = self.DIRECTIVE.dump(None)[5:].strip(' \t\r\n')
        self.bubbleup( 'bodysignature', self.signature )
        super().headpass1( igen )

    def generate( self, igen, *args, **kwargs ):
        pass

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'body: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class ImportAs( NonTerminal ):
    """class to handle `importas` grammar. Supported variants

    To import python modules, ::

        @import .. [, .., ..]
        @import .. [as ..]
        @from .. import .. [,..,..]

    To import template-modules, ::

        @include .. [, .., ..]
        @include .. [as ..]
    """

    def __init__( self, parser, directive, newlines ) :
        super().__init__( parser, directive, newlines )
        self.DIRECTIVE, self.NEWLINES = directive, newlines
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return self._terms

    def parseline(self, line):
        mainfile = self.parser.compiler.ttlfile
        relpath = dirname(mainfile) if mainfile else None
        parts = list( filter( None, [ x for x in line.split(' ') ] ))
        ttlfile, modname = None, None

        if len(parts) == 2 and parts[0] == 'include' :
            ttlfile = h.abspath_from_asset_spec( parts[1], relativeto=relpath )
            modname = splitext( basename( ttlfile ))[0]

        elif len(parts) == 4 and (parts[0], parts[2]) == ('include', 'as') :
            ttlfile = h.abspath_from_asset_spec( parts[1], relativeto=relpath )
            modname = parts[3]

        return ttlfile, modname

    def headpass2( self, igen ):
        line = self.DIRECTIVE.dump(None)[1:]
        ttlfile, modname = self.parseline(line)
        if ttlfile and modname :    # include directive
            igen.importttl( modname, ttlfile )
        else :                      # import directive
            igen.putstatement( line )

    def generate( self, igen, *args, **kwargs ):
        pass

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'importas: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class Inherit( NonTerminal ):
    """class to handle `inherit` grammar.
        @inherit <base-ttl-file> 
    """

    def __init__( self, parser, inherit, newlines ) :
        super().__init__( parser, inherit, newlines )
        self.INHERIT, self.NEWLINES = inherit, newlines
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return self._terms

    def headpass2( self, igen ):
        parts = self.INHERIT.dump(None).strip(' \t\r\n').split(' ')
        parts = list( filter( None, parts ))
        igen.putinherit( parts[1] )
        super().headpass2( igen )

    def generate( self, igen, *args, **kwargs ):
        pass

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'inherit: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class Implement( NonTerminal ):
    """class to handle `implement` grammar.
        @implement <Interface-class> as <pluginname> 
    """

    def __init__( self, parser, directive, newlines ) :
        super().__init__( parser, directive, newlines )
        self.DIRECTIVE, self.NEWLINES = directive, newlines
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return self._terms

    def headpass1( self, igen ):
        parts = [ x.strip() for x in 
                  self.DIRECTIVE.dump(None).strip(' \t\r\n').split(' ') ]
        parts = list( filter( None, parts ))
        assert parts[2] == 'as'
        module, interfacename = parts[1].split(':', 1)
        self.bubbleupaccum(
                'implements', (module, interfacename.strip(), parts[3]) )
        super().headpass1( igen )

    def generate( self, igen, *args, **kwargs ):
        pass

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'implement: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


#TODO : Remove this AST @use directive is removed.
class Use( NonTerminal ):
    """class to handle `use` grammar."""

    def __init__( self, parser, directive, newlines ) :
        super().__init__( parser, directive, newlines )
        self.DIRECTIVE, self.NEWLINES  = directive, newlines
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def _parseline( self, line ):
        # TODO : Broken !! Fix this
        parts = list( filter( None, map(
            lambda x : x [0],
            re.findall( r'((\$\{.+\})|([^ \r\n\f\t]+))(?=[ \t]|$)', line )
        )))
        if len(parts) == 5 and (parts[0], parts[3]) == ('@use', 'as') :
            interface, pluginname, importname = parts[1], parts[2], parts[4]
        elif len(parts) == 4 and (parts[0], parts[2]) == ('@use', 'as') :
            interface, pluginname, importname = parts[1], '', parts[3]
        else :
            raise Exception( '@use directive syntax error' )
        module, interfacename = interface.split(':')
        match = re.match( r'\$\{(.+)\}', pluginname )
        if match :
            text, filters = ExprsContents.parseexprs( match.groups()[0] )
            pluginname = text, filters
        return module, interfacename, pluginname, importname

    def children( self ):
        return self._terms

    def headpass2( self, igen ):
        line = self.USE.dump(None).strip(' \t\r\n')
        self.module, self.interfacename, self.pluginname, self.name = \
                self._parseline( line )
        igen.comment( self.USE.lineno )
        igen.comment( "lineno:%s" % self.USE.lineno )
        igen.useinterface(
                self.module, self.interfacename, self.pluginname, self.name )
        super().headpass2( igen )

    def generate( self, igen, *args, **kwargs ):
        pass

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'use: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class Script( NonTerminal ):
    """class to handle `script` grammar."""

    def __init__( self, parser, script, nonterm ) :
        super().__init__( parser, script, nonterm )
        self.script, self.nonterm = script, nonterm
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return self._nonterms

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        [x.show(buf, offset, attrnames, showcoord) for x in self.children()]


class CommentLine( NonTerminal ):
    """class to handle `commentline` grammar."""

    def __init__( self, parser, line, newlines ) :
        super().__init__( parser, line, newlines )
        self.COMMENTLINE, self.NEWLINES = line, newlines
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return self._terms

    def generate( self, igen, *args, **kwargs ):
        pass

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'commentline: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class CommentBlock( NonTerminal ):
    """class to handle `commentblock` grammar."""

    def __init__( self, parser, commentopen, commenttext, commentclose, nl,
                  prolog ) :
        super().__init__( parser, commentopen, commenttext, commentclose, nl )
        self.COMMENTOPEN, self.COMMENTTEXT, self.COMMENTCLOSE, self.NEWLINES=\
                commentopen, commenttext, commentclose, nl
        self.prolog = prolog
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return self._terms

    def headpass1( self, igen, *args, **kwargs ):
        if self.prolog == True :
            self.bubbleupaccum( 'htmlprologs', self.dump(None) )

    def generate( self, igen, *args, **kwargs ):
        if self.prolog == False :
            super().generate( igen, *args, **kwargs )

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'commentblock: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


prolognodes = (
  DocType, Body, ImportAs, Inherit, Implement, Use, CommentBlock, CommentLine
)


class Statement( NonTerminal ):
    """class to handle `statement` grammar."""

    def __init__( self, parser, statement, newlines ) :
        super().__init__( parser, statement, newlines )
        self.STATEMENT, self.NEWLINES = statement, newlines
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return self._terms

    def generate( self, igen, *args, **kwargs ):
        line = self.STATEMENT.dump(None).lstrip('@ \t')
        igen.comment( "lineno:%s" % self.STATEMENT.lineno )
        if line.startswith( 'return' ) :
            try    : keyword, expression = line.split(' ')
            except : keyword, expression = line, None
            if expression :
                igen.popobject( returnwith=expression )
            else :
                igen.popobject()
        else :
            igen.putstatement( line )

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'statement: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class TagLine( NonTerminal ):
    """class to handle `tagline` grammar."""

    def __init__( self, parser, tagspans, newlines ) :
        super().__init__( parser, tagspans, newlines )
        self.tagspans, self.NEWLINES = tagspans, newlines
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return list( filter( None, (self.tagspans, self.NEWLINES) ))

    def genhandle( self, igen, *args, **kwargs ):
        self.tagspans.genhandle( igen, *args, **kwargs )

    def generate( self, igen, *args, **kwargs ):
        igen.comment( "lineno:%s" % self.tagspans.TAGBEGIN.lineno )
        super().generate( igen, *args, **kwargs )
        if not isinstance( self.parent, TagBlock ):
            self.genhandle( igen, *args, **kwargs )

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'tagline: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]

class TagSpans( NonTerminal ):
    """class to handle `tagspans` grammar. TagSpans go through a twisted logic
    of reverse generate() using self.parent. Be careful when changing this
    code !!!"""

    iprune = False
    """Boolean, if True, should remove all whitespaces before and after the 
    content enclosed by this tag."""

    oprune = False
    """Boolean, if True, should remove all leading and trailining whitespaces
    around this tag element."""

    def __init__( self, parser, tagspans, tagbegin, text ) :
        super().__init__( parser, tagspans, tagbegin, text )
        self.tagspans, self.TAGBEGIN, self.text = tagspans, tagbegin, text
        # Set parent attribute for children, should be last statement !!
        tbtext = tagbegin.dump(None)
        self.oprune = '!' == tbtext[1]
        self.iprune = '!' == tbtext[-2]
        self.setparent( self, self.children() )

    def children( self ):
        """Return the children in right recursive fashion."""
        x = self.TAGBEGIN, self.text, self.tagspans
        return list( filter( None, x ))

    def right_recursive( self, tagspans, TAGBEGIN, text ):
        """Convert left recursion to right recursion so that generate() can be
        a straight forward logic. Call this method right in the parser once
        the top node of the left recursive tree is detected."""
        ts = TagSpans( self.parser, tagspans, TAGBEGIN, text )
        if self.tagspans :
            TAGBEGIN, text = self.tagspans.TAGBEGIN, self.tagspans.text
            return self.tagspans.right_recursive( ts, TAGBEGIN, text )
        return ts

    def genhandle( self, igen, *args, **kwargs ):
        igen.handletag(
                indent=False, nl='', iprune=self.iprune, oprune=self.oprune )

    def generate( self, igen, *args, **kwargs ):
        from  tayra.lexer import TTLLexer
        # TAGBEGIN
        tagbegin = self.TAGBEGIN.dump(None).strip(' \t')
        igen.pushbuf()
        s = 0
        for m in re.finditer( TTLLexer.exprsubst, tagbegin ) :
            expr = m.group()
            start, end = m.regs[0]
            igen.puttext( tagbegin[s:start] )
            igen.evalexprs( expr[2:-1] )
            s = end
        igen.puttext( tagbegin[s:] ) if tagbegin[s:] else None

        # TEXT
        igen.pushbuf()
        if self.text :
            self.text.generate( igen, *args, **kwargs )

        if self.tagspans :
            self.tagspans.generate( igen, *args, **kwargs )

        if isinstance( self.parent, TagSpans ) :
            self.genhandle( igen, *args, **kwargs )

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'tagspans: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class TagBlock( NonTerminal ):
    """class to handle `tagblock` grammar."""

    def __init__( self, parser, tagline, indent, script, dedent ) :
        super().__init__( parser, tagline, indent, script, dedent )
        self.tagline, self.INDENT, self.script, self.DEDENT = \
                tagline, indent, script, dedent
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        x = self.tagline, self.INDENT, self.script, self.DEDENT
        return list( filter( None, x ))

    def generate( self, igen, *args, **kwargs ):
        super().generate( igen, *args, **kwargs )
        self.tagline.genhandle( igen, *args, **kwargs )

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'tagblock: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class Text( NonTerminal ):
    """class to handle `text` grammar."""

    def __init__( self, parser, text, textterm ) :
        super().__init__( parser, text, textterm )
        self.text, self.TEXT = text, textterm
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return list( filter( None, (self.text, self.TEXT) ))

    def generate( self, igen, *args, **kwargs ):
        igen.comment( "lineno:%s" % self.TEXT.lineno )
        text = self.dump( None )
        if text :
            self.generate_text( text, igen, *args, **kwargs )

    def generate_text( self, text, igen, *args, **kwargs ):
        from  tayra.lexer import TTLLexer
        s = 0
        for m in re.finditer( TTLLexer.exprsubst, text ) :
            expr = m.group()
            start, end = m.regs[0]
            igen.puttext( text[s:start] )
            igen.evalexprs( expr[2:-1] )
            s = end
        igen.puttext( text[s:] ) if text[s:] else None

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'text: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class TextSpan( NonTerminal ):
    """class to handle `textspan` grammar."""

    def __init__( self, parser, text, tagspans, newlines ) :
        super().__init__( parser, text, tagspans, newlines )
        self.text, self.tagspans, self.NEWLINES = text, tagspans, newlines
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return list( filter( None, (self.text, self.tagspans, self.NEWLINES)))

    def generate( self, igen, *args, **kwargs ):
        super().generate( igen, *args, **kwargs )
        self.tagspans.genhandle( igen, *args, **kwargs )

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'text: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class TextBlock( NonTerminal ):
    """class to handle `textblock` grammar."""

    def __init__( self, parser, tb, text, newlines, indent, script, dedent ):
        super().__init__( parser, tb, text, newlines, indent, script, dedent )
        self.tb, self.text, self.NEWLINES = tb, text, newlines
        self.INDENT, self.script, self.DEDENT = indent, script, dedent
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        x = ( self.tb, self.text, self.NEWLINES, self.INDENT, self.script,
              self.DEDENT )
        return list( filter( None, x ))

    def generate( self, igen, *args, **kwargs ):
        # Textblock
        self.tb.generate( igen, *args, **kwargs ) if self.tb else None
        # TEXT
        if self.text :
            self.text.generate( igen, *args, **kwargs )
        # NEWLINE
        if self.NEWLINES :
            self.NEWLINES.generate( igen, *args, **kwargs )
        # Nested script.
        [ c.generate( igen, *args, **kwargs )
            for c in filter( None, (self.INDENT,self.script,self.DEDENT) ) ]

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        [x.show(buf, offset, attrnames, showcoord) for x in self.children()]


class InterfaceBlock( NonTerminal ):
    """class to handle `interfaceblock` grammar."""

    def __init__( self, parser, interface, nl, indent, script, dedent ) :
        super().__init__( parser, interface, nl, indent, script, dedent )
        self.INTERFACE, self.NEWLINES, self.INDENT,self.script,self.DEDENT =\
                interface, nl, indent, script, dedent
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        x = ( self.INTERFACE, self.NEWLINES, self.INDENT, self.script,
              self.DEDENT )
        return list( filter( None, x ))

    def headpass1( self, igen ):
        # Parse interface signature, for interface-name, method-name and
        # function-signature.
        I = self.INTERFACE
        interface, signature = I.dump(None).strip().split('(', 1)
        interfacename, methodname = interface[10:].rsplit('.', 1)
        self.funcline = ('def ' + methodname + '(' + signature), I.lineno
        # Bubble up
        self.bubbleupaccum('interfaces', (interfacename.strip(), methodname))
        super().headpass1( igen )

    def generate( self, igen, *args, **kwargs ):
        self.args, self.kwargs = args, kwargs

    def tailpass( self, igen ):
        self.genfunction( igen, None, self.funcline, self.script, 
                          *self.args, **self.kwargs )
        # Do tail pass after the deferred generation.
        super().tailpass( igen )

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'interfaceblock: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class FunctionBlock( NonTerminal ):
    """class to handle `functionblock` grammar."""

    def __init__( self, parser, decorator, nl1, function, nl2, indent, 
                        script, dedent ):
        super().__init__( parser, decorator, nl1, function, nl2, indent,
                          script, dedent )
        (self.DECORATOR, self.NEWLINES1, self.FUNCTION, self.NEWLINES2,
                self.INDENT, self.script, self.DEDENT) = \
                        decorator, nl1, function, nl2, indent, script, dedent
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        x = ( self.DECORATOR, self.NEWLINES1, self.FUNCTION, self.NEWLINES2,
              self.INDENT, self.script, self.DEDENT )
        return list( filter( None, x ))

    def headpass1( self, igen ):
        D, F = self.DECORATOR, self.FUNCTION
        # Function signature
        if D :
            self.dline = ' '.join( D.dump(None).splitlines() )
            line = '@' + self.dline[4:].strip() + self.NEWLINES1.dump(None)
            self.dline = line, D.lineno
        else :
            self.dline = None
        self.fline = F.dump(None).strip()[1:], F.lineno
        super().headpass1( igen )

    def generate( self, igen, *args, **kwargs ):
        self.localfunc = kwargs.get( 'localfunc', False )
        self.args, self.kwargs = args, kwargs
        if self.localfunc :
            # Function block, script will be generated via genfunction.
            self.genfunction(
                    igen, self.dline, self.fline, self.script, args, kwargs )

    def tailpass( self, igen ):
        if self.localfunc == False :
            # Function block, script will be generated via genfunction
            self.genfunction( igen, self.dline, self.fline, self.script,
                              *self.args, **self.kwargs )
        # Do tail pass after the deferred generation.
        super().tailpass( igen )

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'functionblock: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class FilterBlock( NonTerminal ):
    """class to handle `filterblock` grammar. Contains the following
    terminals,

    ``FILTEROPEN``,
        terminal that opens the filterblock.

    ``NEWLINES1``,
        one or more newline characters that follow the FILTEROPEN terminal.

    ``FILTERTEXT``,
        array of FILTERTEXT terminal nodes, the value of the each terminal 
        node contains a single line of filtertext and includes one or more
        newlines that separates this line from the next.

    ``FILTERCLOSE``,
        terminal that closes the filterblock.

    ``NEWLINES2``,
        one or more newline characters that follow the FILTERCLOSE terminal.
    """

    def __init__(self, parser, filteropen, nl1, filtertext, filterclose, nl2):
        super().__init__(parser,filteropen,nl1,filtertext,filterclose,nl2 )
        self.FILTEROPEN, self.filtertext, self.FILTERCLOSE = \
                filteropen, filtertext, filterclose
        self.NEWLINES1, self.NEWLINES2 = nl1, nl2
        name = 'tayra.filterblock' + filteropen.dump(None)[1:].split(':', 1)[0]
        self.plugin = parser.compiler.qp( ITayraFilterBlock, name )
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        x = ( self.FILTEROPEN, self.NEWLINES1, self.filtertext,
              self.FILTERCLOSE, self.NEWLINES2 )
        return list( filter( None, x ))

    def headpass1( self, igen ):
        self.passresult = self.plugin.headpass1( igen, self )

    def headpass2( self, igen ):
        self.passresult = self.plugin.headpass2( igen, self, self.passresult )

    def generate( self, igen, *args, **kwargs ):
        self.passresult = self.plugin.generate(
                                igen, self, self.passresult, *args, **kwargs )

    def tailpass( self, igen ):
        self.passresult = self.plugin.tailpass( igen, self, self.passresult )

    def dump( self, context ):
        cs = [ self.FILTEROPEN, self.NEWLINES1 ] + self.filtertext +  \
             [ self.FILTERCLOSE, self.NEWLINES2 ]
        return ''.join([ c.dump(context) for c in cs ])

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'filterblock: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        cs = [ self.FILTEROPEN, self.NEWLINES1 ] + self.filtertext +  \
             [ self.FILTERCLOSE, self.NEWLINES2 ]
        return [ c.show( buf, offset+2, attrnames, showcoord ) for c in cs ]


#---- Control Blocks

class IfelfiBlock( NonTerminal ):
    """class to handle `ifelfiblock` grammar."""

    def __init__( self, parser, ifelfiblock, ifblock, elifblock, elseblock ) :
        super().__init__( parser, ifelfiblock, ifblock, elifblock, elseblock )
        self.ifelfiblock, self.ifblock, self.elifblock, self.elseblock = \
                ifelfiblock, ifblock, elifblock, elseblock
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        return self._nonterms

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'ifelfiblock: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class IfBlock( NonTerminal ):
    """class to handle `ifblock` grammar."""

    def __init__( self, parser, iff, newlines, indent, script, dedent ):
        super().__init__( parser, iff, newlines, indent, script, dedent )
        self.IF, self.NEWLINES, self.INDENT, self.script, self.DEDENT = \
                iff, newlines, indent, script, dedent
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        x = ( self.IF, self.NEWLINES, self.INDENT, self.script, self.DEDENT )
        return list( filter( None, x ))

    def generate( self, igen, *args, **kwargs ):
        line = 'if' + self.IF.dump(None)[3:]
        parts = line, self.INDENT, self.script, self.DEDENT
        self.gencontrolblock( igen, parts, self.IF.lineno, *args, **kwargs )
        return None

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'ifblock: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class ElifBlock( NonTerminal ):
    """class to handle `elifblock` grammar."""

    def __init__( self, parser, elif_, newlines, indent, script, dedent ) :
        super().__init__( parser, elif_, newlines, indent, script, dedent )
        self.ELIF, self.NEWLINES, self.INDENT, self.script, self.DEDENT = \
                elif_, newlines, indent, script, dedent
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        x = self.ELIF, self.NEWLINES, self.INDENT, self.script, self.DEDENT
        return list( filter( None, x ))

    def generate( self, igen, *args, **kwargs ):
        line = 'elif' + self.ELIF.dump(None)[5:]
        parts = line, self.INDENT, self.script, self.DEDENT
        self.gencontrolblock( igen, parts, self.ELIF.lineno, *args, **kwargs )
        return None

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'elifblock: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class ElseBlock( NonTerminal ):
    """class to handle `elseblock` grammar."""

    def __init__( self, parser, else_, newlines, indent, script, dedent ):
        super().__init__( parser, else_, newlines, indent, script, dedent )
        self.ELSE, self.NEWLINES, self.INDENT, self.script, self.DEDENT = \
                else_, newlines, indent, script, dedent
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        x = self.ELSE, self.NEWLINES, self.INDENT, self.script, self.DEDENT
        return list( filter( None, x ))

    def generate( self, igen, *args, **kwargs ):
        line = 'else' + self.ELSE.dump(None)[5:]
        parts = line, self.INDENT, self.script, self.DEDENT
        self.gencontrolblock( igen, parts, self.ELSE.lineno, *args, **kwargs )
        return None

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'elseblock: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class ForBlock( NonTerminal ):
    """class to handle `elseblock` grammar."""

    def __init__( self, parser, for_, newlines, indent, script, dedent ):
        super().__init__( parser, for_, newlines, indent, script, dedent )
        self.FOR, self.NEWLINES, self.INDENT, self.script, self.DEDENT = \
                for_, newlines, indent, script, dedent
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        x = self.FOR, self.NEWLINES, self.INDENT, self.script, self.DEDENT
        return list( filter( None, x ))

    def generate( self, igen, *args, **kwargs ):
        line = 'for' + self.FOR.dump(None)[4:]
        self.NEWLINES.generate( igen, *args, **kwargs )
        parts = line, self.INDENT, self.script, self.DEDENT
        self.gencontrolblock( igen, parts, self.FOR.lineno, *args, **kwargs )
        return None

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'forblock: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


class WhileBlock( NonTerminal ):
    """class to handle `whileblock` grammar."""

    def __init__( self, parser, while_, newlines, indent, script, dedent ):
        super().__init__( parser, while_, newlines, indent, script, dedent )
        self.WHILE, self.NEWLINES, self.INDENT, self.script, self.DEDENT = \
                while_, newlines, indent, script, dedent
        # Set parent attribute for children, should be last statement !!
        self.setparent( self, self.children() )

    def children( self ):
        x = self.WHILE, self.NEWLINES, self.INDENT, self.script, self.DEDENT
        return list( filter( None, x ))

    def generate( self, igen, *args, **kwargs ):
        line = 'while' + self.WHILE.dump(None)[6:]
        self.NEWLINES.generate( igen, *args, **kwargs )
        parts = line, self.INDENT, self.script, self.DEDENT
        self.gencontrolblock( igen, parts, self.WHILE.lineno, *args, **kwargs )
        return None

    def show( self, buf=sys.stdout, offset=0, attrnames=False,
              showcoord=False ):
        lead = ' ' * offset
        buf.write( lead + 'whileblock: ' )
        if showcoord:
            buf.write( ' (at %s)' % self.coord )
        buf.write('\n')
        [x.show(buf, offset+2, attrnames, showcoord) for x in self.children()]


#-------------------------- AST Terminals -------------------------

class NEWLINES( Terminal ) : pass

class INDENT( Terminal ):
    def generate( self, igen, *args, **kwargs ):
        pass
    def dump( self, context ) :
        return ''

class DEDENT( Terminal ):
    def generate( self, igen, *args, **kwargs ):
        pass
    def dump( self, context ) :
        return ''

class TEXT( Terminal ): pass

class DOCTYPE( Terminal ) : pass
class BODY( Terminal ) : pass
class IMPORT( Terminal ) : pass
class IMPLEMENT( Terminal ) : pass
class INHERIT( Terminal ) : pass

class COMMENTLINE( Terminal ) : pass
class STATEMENT( Terminal ) : pass
class TAGBEGIN( Terminal ) : pass

class COMMENTOPEN( Terminal ) : pass
class COMMENTTEXT( Terminal ) : pass
class COMMENTCLOSE( Terminal ) : pass
class FILTEROPEN( Terminal ) : pass
class FILTERTEXT( Terminal ) : pass
class FILTERCLOSE( Terminal ) : pass

class IF( Terminal ) : pass
class ELIF( Terminal ) : pass
class ELSE( Terminal ) : pass
class FOR( Terminal ) : pass
class WHILE( Terminal ) : pass

class DECORATOR( Terminal ) : pass
class FUNCTION( Terminal ) : pass
class INTERFACE( Terminal ) : pass

#---- XXXXXXXXX To be deleted XXXXXXXXXXXXX

class TAGOPEN( Terminal ):
    def checkprune( self ):
        from  tayra.lexer import TTLLexer
        tagopen = self.terminal
        self.pruneouter = tagopen[1] == TTLLexer.prunews
        if self.pruneouter :
            self.terminal = tagopen[0] + tagopen[2:]
        return self.pruneouter, None

    def _tagname( self ):
        from  tayra.lexer import TTLLexer
        return self.terminal.rstrip( TTLLexer.ws ).lstrip( '<!' )

    tagname = property( lambda self : self._tagname() )

class TAGCLOSE( Terminal ) :
    def checkprune( self ):
        from  tayra.lexer import TTLLexer
        tagclose = self.terminal
        self.pruneinner = TTLLexer.prunews in tagclose
        self.pruneindent = TTLLexer.pruneindent in tagclose
        if self.pruneinner or self.pruneindent :
            self.terminal = re.sub( r'[!%]', '', tagclose )
        return self.pruneinner, self.pruneindent
