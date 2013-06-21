import imp
from   io                   import StringIO
from   pluggdapps.plugin    import Plugin, implements
from   tayra                import BaseTTLPlugin

def __traceback_decorator__( frames ):
    from copy    import deepcopy
    from os.path import basename

    def _map2ttl( frame ):
        filename = frame.filename
        lineno = frame.lineno
        lines = open(filename).readlines()[:lineno]
        lines.reverse()
        rc = {}
        for l in lines :
            if l.strip().startswith('# lineno') :
                _, ttl_lineno = l.split(':', 1)
                ttl_lineno = int( ttl_lineno )
                ttl_text = open( _ttlfile ).readlines()[ ttl_lineno-1 ]
                return ttl_lineno, ttl_text
        return None, None

    newframes = []
    for frame in frames :
        newframes.append( frame )
        frameadded = getattr( frame, '_ttlframeadded', False )

        basen = basename( frame.filename )
        if basen.endswith( '.ttl.py' )              and basen == (basename( _ttlfile ) + '.py')              and frameadded == False :
            newframe = deepcopy( frame )
            frame._ttlframeadded = True
            try :
                newframe.lineno, newframe.linetext = _map2ttl( newframe )
                if newframe.lineno :
                    newframe.filename = _ttlfile
                    newframes.append( newframe )
            except :
                raise
                continue
    return newframes


_context = globals()['_context']
blocks = _compiler.importlib(this, _context, '/home/pratap/dev/tayra/tayra/test/stdttl/element.ttl')

