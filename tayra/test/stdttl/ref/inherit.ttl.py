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


_m.inherit( 'tayra:test/stdttl/base.ttl', globals() )

def body( *args, **kwargs ) :  
  _m.pushbuf()
  _m.extend( ["<!-- \nThis file is subject to the terms and conditions defined in\nfile 'LICENSE', which is part of this source code package.\n      Copyright (c) 2011 SKR Farms (P) LTD.\n-->\n\n"] )
  # lineno:9
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'parent.body()', '', globals(), locals()) )
  _m.extend( ['\n\n'] )
  return _m.popbuftext()

# ---- Global Functions

# lineno:11
def hd_styles() :  
  _m.pushbuf()
  # lineno:12
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'parent.hd_styles()', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  # lineno:13
  _m.pushbuf()
  _m.extend( ['<style text/css>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:14
  _m.extend( ['div.features {', '\n      '] )
  # lineno:15
  _m.extend( ['margin : 0px 5px;', '\n    '] )
  # lineno:16
  _m.extend( ['}', '\n    '] )
  # lineno:17
  _m.extend( ['div.features p.title {', '\n      '] )
  # lineno:18
  _m.extend( ['font-family : Amaranth, arial;', '\n      '] )
  # lineno:19
  _m.extend( ['font-size : large;', '\n    '] )
  # lineno:20
  _m.extend( ['}', '\n    '] )
  # lineno:21
  _m.extend( ['div.features input[type="text"] {', '\n      '] )
  # lineno:22
  _m.extend( ['margin : 10px 0px 0px 0px;', '\n      '] )
  # lineno:23
  _m.extend( ['background-color : #444;', '\n      '] )
  # lineno:24
  _m.extend( ['border : 1px solid gray;', '\n      '] )
  # lineno:25
  _m.extend( ['width : 40%;', '\n      '] )
  # lineno:26
  _m.extend( ['color : white;', '\n    '] )
  # lineno:27
  _m.extend( ['}', '\n    '] )
  # lineno:28
  _m.extend( ['div.features fieldset {', '\n      '] )
  # lineno:29
  _m.extend( ['padding : 0px 3px 5px 3px;', '\n      '] )
  # lineno:30
  _m.extend( ['margin : 0px 5px;', '\n      '] )
  # lineno:31
  _m.extend( ['width : 45%;', '\n      '] )
  # lineno:32
  _m.extend( ['border : 1px solid gray;', '\n    '] )
  # lineno:33
  _m.extend( ['}', '\n    '] )
  # lineno:34
  _m.extend( ['div.features fieldset legend {', '\n      '] )
  # lineno:35
  _m.extend( ['font-weight : bold;', '\n      '] )
  # lineno:36
  _m.extend( ['font-family : Amaranth, arial;', '\n    '] )
  # lineno:37
  _m.extend( ['}', '\n    '] )
  # lineno:38
  _m.extend( ['div.features fieldset div.keywords {', '\n      '] )
  # lineno:39
  _m.extend( ['text-align : center;', '\n    '] )
  # lineno:40
  _m.extend( ['}', '\n    '] )
  # lineno:41
  _m.extend( ['div.search {', '\n      '] )
  # lineno:42
  _m.extend( ['height : 5em;', '\n    '] )
  # lineno:43
  _m.extend( ['}', '\n    '] )
  # lineno:44
  _m.extend( ['div.features ul {', '\n      '] )
  # lineno:45
  _m.extend( ['list-style : none; ', '\n      '] )
  # lineno:46
  _m.extend( ['padding : 0px;', '\n      '] )
  # lineno:47
  _m.extend( ['margin : 0px;', '\n    '] )
  # lineno:48
  _m.extend( ['}', '\n    '] )
  # lineno:49
  _m.extend( ['div.features ul li {', '\n      '] )
  # lineno:50
  _m.extend( ['border-left : 1px solid crimson;', '\n      '] )
  # lineno:51
  _m.extend( ['margin : 5px 0px;', '\n      '] )
  # lineno:52
  _m.extend( ['background-color : #444;', '\n      '] )
  # lineno:53
  _m.extend( ['padding : 3px;', '\n      '] )
  # lineno:54
  _m.extend( ['padding-left : 5px;', '\n      '] )
  # lineno:55
  _m.extend( ['font-weight : bold;', '\n      '] )
  # lineno:56
  _m.extend( ['border-top : 1px solid #444;', '\n    '] )
  # lineno:57
  _m.extend( ['}', '\n    '] )
  # lineno:58
  _m.extend( ['div.features ul li:hover {', '\n      '] )
  # lineno:59
  _m.extend( ['background-color : #999;', '\n      '] )
  # lineno:60
  _m.extend( ['border-top : 1px solid #DDD;', '\n      '] )
  # lineno:61
  _m.extend( ['color : black;', '\n      '] )
  # lineno:62
  _m.extend( ['text-shadow : 0px 1px 1px #FFF, 0px 1px 1px black;', '\n      '] )
  # lineno:63
  _m.extend( ['-moz-text-shadow : 0px 1px 1px #FFF, 0px 1px 1px black;', '\n      '] )
  # lineno:64
  _m.extend( ['-webkit-text-shadow : 0px 1px 1px #FFF, 0px 1px 1px black;', '\n    '] )
  # lineno:65
  _m.extend( ['}', '\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()


# lineno:67
def hd_script() :  
  _m.pushbuf()
  # lineno:68
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'parent.hd_script()', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  # lineno:69
  _m.pushbuf()
  _m.extend( ['<script text/javascript>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:70
  _m.extend( ['var speed = 200;', '\n    '] )
  # lineno:71
  _m.extend( ['$(document).ready( function() {', '\n      '] )
  # lineno:72
  _m.extend( ['// Search', '\n      '] )
  # lineno:73
  _m.extend( ["$('input.search').keydown( function(e) {", '\n        '] )
  # lineno:74
  _m.extend( ['var patt = new RegExp( $(\'input.search\').val(), "i" );', '\n        '] )
  # lineno:75
  _m.extend( ["$('div.features li').each( function(index, n) {", '\n          '] )
  # lineno:76
  _m.extend( ['patt.test( $(n).text() ) ? $(n).fadeIn(speed) : $(n).fadeOut(speed);', '\n        '] )
  # lineno:77
  _m.extend( ['})', '\n      '] )
  # lineno:78
  _m.extend( ['});', '\n      '] )
  # lineno:79
  _m.extend( ['// Showall', '\n      '] )
  # lineno:80
  _m.extend( ["$('.showall').click( function(e) {", '\n        '] )
  # lineno:81
  _m.extend( ["$('div.features li').each( function(index, n) { $(n).fadeIn(speed); } )", '\n      '] )
  # lineno:82
  _m.extend( ['});', '\n      '] )
  # lineno:83
  _m.extend( ['// Direct search', '\n      '] )
  # lineno:84
  _m.extend( ["$('.dsrch').click( function(e) {", '\n        '] )
  # lineno:85
  _m.extend( ['var patt = new RegExp( $(this).text(), "i" );', '\n        '] )
  # lineno:86
  _m.extend( ['console.log( $(this).text() );', '\n        '] )
  # lineno:87
  _m.extend( ["$('div.features li').each( function(index, n) {", '\n          '] )
  # lineno:88
  _m.extend( ['patt.test( $(n).text() ) ? $(n).fadeIn(speed) : $(n).fadeOut(speed);', '\n        '] )
  # lineno:89
  _m.extend( ['})', '\n      '] )
  # lineno:90
  _m.extend( ['});', '\n    '] )
  # lineno:91
  _m.extend( ['});', '\n\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()


# lineno:93
def body_centerpane() :  
  _m.pushbuf()
  # lineno:94
  _m.extend( [''] )
  _m.append(_m.evalexprs( '', 'parent.body_centerpane()', '', globals(), locals()) )
  _m.extend( ['\n  '] )
  # lineno:95
  _m.pushbuf()
  _m.extend( ['<div .features>'] )
  _m.pushbuf()
  _m.extend( ['\n    '] )
  # lineno:96
  _m.pushbuf()
  _m.extend( ['<p .title>'] )
  _m.pushbuf()
  # lineno:96
  _m.extend( [' Pluggdapps in a nutshell, that it is today and that it will be', '\n      '] )
  # lineno:97
  _m.extend( ['tomorrow.', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:98
  _m.pushbuf()
  _m.extend( ['<div .search>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:99
  _m.pushbuf()
  _m.extend( ['<inptext .search placeholder="Search features ...">'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:100
  _m.pushbuf()
  _m.extend( ['<a .showall.fntxsmall.pointer>'] )
  _m.pushbuf()
  # lineno:100
  _m.extend( [' show-all', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:101
  _m.pushbuf()
  _m.extend( ['<fieldset .floatr>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:102
  _m.pushbuf()
  _m.extend( ['<legend>'] )
  _m.pushbuf()
  # lineno:102
  _m.extend( [' Common search terms', '\n        '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:103
  _m.pushbuf()
  _m.extend( ['<div .keywords>'] )
  _m.pushbuf()
  _m.extend( ['\n          '] )
  # lineno:104
  _m.pushbuf()
  _m.extend( ['<span .dsrch.pointer.ralign>'] )
  _m.pushbuf()
  # lineno:104
  _m.extend( ['plugin', '\n          '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:105
  _m.pushbuf()
  _m.extend( ['<span .dsrch.pointer.ralign>'] )
  _m.pushbuf()
  # lineno:105
  _m.extend( ['template', '\n          '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:106
  _m.pushbuf()
  _m.extend( ['<span .dsrch.pointer.ralign>'] )
  _m.pushbuf()
  # lineno:106
  _m.extend( ['web|html', '\n          '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:107
  _m.pushbuf()
  _m.extend( ['<span .dsrch.pointer.ralign>'] )
  _m.pushbuf()
  # lineno:107
  _m.extend( ['couch', '\n          '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:108
  _m.pushbuf()
  _m.extend( ['<span .dsrch.pointer.ralign>'] )
  _m.pushbuf()
  # lineno:108
  _m.extend( ['tayra', '\n          '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:109
  _m.pushbuf()
  _m.extend( ['<span .dsrch.pointer.ralign>'] )
  _m.pushbuf()
  # lineno:109
  _m.extend( ['program', '\n    '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:110
  _m.pushbuf()
  _m.extend( ['<ul>'] )
  _m.pushbuf()
  _m.extend( ['\n      '] )
  # lineno:111
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:111
  _m.extend( ['Build applications on web-technologies. Build it on pluggdapps.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:112
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:112
  _m.extend( ['Linus took unix to all programmers, and apt-get took Linux to all people.', '\n        '] )
  # lineno:113
  _m.extend( ['In pluggdapps, deploy a website by installing a package.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:114
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:114
  _m.extend( ['Not just websites, whether it is an application or web-application, libraries', '\n        '] )
  # lineno:115
  _m.extend( ['or plugins or just couple of template files, deploy them by installing an egg', '\n        '] )
  # lineno:116
  _m.extend( ['package.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:117
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:117
  _m.extend( ['MVC (Model-View-Controller) is great. Plugin architecture is great. Do them', '\n        '] )
  # lineno:118
  _m.extend( ['both in pluggdapps and get the best of both worlds.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:119
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:119
  _m.extend( ['Should client and server run on different machines ? Not with pluggdapps.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:120
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:120
  _m.extend( ['Pluggdapps run on python and javascript and web-browser and uses erlang for', '\n        '] )
  # lineno:121
  _m.extend( ['database, hence, it can run on any device supporting them. Why not ?', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:122
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:122
  _m.extend( ['Library is a tool. Great libraries are stateless and re-entrant. For', '\n        '] )
  # lineno:123
  _m.extend( ['pluggdapps, even applications are stateless and re-entrant.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:124
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:124
  _m.extend( ['A framework is just a library, with callback APIs. A plugin is just a library,', '\n        '] )
  # lineno:125
  _m.extend( ['with callback APIs. Hence, plugins are great way to design frameworks.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:126
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:126
  _m.extend( ['To access a library, import them. To access plugins, query for them.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:127
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:127
  _m.extend( ['Pluggdapps is not first to do it right, it merely tracks the footsteps of', '\n        '] )
  # lineno:128
  _m.extend( ['its masters - Python, Zope, Pyramid, ...', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:129
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:129
  _m.extend( ['Interface will specify attributes, methods, method-signature and its function.', '\n        '] )
  # lineno:130
  _m.extend( ['A callback API is nothing but an interface, hence, plugins are nothing but', '\n        '] )
  # lineno:131
  _m.extend( ['a bunch of code implementing an interface. That pretty much sums up the', '\n        '] )
  # lineno:132
  _m.extend( ['plugin architecture.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:133
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:133
  _m.extend( ['Install applications and access them on the url.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:134
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:134
  _m.extend( ['Configure and customize application along with modules, interfaces and plugins', '\n        '] )
  # lineno:135
  _m.extend( ['used by the application. Configure them in .ini file, configure them via web.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:136
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:136
  _m.extend( ['Applications are mounted on the url in three ways - domain, subdomain and', '\n        '] )
  # lineno:137
  _m.extend( ['script. While the default is script, choose the one that fits, and', '\n        '] )
  # lineno:138
  _m.extend( ['applications can be agnostic to how they are mounted.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:139
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:139
  _m.extend( ['Url-rewriting. Requests are automatically routed to the mounted', '\n        '] )
  # lineno:140
  _m.extend( ['application.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:141
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:141
  _m.extend( ['Cross application access. For apps to access each other in the same run-time.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:142
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:142
  _m.extend( ['Scaffolding. From first key-stroke to first application page in less than', '\n        '] )
  # lineno:143
  _m.extend( ['30 seconds.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:144
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:144
  _m.extend( ['Authenticate users and authorize them with permissions. Off-the-shelf plugins', '\n        '] )
  # lineno:145
  _m.extend( ['available for challenging credentials and interfacing with backend store.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:146
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:146
  _m.extend( ['Your browser has got the best documentation engine ever and wiki makes it', '\n        '] )
  # lineno:147
  _m.extend( ['accessible. Use EazyText to create content for your apps.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:148
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:148
  _m.extend( ['EazyText wiki markup. Generate HTML documents with out compromising on its', '\n        '] )
  # lineno:149
  _m.extend( ['readability.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:150
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:150
  _m.extend( ['With EazyText highlight your text as bold, italic, underline, subscript,', '\n        '] )
  # lineno:151
  _m.extend( ['superscript and more.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:152
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:152
  _m.extend( ['EazyText can hyperlink documents and images.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:153
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:153
  _m.extend( ['Text in EazyText looks natural for reading. All the same it can generate', '\n        '] )
  # lineno:154
  _m.extend( ['lists, tables, definitions, blockquotes and paragraphs.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:155
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:155
  _m.extend( ['EazyText macros, create new functions and use them in your documents.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:156
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:156
  _m.extend( ['EazyText extensions, extend the wiki engine.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:157
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:157
  _m.extend( ['Become an expert in EazyText and create interactive documents.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:158
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:158
  _m.extend( ['And EazyText is moving towards HTML5.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:159
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:159
  _m.extend( ['With CSS and javascript, your browser can be way more than just a document', '\n        '] )
  # lineno:160
  _m.extend( ['renderer. Use tayra templates to design your front end.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:161
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:161
  _m.extend( ['HTML is verbose. Make it consise with Tayra.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:162
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:162
  _m.extend( ['CSS Selector. That which pulls HTML, Javascript and CSS together.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:163
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:163
  _m.extend( ['Tayra templating language. Bunch of syntax wrapped around a bunch of', '\n        '] )
  # lineno:164
  _m.extend( ['specification. Adapt the language to your needs.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:165
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:165
  _m.extend( ['Intendations are only natural to html. Why not enforce them ?', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:166
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:166
  _m.extend( ['Tayra templates. Define templates as function.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:167
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:167
  _m.extend( ['Tayra templates. Organise template functions as modules. Import them in other', '\n        '] )
  # lineno:168
  _m.extend( ['templates.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:169
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:169
  _m.extend( ['Tayra templates. Templates are modules. Templates are objects. Use template', '\n        '] )
  # lineno:170
  _m.extend( ['inheritance to design layouts.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:171
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:171
  _m.extend( ['Tayra templates. Specify template interface. Implement template plugins. Use', '\n        '] )
  # lineno:172
  _m.extend( ['them else-where.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:173
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:173
  _m.extend( ['If you like decorators in python, you will like it in Tayra templates.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:174
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:174
  _m.extend( ['NoSQL is cool. CouchDB is radical. Program your database with CouchPy.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:175
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:175
  _m.extend( ["Don't you feel stored procedure in SQL as an after-thought ? After programming", '\n        '] )
  # lineno:176
  _m.extend( ['(views,...) in CouchDB, there is a high chance you might.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:177
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:177
  _m.extend( ['CouchDB on HTTP is nothing but CRUD on ReST.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:178
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:178
  _m.extend( ['CouchPy for CouchDB. Model. Transact. Replicate. Program. Query. Eventually', '\n        '] )
  # lineno:179
  _m.extend( ['consistent with MVCC.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:180
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:181
  _m.pushbuf()
  _m.extend( ['<em>'] )
  _m.pushbuf()
  # lineno:181
  _m.extend( ['Programmers believe that the value of their system lies in', '\n          '] )
  # lineno:182
  _m.extend( ['the whole, in the building: posterity discovers it in the bricks with which', '\n          '] )
  # lineno:183
  _m.extend( ['they built and which are often used again for better building.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:184
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  _m.extend( ['\n        '] )
  # lineno:185
  _m.extend( ['Be it internet apps, be it desktop apps, build them on pluggdapps, whether your', '\n        '] )
  # lineno:186
  _m.extend( ['applications live or whither, your plugins will go on to build better apps.', '\n      '] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  # lineno:187
  _m.pushbuf()
  _m.extend( ['<li>'] )
  _m.pushbuf()
  # lineno:187
  _m.extend( ['Start by contributing plugins, grow as you design apps and become a network', '\n        '] )
  # lineno:188
  _m.extend( ['geek.', '\n'] )
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  _m.handletag( _m.popbuftext(), _m.popbuftext(), indent=False, nl='')
  return _m.popbuftext()

# ---- Interface functions

# ---- Footer
