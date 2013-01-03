# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

from  tayra.tags    import TayraTags

class TayraHTML5( TayraTags ):

    def handle( self, mach, tagname, tokens, styles, attributes, content ):
        fn = getattr(self, 'tag_'+tagname, None)
        if fn :
            attrs, remtoks = self.parse_specs( tokens, styles, attributes )
            html = fn( mach, tagname, remtoks, attrs, content )
        else :
            html = None
        return html

    def tag_a( self, mach, tagname, tokens, attributes, content ):
        """<a> tag handler. Supported tokens,

          * a quoted string token is interpreted as ``href`` attribute and 
            translated to ``href="string"``
        """
        for tok in tokens :
            if (tok[0], tok[-1]) == ('"', '"') :
                attributes += ' href=%s' % tok
        return '<a %s>%s</a>' % (attributes, content)

    def tag_abbr( self, mach, tagname, tokens, attributes, content ):
        """<abbr> tag handler. Supported tokens,

          * a quoted string token is interpreted as ``title`` attribute and 
            translates to ``title=<string>``
        """
        attributes += (' title=%s' % tokens[0]) if tokens else ''
        return '<abbr %s>%s</abbr>' % (attributes, content)

    def tag_area( self, mach, tagname, tokens, attributes, content ):
        """<area> tag handler. Supported tokens,

          * If token is of the form ''<shape>:<coords>'' it translates to
            ``shape="<shape>" coords="<coords>"`` attributes.
          * a quoted string token is interpreted as ``href`` attribute and 
            translated to ``href="string"``.
        """
        for tok in tokens :
            try    :
                shape, coords = tok.split(':', 1)
                attributes += ' shape="%s" coords="%s"' % (shape, coords)
            except :
                attributes += ' href=%s' % tok
        return '<area %s>%s</area>' % (attributes, content)

    audio2attr = {
        'autoplay'  : ' autoplay="autoplay"',
        'controls'  : ' controls="controls"',
        'loop'      : ' loop="loop"',
        'auto'      : ' preload="auto"',
        'metadata'  : ' preload="metadata"',
        'none'      : ' preload="none"',
    }
    def tag_audio( self, mach, tagname, tokens, attributes, content ):
        """<audio> tag handler. Support tokens,

          * ``autoplay`` token translates to ``autoplay="autoplay"``
          * ``controls`` token translates to ``controls="controls"``
          * ``loop`` token translates to ``loop="loop"``
          * ``auto`` token translates to ``preload="auto"``
          * ``metadata`` token translates to ``preload="metadata"``
          * ``none`` token translates to ``preload="none"``
          * a quoted string is interpreted as ``src`` attribute and translates
            to ``src=<string>``
        """
        for t in tokens :
            attr = self.audio2attr.get( t, None )
            attributes += attr if attr else (' src=%s' % t)
        return '<audio %s>%s</audio>' % (attributes, content)

    def tag_base( self, mach, tagname, tokens, attributes, content ):
        """<base> tag handler. Supported tokens,

          * If a token is present it is interpreted as ``target`` attribute 
            and translates to ``target="<token>"``
        """
        attributes += (' target="%s"' % tokens[0]) if tokens else ''
        return '<base %s>%s</base>' % (attributes, content)


    def tag_blockquote( self, mach, tagname, tokens, attributes, content ):
        """<blockquote> tag handler. Supported tokens,
          * a quoted string is interpreted as ``cite`` attribute and 
            translates to ``cite=<string>``
        """
        attributes += (' cite=%s' % tokens[0]) if tokens else ''
        return '<blockquote %s>%s</blockquote>' % (attributes, content)


    button2attr = {
        'button'            : ' type="button"',
        'reset'             : ' type="reset"',
        'submit'            : ' type="submit"',
        'autofocus'         : ' autofocus="autofocus"',
        'application/x-www-form-urlencoded': \
                            ' formenctype="application/x-www-form-urlencoded"',
        'multipart/form-data' : ' formenctype="multipart/form-data"',
        'text/plain'        : ' formenctype="text/plain"',
        'get'               : ' formmethod="get"',
        'post'              : ' formmethod="post"',
        'formnovalidate'    : ' formnovalidate="formnovalidate"',
        '_blank'            : ' target="_blank"',
        '_self'             : ' target="_self"',
        '_parent'           : ' target="_parent"',
        '_top'              : ' target="_top"',
    }
    def tag_button( self, mach, tagname, tokens, attributes, content ):
        """<button> tag handler. Supported tokens,
          * ``button`` token translates to ``type="button"``.
          * ``reset`` token translates to ``type="reset"``.
          * ``submit`` token translates to ``type="submit"``.
          * ``autofocus`` token translates to ``autofocus="autofocus"``.
          * ``application/x-www-form-urlencoded`` token translates to
            ``formenctype="application/x-www-form-urlencoded"``.
          * ``multipart/form-data`` token translates to
            ``formenctype="multipart/form-data"``.
          * ``text/plain`` token translates to ``formenctype="text/plain"``.
          * ``get`` token translates to ``formmethod="get"``.
          * ``post`` token translates to ``formmethod="post"``.
          * ``formnovalidate`` token translates to 
            ``formnovalidate="formnovalidate"``.
          * ``_blank`` token translates to ``target="_blank"``.
          * ``_self`` token translates to ``target="_self"``.
          * ``_parent`` token translates to ``target="_parent"``.
          * ``_top`` token translates to ``target="_top"``.
          * If a token starts with ``frame:<frametarget>`` it will be 
            translated to ``frametarget="<frametarget>"``.
          * If a token starts with ``form:<formname>`` it will be translated
            to ``form="<formname>"``.
          * a quoted string is interpreted as ``formaction`` attribute and 
            translates to ``formaction=<string>``.
        """
        for tok in tokens :
            if tok.startswith( 'frame:' ) :
                attributes += ' frametarget="%s"' % tok.split(':', 1)[1]
            elif tok.startswith( 'form:' ) :
                attributes += ' form="%s"' % tok.split(':', 1)[1]
            elif (tok[0], tok[-1]) == ('"', '"') :
                attr = self.button2attr.get( tok, '' )
                attributes += attr or (' formaction=%s' % tok)
        return '<button %s>%s</button>' % (attributes, content)

    def tag_canvas( self, mach, tagname, tokens, attributes, content ):
        """<canvas> tag handler. Supported tokens,

          * If a specifier token is of the form ``<width>,<height>`` it 
            translates to ``width="<width>" height="<height>"``.
        """
        try :
            attributes += (
                (' width="%s" height="%s"' % tokens[0].split(',', 1) )
                        if tokens else '' )
        except : pass
        return '<canvas %s>%s</canvas>' % (attributes, content)

    def tag_col( self, mach, tagname, tokens, attributes, content ):
        """<col> tag handler. Supported tokens,

          * If a token is present, it will be interpreted as ``span``
            attribute and translates to ``span="<span>"``
        """
        attributes += (' span="%s"' % tokens[0]) if tokens else ''
        return '<col %s>%s</col>' % (attributes, content)


    def tag_colgroup( self, mach, tagname, tokens, attributes, content ):
        """<colgroup> tag handler. Supported tokens,

          * If a specifier token is present, it will be interpreted as ``span``
            attribute and translates to ``span="<span>"``
        """
        attributes += (' span="%s"' % tokens[0]) if tokens else ''
        return '<colgroup %s>%s</colgroup>' % (attributes, content)

    command2attr = {
        'checkbox' : ' type="checkbox"',
        'command' : ' type="command"',
        'radio' : ' type="radio"',
    }
    def tag_command( self, mach, tagname, tokens, attributes, content ):
        """<command> tag handler. Supported tokens,

          * ``checkbox`` token translates to ``type="checkbox"``
          * ``command`` token translates to ``type="command"``
          * ``radio`` token translates to ``type="radio"``
          * a quoted string is interpreted as ``icon`` attribute and translated
            to ``icon=<string>``.
        """
        for t in tokens :
            attr = self.command2attr.get( t, None )
            attributes += attr or (' icon=%s' % t)
        return '<command %s>%s</command>' % (attributes, content)

    def tag_del( self, mach, tagname, tokens, attributes, content ):
        """<del> tag handler. Supported tokens,

        * If a non quoted token is present, it will interpreted as ``datetime``
          attribute and translates to ``datetime="<token>"``

        * a quoted string is interpreted as ``cite`` attribute and translated
          to ``cite=<string>``
        """
        for tok in tokens :
            if (tok[0], tok[-1]) == ('"', '"') :
                attributes += ' cite=%s' % tok
            else :
                attributes += ' datetime="%s"' % tok
        return '<del %s>%s</del>' % (attributes, content)

    def tag_detail( self, mach, tagname, tokens, attributes, content ):
        """<details> tag handler. Supported tokens,

          * ``open`` token translates to ``open="open"``
        """
        attributes += (' open="%s"' % tokens[0]) if tokens else ''
        return '<detail %s>%s</detail>' % (attributes, content)

    def tag_embed( self, mach, tagname, tokens, attributes, content ):
        """<embed> tag handler. Supported tokens,

          * If token of the form ``<width>,<height>`` it translates to 
            ``width="<width>" height="<height>"``.

          * a quoted string is interpreted as ``src`` attribute and translated
            to ``src=<string>``.
        """
        for tok in tokens :
            if (tok[0], tok[-1]) == ('"', '"') :
                attributes += ' src=%s' % tok
            else :
                try :
                    attributes += ' width="%s" height="%s"' % tok.split(',', 1)
                except : pass
        return '<embed %s>%s</embed>' % (attributes, content)

    def tag_fieldset( self, mach, tagname, tokens, attributes, content ):
        """<fieldset> tag handler. Supported tokens,

          * If a token is of the form ``f:<formname>``, it translates to
            ``form="<formname>"``.
        """
        try :
            attributes += (
                (' form="%s"' % tokens[0].split(':', 1)[1]) if tokens else '' )
        except : pass
        return '<fieldset %s>%s</fieldset>' % (attributes, content)

    form2attr = {
        'on'                : ' autocomplete="on"',
        'off'               : ' autocomplete="off"',
        'application/x-www-form-urlencoded' : \
                    ' enctype="application/x-www-form-urlencoded"',
        'multipart/form-data': ' enctype="multipart/form-data"',
        'text/plain'        : ' enctype="text/plain"',
        'get'               : ' method="get"',
        'post'              : ' method="post"',
        'novalidate'        : ' novalidate="novalidate"',
    }
    def tag_form( self, mach, tagname, tokens, attributes, content ):
        """<form> tag handler. Supported tokens,

        * ``on`` token translates to ``autocomplete="on"``.
        * ``off`` token translates to ``autocomplete="off"``.
        * ``application/x-www-form-urlencoded`` token translates to
          ``enctype="application/x-www-form-urlencoded"``.
        * ``multipart/form-data`` token translates to 
          ``enctype="multipart/form-data"``.
        * ``text/plain`` token translates to ``menctype="text/plain"``.
        * ``get`` token translates to ``formmethod="get"``
        * ``post`` token translates to ``formmethod="post"``
        * ``novalidate`` token translates to ``novalidate="novalidate"``
        * a quoted string is interpreted as ``action`` attribute and translated
          to //action=<string>//
        """
        for tok in tokens :
            attr = self.form2attr.get( tok, None )
            attributes += attr if attr else (' action=%s' % tok)
        return '<form %s>%s</form>' % (attributes, content)

    def tag_head( self, mach, tagname, tokens, attributes, content ):
        """<head> tag handler. Supported tokens,

        * a quoted string is interpreted as ``manifest`` attribute and
          translated to ``manifest=<string>``.
        """
        attributes += (' manifest=%s' % tokens[0]) if tokens else ''
        return '<head %s>%s</head>' % (attributes, content)

    def tag_html( self, mach, tagname, tokens, attributes, content ):
        """<html> tag handler. Supported tokens,

        * a quoted string is interpreted as ``manifest`` attribute and
          translated to ``manifest=<string>``.
        """
        attributes += (' manifest=%s' % tokens[0]) if tokens else ''
        return '<html %s>%s</html>' % (attributes, content)

    iframe2attr = {
        'seamless' : ' seamless="seamless"',
    }
    def tag_iframe( self, mach, tagname, tokens, attributes, content ):
        """<frame> tag handler. Supported tokens,

          * ``seamless`` token translated to ``seamless="seamless"``.
          * If a token is of the form ``<width>,<height>`` where width and 
            height are integers, it translates to 
            ``width="<width>" height="<height>"``.
          * If a token starts with ``allow-`` it will be joined together as
            comma separated value to ``sandbox`` attribute.
          * a quoted string is interpreted as ``src`` attribute and
            translated to ``src=<string>``
        """
        sandbox = []
        for t in tokens :
            if t.startswith( 'allow-' ) :
                sandbox.append(t)
            elif (t[0], t[1]) == ('"', '"') :
                attributes += ' src=%s' % t
            else :
                attr = self.iframe2attr.get( t, '' )
                try :
                    attributes += ( attr or 
                                    ' width="%s" height="%s"'%t.split(',', 1) )
                except : pass
        attributes += ' sandbox="%s"' % ' '.join(sandbox) if sandbox else ''
        return '<iframe %s>%s</iframe>' % (attributes, content)

    img2attr = {
        'ismap' : ' ismap="ismap"',
    }
    def tag_img( self, mach, tagname, tokens, attributes, content ):
        """<img> tag handler. Supported tokens,

          * ``ismap`` token translates to ``ismap="ismap"``
          * If a token is of the form ``<width>,<height>`` it is translated
            to ``width="<width>" height="<height>"``.
          * a quoted string is interpreted as ``src`` attribute and translated
            to //src=<string>//
        """
        for tok in tokens :
            if (tok[0], tok[-1]) == ('"', '"') :
                attributes += ' src=%s' % tok
            else :
                attr = self.img2attr.get( tok, None )
                try :
                    attributes += ( 
                        attr or
                        (' width="%s" height="%s"' % tok.split(',', 1)) )
                except : pass
        return '<img %s>%s</img>' % (attributes, content)

    def tag_ins( self, mach, tagname, tokens, attributes, content ):
        """<ins> tag handler. Supported tokens,

          * If a token is present it will interpreted as ``datetime`` 
            attribute and translated to ``datetime="<token>"``.
          * a quoted string is interpreted as ``cite`` attribute and translated
            to ``cite=<string>``.
        """
        for tok in tokens :
            if (tok[0], tok[-1]) == ('"', '"') :
                attributes += ' cite=%s' % tok
            else :
                attributes += ' datetime="%s"' % tok
        return '<ins %s>%s</ins>' % (attributes, content)

    def tag_label( self, mach, tagname, tokens, attributes, content ):
        """<label> tag handler. Supported tokens,

        * If a token looks like ``f:<formname>``, it will be translated to
          ``form="<formname>"``
        * Otherwise the token will be translated to //for="<token>"//
        """
        for tok in tokens :
            if tok.startswith( 'f:' ) :
                attributes += ' form="%s' % tok
            else :
                attributes += ' for="%s"' % tok
        return '<label %s>%s</label>' % (attributes, content)

    def tag_li( self, mach, tagname, tokens, attributes, content ):
        """<li> tag handler. Supported tokens,

          * If a token is present it will be translated to ``value="<token>"``.
        """
        attributes += (' value="%s"' % tokens[0]) if tokens else ''
        return '<li %s>%s</li>' % (attributes, content)

    def tag_link( self, mach, tagname, tokens, attributes, content ):
        """<link> tag handler. Supported tokens,

          * If a token is present it will be translated to ``type="<token>"``.
          * a quoted string is interpreted as ``cite`` attribute and translated
            to ``href=<string>``.
        """
        for tok in tokens :
            if (tok[0], tok[-1]) == ('"', '"') :
                attributes += ' href=%s' % tok
            else :
                attributes += ' type="%s"' % tok
        return '<link %s>%s</link>' % (attributes, content)

    def tag_menu( self, mach, tagname, tokens, attributes, content ):
        """<menu> tag handler. Supported tokens,

          * If a token is present it will be translated to ``type="<token>"``.
          * a quoted string is interpreted as ``label`` attribute and translated
            to ``label=<string>``.
        """
        for t in tokens :
            attributes += (' label=%s'%t) \
                                if (t,t) == ('"','"') else (' type="%s"'%t)
        return '<menu %s>%s</menu>' % (attributes, content)

    def tag_meta( self, mach, tagname, tokens, attributes, content ):
        """<meta> tag handler. Supported tokens,

        * If a token is present it will be translated to 
          ``http-equiv="<token>"``.
        * a quoted string is interpreted as ``content`` attribute and translated
          to ``content=<string>``.
        """
        for t in tokens :
            attributes += (' content=%s'%t) if (t,t) == ('"','"') \
                            else (' http-equiv="%s"'%t)
        return '<meta %s>%s</meta>' % (attributes, content)

    def tag_meter( self, mach, tagname, tokens, attributes, content ):
        """<meter> tag hanlder. Supported tokens,

        * If a token starts with ``f:<formname>`` it will be translated to
          ``form="<formname>"``.
        * If a token is of the form ``low < high`` it will be translated to
          ``low="<low>" high="<high>"``
        * If a token is of the form ``low < optimum < high`` it will be 
          translated to ``low="<low>" optimum="<optimum>" high="<high>"``.
        * Otherwise the token will be interpreted as //value// attribute and
          translated as ``value="<value>"``.
        """
        for tok in tokens :
            if tok.startswith('f:') :
                attributes += ' form="%s' % tok
                continue
            parts = tok.split('<')
            if len(parts) == 2 :
                attributes += ' low="%s" high="%s"' % tuple( parts )
            elif len(parts) == 3 :
                attributes += ' low="%s" optimum="%s" high="%s"' % tuple(parts)
            else :
                attributes += ' value="%s"' % tok
        return '<meter %s>%s</meter>' % (attributes, content)

    def tag_object( self, mach, tagname, tokens, attributes, content ):
        """<object> tag handler. Supported tokens,

          * If a token starts with ``form:`` it will be translated to 
            ``form="<formname>"``.
          * If a token is of the form ``<width>,<height>`` it will be
            translated to ``width="<width>" height="<height>"``.
          * a quoted string is interpreted as ``data`` attribute and
            translated as ``data=<string>``.
        """
        for tok in tokens :
            if (tok[0], tok[-1]) == ('"', '"') :
                attributes += ' data=%s' % tok
            elif tok.startswith( 'form:' ) :
                attributes += ' form="%s"' % tok
            else :
                try : 
                    attributes += ' width="%s" height="%s"' % tok.split(',', 1)
                except : pass
        return '<object %s>%s</object>' % (attributes, content)

    ol2attr = {
        'reversed' : ' reversed="reversed"',
        '1' : ' type="1"',
        'A' : ' type="A"',
        'a' : ' type="a"',
        'l' : ' type="l"',
        'i' : ' type="i"',
    }
    def tag_ol( self, mach, tagname, tokens, attributes, content ):
        """<ol> tag handler. Supported tokens,

          * ``reversed`` token translates to ``reversed="reversed"``.
          * ``1`` token translates to ``type="1"``.
          * ``A`` token translates to ``type="A"``.
          * ''a'' token translates to ``type="a"``.
          * ''l'' token translates to ``type="l"``.
          * ''i'' token translates to ``type="i"``.
          * If a token is of the form ``<type>,<start>``, it will be 
            translated to ``type="<type>" start="<start>"``.
        """
        for tok in tokens :
            attr = self.ol2attr.get( tok, None )
            try :
                attributes += ( attr or 
                                ' type="%s" start="%s"' % tok.split(',', 1) )
            except : pass
        return '<ol %s>%s</ol>' % (attributes, content)

    def tag_optgroup( self, mach, tagname, tokens, attributes, content ):
        """<optgroup> tag handler. Supported tokens,

          * a quoted string is interpreted as ``label`` attribute and translated
            to ``label=<string>``.
        """
        attributes += (' label=%s' % tokens[0]) if tokens else ''
        return '<optgroup %s>%s</optgroup>' % (attributes, content)

    def tag_option( self, mach, tagname, tokens, attributes, content ):
        """<option> tag handler. Supported tokens,

        * a quoted string is interpreted as ``value`` attribute and translated
          as ``value=<string>``.
        """
        attributes += (' value=%s' % tokens[0]) if tokens else ''
        return '<option %s>%s</option>' % (attributes, content)

    def tag_output( self, mach, tagname, tokens, attributes, content ):
        """<output> tag handler. Supported tokens,

          * If a token is of the form ``<form>:<name>`` it will be translated
            to ``form="<form>" for="<name>"``.
        """
        try :
            attributes += (
                (' form="%s" for="%s"' % tokens[0].split(':', 1)) 
                if tokens else '' )
        except : pass
        return '<output %s>%s</output>' % (attributes, content)

    def tag_param( self, mach, tagname, tokens, attributes, content ):
        """<param> tag handler. Supported tokens,

        * a quoted string is interpreted as ``value`` attribute and translated
          as ``value=<string>``.
        """
        attributes += (' value=%s' % tokens[0]) if tokens else ''
        return '<param %s>%s</param>' % (attributes, content)

    def tag_progress( self, mach, tagname, tokens, attributes, content ):
        """<progress> tag handler. Supported tokens,

          * If token is of the form ``<max>,<value>`` it will be translated to
            ``max="<max>" value="<value>"``.
        """
        try :
            attributes += (
                (' max="%s" value="%s"' % tokens[0].split(',', 1)) \
                if tokens else '' )
        except : pass
        return '<progress %s>%s</progress>' % (attributes, content)

    def tag_q( self, mach, tagname, tokens, attributes, content ):
        """<q> tag handler. Supported tokens,

          * a quoted string is interpreted as ``value`` attribute and 
            translated to ``cite=<string>``.
        """
        attributes += (' cite=%s' % tokens[0]) if tokens else ''
        return '<q %s>%s</q>' % (attributes, content)

    script2attr = {
        'async' : ' async="async"',
        'defer' : ' defer="defer"',
    }
    def tag_script(self, mach, tagname, tokens, attributes, content):
        """<script> tag handler. Supported tokens,

          * ``async`` token translates to ``async="async"``.
          * ''defer'' token translates to ``defer="defer"``.
          * Otherwise it will be interpreted as ``type`` attribute and 
            translated to ``type="<token>"``.
          * a quoted string is interpreted as ``src`` attribute and 
            as ``src=<string>``.
        """
        for tok in tokens :
            if (tok[0], tok[-1]) == ('"', '"') :
                attributes += ' src=%s' % tok
            else :
                attr = self.script2attr.get( tok, None )
                attributes += attr or ' type="%s"' % tok
        return '<script %s>%s</script>' % (attributes, content)

    def tag_source(self, mach, tagname, tokens, attributes, content):
        """<source> tag handler. Supported tokens,

          * If a token is present it will be interpreted as ``type`` 
            attribute and translated to ``type="<token>"``.
          * a quoted string is interpreted as ``src`` attribute and 
            as ``src=<string>``.
        """
        for tok in tokens :
            if (tok[0], tok[1]) == ('"', '"') :
                attributes += ' src=%s' % tok
            else :
                attributes += ' type="%s"' % tok
        return '<source %s>%s</source>' % (attributes, content)

    style2attr = {
        'text/css' : ' type="text/css"',
        'scoped'   : ' scoped="scoped"',
    }
    def tag_style(self, mach, tagname, tokens, attributes, content):
        """<style> tag handler. Supported tokens,

        * ``text/css`` token translates to ``type="text/css"``.
        * ``scoped`` token translates to ``scoped="scoped"``.
        """
        attributes += (' ' + 
                       ''.join([ self.style2attr.get(t, '') for t in tokens ]))
        return '<style %s>%s</style>' % (attributes, content)

    def tag_table(self, mach, tagname, tokens, attributes, content):
        """<table> tag handler. Supported tokens,

          * ``1`` token translates to ``border="1"``.
        """
        attributes += (' border="%s"' % tokens[0]) if tokens else ''
        return '<table %s>%s</table>' % (attributes, content)

    def tag_time( self, mach, tagname, tokens, attributes, content ):
        """<time> tag handler. Supported tokens,

          * If a token is present it will be interpreted as ``pubdate``
            attribute and translated as ``pubdate="<token>"``.
          * a quoted string is interpreted as ``datetime`` attribute and 
            translated as ``datetime=<string>``.
        """
        for tok in tokens :
            if (tok[0], tok[-1]) == ('"', '"') :
                attributes += ' datetime=%s' % tok
            else :
                attributes += ' pubdate="%s"' % tok
        return '<abbr %s>%s</abbr>' % (attributes, content)