def body( *args, **kwargs ) :  
  _m.pushbuf()
  # lineno:8
  _m.pushbuf()
  _m.extend( ['<html>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  # lineno:9
  _m.pushbuf()
  _m.extend( ['<head .pluggdsite>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:10
  _m.pushbuf()
  _m.extend( ['<link image/ico "'] )
  _m.append(_m.evalexprs( '', 'favicon', '', globals(), locals()) )
  _m.extend( ['" rel="icon">'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:11
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'this.hd_title()', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:12
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'this.hd_meta()', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:13
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'this.hd_links()', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:14
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'this.hd_styles()', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:15
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'this.hd_script()', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:16
  _m.pushbuf()
  _m.extend( ['<body .pluggdsite>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:17
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'this.bd_header()', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:18
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'this.bd_body()', '', globals(), locals()) )
  _m.extend( ['\n    '] )
  # lineno:19
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'this.bd_footer()', '', globals(), locals()) )
  _m.extend( ['\n\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()

# ---- Global Functions
# lineno:4
favicon = 'static/paicon16x16.png'
# lineno:5
title = 'base-page'

_m.extend( ['\n\n'] )
# lineno:24
def hd_title() :  
  _m.pushbuf()
  # lineno:25
  _m.pushbuf()
  _m.extend( ['<title>'] )
  _m.pushbuf()
  # lineno:25
  _m.extend( [' '] )
  _m.append(_m.evalexprs( '', 'title', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()


# lineno:27
def hd_meta() :  
  _m.pushbuf()
  # lineno:28
  pass
  return _m.popbuftext()


# lineno:30
def hd_links() :  
  _m.pushbuf()
  # lineno:32
  fnt_amaranth = 'static/fonts/amaranth/Amaranth-webfont.woff'
  # lineno:33
  fnt_opensans = 'static/fonts/open_sans/OpenSans-Regular-webfont.woff'
  _m.extend( ['\n  '] )
  # lineno:35
  _m.pushbuf()
  _m.extend( ['<style text/css>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:36
  _m.extend( ['@font-face {', '\n      '] )
  # lineno:37
  _m.extend( ["font-family: 'Amaranth';", '\n      '] )
  # lineno:38
  _m.extend( ['font-style: normal;', '\n      '] )
  # lineno:39
  _m.extend( ['font-weight: normal;', '\n      '] )
  # lineno:40
  _m.extend( ["src: local('Amaranth'), url('"] )
  _m.append(_m.evalexprs( '', 'fnt_amaranth', '', globals(), locals()) )
  _m.extend( ["') format('woff');", '\n    '] )
  # lineno:41
  _m.extend( ['}', '\n    '] )
  # lineno:42
  _m.extend( ['@font-face {', '\n      '] )
  # lineno:43
  _m.extend( ["font-family: 'Open Sans';", '\n      '] )
  # lineno:44
  _m.extend( ['font-style: normal;', '\n      '] )
  # lineno:45
  _m.extend( ['font-weight: normal;', '\n      '] )
  # lineno:46
  _m.extend( ["src: local('Open Sans'), url('"] )
  _m.append(_m.evalexprs( '', 'fnt_opensans', '', globals(), locals()) )
  _m.extend( ["') format('woff');", '\n    '] )
  # lineno:47
  _m.extend( ['}', '\n\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:49
  defaultcss = 'static/default.css'
  # lineno:50
  _m.pushbuf()
  _m.extend( ['<link text/css "'] )
  _m.append(_m.evalexprs( '', 'defaultcss', '', globals(), locals()) )
  _m.extend( ['" rel="stylesheet" charset="utf-8">'] )
  _m.pushbuf()
  _m.extend( ['\n    \n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()


# lineno:52
def hd_styles() :  
  _m.pushbuf()
  # lineno:53
  pass
  return _m.popbuftext()


# lineno:55
def hd_script() :  
  _m.pushbuf()
  # lineno:56
  jqueryfile = 'static/jquery-1.5.1.min.js'
  # lineno:57
  jqlibfile = 'static/jqlib.js'
  # lineno:58
  _m.pushbuf()
  _m.extend( ['<script text/javascript "'] )
  _m.append(_m.evalexprs( '', 'jqueryfile', '', globals(), locals()) )
  _m.extend( ['">'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:59
  _m.pushbuf()
  _m.extend( ['<script text/javascript "'] )
  _m.append(_m.evalexprs( '', 'jqlibfile', '', globals(), locals()) )
  _m.extend( ['">'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:60
  _m.pushbuf()
  _m.extend( ['<script type="text/javascript">'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:61
  _m.extend( ['var _gaq = _gaq || [];', '\n    '] )
  # lineno:62
  _m.extend( ["_gaq.push(['_setAccount', 'UA-26824958-1']);", '\n    '] )
  # lineno:63
  _m.extend( ["_gaq.push(['_setDomainName', 'pluggdapps.com']);", '\n    '] )
  # lineno:64
  _m.extend( ["_gaq.push(['_trackPageview']);", '\n    '] )
  # lineno:65
  _m.extend( ['(function() {', '\n      '] )
  # lineno:66
  _m.extend( ["var ga = document.createElement('script');", '\n      '] )
  # lineno:67
  _m.extend( ["ga.type = 'text/javascript'; ga.async = true;", '\n      '] )
  # lineno:68
  _m.extend( ["ga.src = ('https:' == document.location.protocol ?", '\n                  '] )
  # lineno:69
  _m.extend( ["'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';", '\n      '] )
  # lineno:70
  _m.extend( ["var s = document.getElementsByTagName('script')[0];", '\n      '] )
  # lineno:71
  _m.extend( ['s.parentNode.insertBefore(ga, s);', '\n    '] )
  # lineno:72
  _m.extend( ['})();', '\n\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()


# lineno:77
def bd_header() :  
  _m.pushbuf()
  # lineno:78
  pass
  return _m.popbuftext()


# lineno:80
def bd_body() :  
  _m.pushbuf()
  # lineno:81
  _m.pushbuf()
  _m.extend( ['<div #right>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:82
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'this.body_rightpane()', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:83
  _m.pushbuf()
  _m.extend( ['<div #left>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:84
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'this.body_leftpane()', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:85
  _m.pushbuf()
  _m.extend( ['<div #center>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:86
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'this.body_centerpane()', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()


# lineno:88
def body_leftpane() :  
  _m.pushbuf()
  # lineno:89
  _m.pushbuf()
  _m.extend( ['<div .ralign.leftpane>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:90
  _m.pushbuf()
  _m.extend( ['<ul>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:91
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:92
  _m.pushbuf()
  _m.extend( ['<a "/index">'] )
  _m.pushbuf()
  # lineno:92
  _m.extend( [' home', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:93
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:94
  _m.pushbuf()
  _m.extend( ['<a "/overview">'] )
  _m.pushbuf()
  # lineno:94
  _m.extend( [' bootstrap', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:95
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:96
  _m.pushbuf()
  _m.extend( ['<a "/ispecroot">'] )
  _m.pushbuf()
  # lineno:96
  _m.extend( [' Interface Specification Request', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:97
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:98
  _m.pushbuf()
  _m.extend( ['<a "/config">'] )
  _m.pushbuf()
  # lineno:98
  _m.extend( [' Configuration', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:99
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:100
  _m.pushbuf()
  _m.extend( ['<a "/psite_getstarted">'] )
  _m.pushbuf()
  # lineno:100
  _m.extend( [' Get Started', '\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()


# lineno:102
def body_centerpane() :  
  _m.pushbuf()
  # lineno:103
  pass
  return _m.popbuftext()


# lineno:105
def body_rightpane() :  
  _m.pushbuf()
  # lineno:106
  _m.pushbuf()
  _m.extend( ['<nav {font-size : x-large}>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:107
  _m.pushbuf()
  _m.extend( ['<a .fntbold "/googlegroup">'] )
  _m.pushbuf()
  # lineno:107
  _m.extend( [' Join', '\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:108
  _m.pushbuf()
  _m.extend( ['<br/>'] )
  _m.pushbuf()
  _m.extend( ['\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:109
  _m.pushbuf()
  _m.extend( ['<div .builton>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:110
  _m.pushbuf()
  _m.extend( ['<b>'] )
  _m.pushbuf()
  # lineno:110
  _m.extend( [' built-on ', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:111
  _m.pushbuf()
  _m.extend( ['<ul>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:112
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:113
  _m.pushbuf()
  _m.extend( ['<a "http://whatwg.org">'] )
  _m.pushbuf()
  # lineno:113
  _m.extend( [' HTML5', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:114
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:115
  _m.pushbuf()
  _m.extend( ['<a "http://python.org">'] )
  _m.pushbuf()
  # lineno:115
  _m.extend( [' python', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:116
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:117
  _m.pushbuf()
  _m.extend( ['<a "https://developer.mozilla.org/en/JavaScript_Language_Resources">'] )
  _m.pushbuf()
  # lineno:117
  _m.extend( [' JavaScript', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:118
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:119
  _m.pushbuf()
  _m.extend( ['<a "http://erlang.org">'] )
  _m.pushbuf()
  # lineno:119
  _m.extend( [' Erlang', '\n\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:121
  _m.pushbuf()
  _m.extend( ['<div .builtwith>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:122
  _m.pushbuf()
  _m.extend( ['<b>'] )
  _m.pushbuf()
  # lineno:122
  _m.extend( [' built-with ', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:123
  _m.pushbuf()
  _m.extend( ['<ul>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:124
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:125
  _m.pushbuf()
  _m.extend( ['<a "http://pylonsproject.com">'] )
  _m.pushbuf()
  # lineno:125
  _m.extend( [' Pyramid', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:126
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:127
  _m.pushbuf()
  _m.extend( ['<a "http://eazytext.pluggdapps.com">'] )
  _m.pushbuf()
  # lineno:127
  _m.extend( [' EazyText', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:128
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:129
  _m.pushbuf()
  _m.extend( ['<a "http://tayra.pluggdapps.com">'] )
  _m.pushbuf()
  # lineno:129
  _m.extend( [' Tayra', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:130
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:131
  _m.pushbuf()
  _m.extend( ['<a "http://couchdb.org">'] )
  _m.pushbuf()
  # lineno:131
  _m.extend( [' CouchDB', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:132
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:133
  _m.pushbuf()
  _m.extend( ['<a "http://couchpy.pluggdapps.com">'] )
  _m.pushbuf()
  # lineno:133
  _m.extend( [' CouchPy', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:134
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:135
  _m.pushbuf()
  _m.extend( ['<a "http://jquery.com/">'] )
  _m.pushbuf()
  # lineno:135
  _m.extend( [' jQuery', '\n\n  '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:137
  _m.pushbuf()
  _m.extend( ['<div .builtfor>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:138
  _m.pushbuf()
  _m.extend( ['<b>'] )
  _m.pushbuf()
  # lineno:138
  _m.extend( [' built-for ', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:139
  _m.pushbuf()
  _m.extend( ['<ul>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:140
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:141
  _m.pushbuf()
  _m.extend( ['<a "http://pluggdapps.com">'] )
  _m.pushbuf()
  # lineno:141
  _m.extend( [' pluggdapps.com', '\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()


# lineno:143
def bd_footer() :  
  _m.pushbuf()
  # lineno:144
  _m.pushbuf()
  _m.extend( ['<table #footer>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:145
  _m.pushbuf()
  _m.extend( ['<tr>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:146
  _m.pushbuf()
  _m.extend( ['<td .copyright>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:147
  _m.extend( ['An SKR Farms Initiative.', '\n        '] )
  # lineno:148
  _m.pushbuf()
  _m.extend( ['<br/>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:149
  _m.extend( ['Website content copyright © by SKR Farms. All rights reserved.', '\n        '] )
  # lineno:150
  _m.extend( ['Pluggdapps and its documentation are licensed under "GPL Version-3".', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  # lineno:151
  _m.pushbuf()
  _m.extend( ['<td .papowered>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:152
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'blocks.papowered( 100, 10 )', '', globals(), locals()) )
  _m.extend( ['\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), **{'nl': '', 'oprune': False, 'indent': False, 'iprune': False} )
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
