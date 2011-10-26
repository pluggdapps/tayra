# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

import re

dtdurls = {
  "html4.01transitional"    : \
        ( "HTML", '"-//W3C//DTD HTML 4.01 Transitional//EN"',
          '"http://www.w3.org/TR/html4/loose.dtd">',
        ),
  "html4.01strict"          : \
        ( "HTML", '"-//W3C//DTD HTML 4.01//EN"',
          '"http://www.w3.org/TR/html4/strict.dtd">'
        ),
  "html4.01frameset"        : \
        ( "HTML", '"-//W3C//DTD HTML 4.01 Frameset//EN"',
          '"http://www.w3.org/TR/html4/frameset.dtd">'
        ),
  "xhtml1.0transitional"    : \
        ( "html", '"-//W3C//DTD XHTML 1.0 Transitional//EN"',
          '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
        ),
  "xhtml1.0strict"          : \
        ( "html", '"-//W3C//DTD XHTML 1.0 Strict//EN"',
          '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
        ),
  "xhtml1.0frameset"        : \
        ( "html", '"-//W3C//DTD XHTML 1.0 Frameset//EN"',
          '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">'
        ),
  "xhtml1.1"                : \
        ( "html", '"-//W3C//DTD XHTML 1.1//EN"',
          '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
        ),
  "xhtml1.1basic"           : \
        ( "html", '"-//W3C//DTD XHTML Basic 1.1//EN"',
          '"http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">'
        ),
  "xhtml1.1mobile"          : \
        ( "html", '"-//WAPFORUM//DTD XHTML Mobile 1.2//EN"',
          '"http://www.openmobilealliance.org/tech/DTD/xhtml-mobile12.dtd">'
        ),
  "xhtml+rdfa1.0"           : \
        ( "html", '"-//W3C//DTD XHTML+RDFa 1.0//EN"',
          '"http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd">'
        ),
}

def ttl2doctype( doctype ) :
    doctype = u' '.join( doctype.splitlines() ).rstrip(' ')
    values = [ w for w in re.split(r'[ \t]', doctype[3:-1]) if w ]
    doc = values.pop(0) if values else u''
    ver = values.pop(0) if values else u''
    level = values.pop(0) if values else u''
    key = doc+ver+level
    if key in dtdurls :
        html = "<!DOCTYPE %s PUBLIC %s %s" % dtdurls[key]
    elif doc == 'xml' :
        html = "<?xml " + ("version=%r " % ver) + ("encoding=%r " % level)+"?>"
    else :
        html = "<!DOCTYPE html>"    # html5
    return html
