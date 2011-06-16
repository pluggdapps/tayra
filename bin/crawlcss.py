#! /usr/bin/env python

import sys, time
from   httplib2         import Http
from   os.path          import basename
import lxml.html        as lh
import urllib2          as u

# HTTP client
ht = Http()
sleeptime = 4
fetchcache = set()
recenthostname = 'deadmeat'

def fetchcss( baseurl, links ) :
    for l in links : 
        attrs = l.attrib
        href = attrs.get( 'href', None )
        type_ = attrs.get( 'type', None )
        if not href : continue
        if type_ != 'text/css' : continue
        print "(%s) CSS Fetching %s ..." % (time.time(), href)
        try :
            url = abshref( baseurl, href )
            hdrs, body = ht.request( url )
        except :
            print 'Request exception for %r ...' % url
            continue
        filename = basename( u.urlparse.urlparse(href).path )
        filename = filename+'.css' if '.css' not in filename else filename
        if ('<html' in body) or ('<HTML' in body) : continue
        open(filename, 'w').write(body)

def start( urls ) :
    global fetchcache, recenthostname
    if urls :
        baseurl, url = urls.pop(0)
        print 'Fetching %s ...' % url 
        try :
            if url.startswith( recenthostname ) :
                time.sleep(sleeptime)
            hdrs, html = ht.request( url )
            recenthostname = baseurl
        except :
            print 'Request exception for %r ...' % url
            return start( urls )

        fetchcache.add( url )
        try :
            root = lh.fromstring( html )
        except :
            print 'HTML parsing error for %r ...' % url
            return start( urls )

        links, anchors = root.xpath( '//link' ), root.xpath( '//a' )
        fetchcss( baseurl, links )
        for a in anchors :
            href = a.attrib.get( 'href', None )
            if not href : continue
            if '.jpg' in href or '.png' in href : continue
            href = abshref( baseurl, href )
            p = u.urlparse.urlparse( href )
            baseurl = '%s://%s' % (p.scheme, p.netloc)
            urls.append( (baseurl, href) )
        start( urls )

def main() :
    baseurl = 'http://100bestwebsites.org/'
    start( [ (baseurl, baseurl) ] )

def abshref( baseurl, link ) :
    x = u.urlparse.urljoin( baseurl, link )
    return x


if __name__ == '__main__' :
    main()
