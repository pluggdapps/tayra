from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.ttl.interfaces import ITayraTags
from   tayra.ttl.tags       import parsespecifiers, composetag

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


class CustomHtml( object ):
    implements( ITayraTags )
    def handlers( self ):
        g = globals()
        return dict([
            (fn[7:], val) for fn, val in g.items() if fn.startswith('handle_')
        ])


# Register this plugin
gsm.registerUtility( CustomHtml(), ITayraTags, 'customhtml' )
