import re

from   tayra.ttl.lexer      import TTLLexer
import tayra.ttl.plugins.htmltags

atom = TTLLexer.atom
regexstring = re.compile( r"""("[^"]*")|('[^']*')""" )
def parsespecifiers( specifiers ) :
    first, rest = specifiers.split(' ', 1)
    idclass = first.split('.') if first[0] in ['#', '.']  else []
    id_ = idclass.pop(0) and (idclass and idclass[0] == '#')
    cls = idclass
