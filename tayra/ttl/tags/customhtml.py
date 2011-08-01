from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

gsm = getGlobalSiteManager()

def handle_aname( tagopen, specifiers, style, attrs, tagfinish ):
    _id, classes, strings, atoms = parsespecifiers( specifiers )
    href = 'name=%s' % tokens.pop(0) if tokens else None
    specattrs = filter( None, [id_, classes, href] )
    return composetag( tagopen, specattrs, style, attrs, tagfinish )

def handle_aimg( tagopen, specifiers, style, attrs, tagfinish ):
    _id, classes, strings, atoms = parsespecifiers( specifiers )
    href = tokens.pop(0) if tokens else ''
    src  = tokens.pop(0) if tokens else ''
    id_ = 'id="%s"' % _id if _id else ''
    cls = 'class="%s"' % classes if classes else ''
    html = '<a href=%s><img %s %s style="%s" src=%s %s/></a>' % (
            href, id_, cls, style, src, ' '.join(attrs) )
    return html
