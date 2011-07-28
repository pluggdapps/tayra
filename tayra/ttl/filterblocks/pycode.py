from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.ttl.interfaces     import  ITayraFilterBlock

gsm = getGlobalSiteManager()

class PyCode( object ):
    implements( ITayraFilterBlock )

    def __init__( self, *args, **kwargs ):
        if args :
            self.filteropen, self.filtertext, self.filterclose = args

    def __call__( self, filteropen, filtertext, filterclose ):
        return PyCode( filteropen, filtertext, filterclose )

    def headpass1( self, igen ):                        # Global
        lines = self.filtertext.splitlines()
        # Signature
        self.signature = lines.pop(0) if lines else None
        self.tokens = tokens = self.signature.strip().split(' ')
        # Align indentation
        striplen = ( len(lines[0]) - len(lines[0].lstrip(' \t')) ) if lines else 0
        if tokens and tokens[0] == 'global' :
            lines = [ line[striplen:] for line in lines ]
            [ igen.putstatement( line ) for line in lines ]
            self.lines = []
        else :
            self.lines = [ line[striplen:] for line in lines ]

    def headpass2( self, igen ):
        pass

    def generate( self, igen, *args, **kwargs ):        # Inline
        lines = self.lines
        [ igen.putstatement( line ) for line in lines ]

    def tailpass( self, igen ):
        pass

# Register this plugin
gsm.registerUtility( PyCode(), ITayraFilterBlock, 'pycode' )
