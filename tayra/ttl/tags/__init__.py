import re
from   copy         import deepcopy

ws = r'[ \r\n\t]*'
parseexp = re.compile(
    r'(\'[^\']+\'%s)|(\"[^"]+\"%s)|([^" \t\r\n\']+%s)' % (ws,ws,ws)
)
def parsespecifiers( specifiers ) :
    parsed = parseexp.findall( specifiers )
    idclass = parsed and parsed[0][-1]
    if idclass and idclass[0] == '#' :
        parts = idclass.split('.')
        if len(parts) > 1 :
            id_, classes = parts[0], ' '.join( parts[1:] )
        else :
            id_, classes = parts[0], ''
        parsed.pop(0)
    elif idclass and idclass[0] == '.' :
        id_, classes = '', idclass[1:].replace('.', ' ')
        parsed.pop(0)
    else :
        id_ = classes = None

    if parsed :
        strings = filter( None, reduce( lambda x, t : x + list(t[:2]), parsed, [] ))
        atoms   = filter( None, map( lambda t : t[2], parsed ))
    else :
        strings = []
        atoms   = []
    id_ = 'id="%s"' % id_ if id_ else None
    classes = 'class="%s"' % classes if classes else None
    return id_, classes, strings, atoms

atom2attr = {
  # global attributes
  'edit'         : 'contenteditable="true"',
  'noedit'       : 'contenteditable="false"',
  'dragcopy'     : 'draggable="true" dragzone="copy"',
  'dragmove'     : 'draggable="true" dragzone="move"',
  'draglink'     : 'draggable="true" dragzone="link"',
  'nodrag'       : 'draggable="false"',
  'hidden'       : 'hidden',
  'spellcheck'   : 'spellcheck="true',
  'nospellcheck' : 'spellcheck="false',
  # encoding type
  'application/x-www-form-urlencoded': 'enctype="application/x-www-form-urlencoded"',
  'multipart/form-data': 'enctype="multipart/form-data"',
  'text/plain': 'enctype="text/plain"',
  # shape
  'default' : 'shape="default"',
  'rect'    : 'shape="rect"',
  'circle'  : 'shape="circle"',
  'poly'    : 'shape="poly"',
  # dir
  'ltr'     : 'shape="ltr"',
  'rtl'     : 'shape="rtl"',
  # target
  '_blank'  : 'target="_blank"',
  '_self'   : 'target="_self"',
  '_parent' : 'target="_parent"',
  '_top'    : 'target="_top"',
  # method
  'get'     : 'method="get"',
  'post'    : 'method="post"',
  # atoms
  'disabled': 'disabled="disabled"',
  'checked' : 'checked="checked"',
  'readonly': 'readonly="readonly"',
  'selected': 'selected="selected"',
  'multiple': 'multiple="multiple"',
  'defer'   : 'defer="defer"',
}

def atoms2attrs( spectokens ):
    leftover, attrs = [], []
    for token in spectokens :
        if token.startswith( 'key:' ):
            attr = 'accesskey="%s"' % token.split(':', 1)[1]
        if token.startswith( 'tab:' ):
            attr = 'tabindex="%s"' % token.split(':', 1)[1]
        else :
            attr = atom2attr.get( token, None )
        attrs.append( attr ) if attr != None else leftover.append( token )
    return filter(None, leftover), attrs

def composetag( tagopen, specattrs, style, attrs, tagfinish ):
    tagopen = tagopen.rstrip(' ')
    style = 'style="%s"' % style.strip(' ') if style else style
    specattrs = ' '.join( specattrs )
    attrs = ' '.join( attrs )
    cont = ' '.join( filter( None, [ tagopen, specattrs, style, attrs ]) )
    return cont + tagfinish

def handle_default( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, _s, _a = parsespecifiers( specifiers )
    return composetag(
        tagopen, filter(None, [id_, classes]), style, attrs, tagfinish
    )
