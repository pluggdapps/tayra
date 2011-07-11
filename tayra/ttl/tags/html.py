from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.ttl.interfaces import ITayraTags
from   tayra.ttl.tags       import parsespecifiers, composetag, stdspecifiers

gsm = getGlobalSiteManager()

def handle_a( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    href = 'href=%s' % tokens.pop(0) if tokens else None
    specattrs = filter( None, [id_, classes, href] )
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_abbr( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    title = 'title=%s' % tokens.pop(0) if tokens else None
    specattrs = filter( None, [id_, classes, title] )
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_area( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    href = coords = ''
    for tok in tokens :
        try :
            x = int( tok.split(',', 1)[0].strip(' ') )
            coords = 'coords="%s"' % tok
            continue
        except :
            pass
        href = tok
    specattrs = filter( None, [id_, classes, href, coords] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_base( tagopen, specifiers, style, attrs, tagfinish ):
    """The base tag must be inside head element, and its `href` must be
    absolute uri. It does not support standard attributes
    """
    id_, classes, tokens = parsespecifiers( specifiers )
    href = 'href=%s' % tokens.pop(0) if tokens else ''
    specattrs = filter( None, [id_, classes, href] )
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_bdo( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    specattrs = filter( None, [id_, classes] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_blockquote( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    cite = 'cite=%s' % tokens.pop(0) if tokens else ''
    specattrs = filter( None, [id_, classes, cite] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

_button_type = [ 'button', 'reset', 'submit' ]
def handle_button( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    type_ = value = name = ''
    for tok in tokens :
        if tok in _button_type :
            type_ = 'type="%s"' % tok
            continue
        if (tok[0] + tok[-1]) in [ '""', "''" ] :
            value = 'value=%s' % tok
            continue
        name = 'name="%s"' % tok
    specattrs = filter( None, [id_, classes, type_, value, name] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

_align_col = [ 'left', 'right', 'center', 'justify', 'char' ]
_valign    = [ 'top', 'middle', 'bottom', 'baseline' ]
def _column( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    align = valign = span = width = ''
    for tok in tokens :
        if tok in _align_col :
            align = 'align="%s"' % tok
            continue
        if tok in _valign :
            valign = 'valign="%s"' % tok
            continue
        if tok.startswith('w:') :
            width = 'width="%s"' % tok.split(':', 1)[-1]
            continue
        try : span = 'span="%s"' % int(tok)
        except : pass
    specattrs = filter( None, [id_, classes, align, valign, span, width]
                ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_col( tagopen, specifiers, style, attrs, tagfinish ):
    _column( tagopen, specifiers, style, attrs, tagfinish )

def handle_colgroup( tagopen, specifiers, style, attrs, tagfinish ):
    _column( tagopen, specifiers, style, attrs, tagfinish )

def handle_del( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    cite = datetime = ''
    for tok in tokens :
        if tok.startswith('on:') :
            datetime = 'datetime="%s"' % tok.split(':', 1)[-1]
            continue
        cite = tok
    specattrs = filter( None, [id_, classes, cite, datetime] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_form( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    action = name = ''
    for tok in tokens :
        if (tok[0] + tok[-1]) in [ '""', "''" ] :
            action = 'action=%s' % tok
            continue
        name = 'name="%s"' % tok
    specattrs = filter( None, [id_, classes, action, name] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_head( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    profile = 'profile=%s' % tokens.pop(0) if tokens else ''
    specattrs = filter( None, [id_, classes, profile] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

_frameborder = [ '1', '0' ]
_scrolling   = [ 'yes', 'no', 'auto' ]
def handle_iframe( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    name = frameborder = scrolling = ''
    for tok in tokens :
        if tok in _frameborder :
            frameborder = 'frameborder="%s"' % tok
            continue
        if tok in _scrolling :
            scrolling = 'scrolling="%s"' % tok
            continue
        name = tok
    specattrs = filter( None, [id_, classes, name, frameborder, scrolling] 
                ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_img( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    src = 'src=%s' % tokens.pop(0) if tokens else ''
    specattrs = filter( None, [id_, classes, src] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

_input_type = [
    'button', 'checkbox', 'file', 'hidden', 'image', 'password', 'radio',
    'reset', 'submit', 'text'
]
def handle_input( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    type_ = 'type="%s"' % tokens.pop(0) if tokens else ''
    specattrs = filter( None, [id_, classes, type_] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_ins( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    cite = datetime = ''
    for tok in tokens :
        if tok.startswith('on:') :
            datetime = 'datetime="%s"' % tok.split(':', 1)[-1]
            continue
        cite = tok
    specattrs = filter( None, [id_, classes, cite, datetime] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_label( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    for_ = 'for="%s"' % tokens.pop(0) if tokens else ''
    specattrs = filter( None, [id_, classes, for_] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_link( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    link = 'link=%s' % tokens.pop(0) if tokens else ''
    specattrs = filter( None, [id_, classes, link] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_map( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    name = 'name="%s"' % tokens.pop(0) if tokens else ''
    specattrs = filter( None, [id_, classes, name] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_meta( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    name = content = ''
    for tok in tokens :
        if (tok[0] + tok[-1]) in [ '""', "''" ] :
            content = 'content="%s"' % tok
            continue
        name = 'name="%s"' % tok
    specattrs = filter( None, [id_, classes, name, content] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_optgroup( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    label = 'label="%s"' % tokens.pop(0) if tokens else ''
    specattrs = filter( None, [id_, classes, label] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_option( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    value = 'value="%s"' % tokens.pop(0) if tokens else ''
    specattrs = filter( None, [id_, classes, value] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_param( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    name = 'name="%s"' % tokens.pop(0) if tokens else ''
    value = 'value="%s"' % tokens.pop(0) if tokens else ''
    specattrs = filter( None, [id_, classes, name, value] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_q( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    cite = 'cite=%s' % tokens.pop(0) if tokens else ''
    specattrs = filter( None, [id_, classes, cite] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_select( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    size = name = ''
    for tok in tokens :
        try :
            size = 'size="%s"' % int(tok)
            continue
        except :
            pass
        name = 'name="%s"' % tok
    specattrs = filter( None, [id_, classes, size, name] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_textarea( tagopen, specifiers, style, attrs, tagfinish ):
    id_, classes, tokens = parsespecifiers( specifiers )
    tokens, specattrs = stdspecifiers( tokens )
    for tok in tokens :
        try :
            cols, rows = [ int(t) for t in tok.split(',') ]
            cols, rows = 'cols="%s"'%cols, 'rows="%s"'%rows
            continue
        except :
            pass
        name = 'name="%s"' % tok
    specattrs = filter( None, [id_, classes, cols, rows, name] ) + specattrs
    return composetag( tagopen, specattrs, style, attrs, tagfinish )



class Html( object ):
    implements( ITayraTags )
    def handlers( self ):
        g = globals()
        return dict([
            (fn[7:], val) for fn, val in g.items() if fn.startswith('handle_')
        ])

# Register this plugin
gsm.registerUtility( Html(), ITayraTags, 'html' )
