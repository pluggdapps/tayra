import re

import tayra.ttl.plugins.htmltags
from   tayra.ttl.lexer              import TTLLexer

atom = TTLLexer.atom
regexstring = re.compile( r"""("[^"]*")|('[^']*')""" )
def parsespecifiers( specifiers ) :
    try :
        first, rest = ' '.join( specifiers.splitlines() ).split(' ', 1)
    except :
        first, rest = specifiers, ''
    if first.startswith('#') :
        try :
            id_, classes = first.split('.', 1)
        except :
            id_, classes = first, ''
        classes = classes.replace('.', ' ')
    elif first.startswith('.') :
        id_, classes = '', first.replace('.', ' ').strip(' ')
    else :
        rest = ' '.join([first, rest ])
        id_ = classes = ''
    id_ = 'id="%s"' % id_ if id_ else id_
    classes = 'class="%s"' % classes if classes else classes
    
    # Parse tag-specifiers
    rest, tokens = rest.strip(' '), [ '' ]
    stringify = None
    for c in rest :
        if stringify :
            tokens[-1] += c
            if c == stringify :
                stringify = None
                tokens.append( '' )
        elif c == ' ' :
            tokens.append( '' )
        else :
            tokens[-1] += c
    return id_, classes, tokens

