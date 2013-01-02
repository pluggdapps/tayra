# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

from  tayra.tags    import TayraTags

class TayraHTML5( TayraTags ):

    def handle( self, mach, tagname, tokens, styles, attributes, content ):
        fn = getattr(self, 'tag_'+tagname, None)
        if fn :
            html = fn(mach, tagname, tokens, styles, attributes, content)
        else :
            html = None
        return html

    def tag_a( self, mach, tagname, tokens, styles, attributes, content ):
        """<a> tag handler. Supported tokens,

          * a quoted string token is interpreted as ``href`` attribute and 
            translated to ``href="string"``

        ... code-block :: html
            <a "http://pluggdapps.com"> pluggdapps-link
            <!-- translates to -->
            <a href="http://pluggdapps.com"> pluggdapps-link </a>
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            if (tok[0], tok[-1]) == ('"', '"') :
                attrs += ' href=%s' % tok
        return '<a %s>%s</a>' % (attrs, content)

    def tag_abbr( self, mach, tagname, tokens, styles, attributes, content ):
        """<abbr> tag handler. Supported tokens,

          * a quoted string token is interpreted as ``title`` attribute and 
            translates to ``title=<string>``
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' title=%s' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<abbr %s>%s</abbr>' % (attrs, content)

    def tag_area( self, mach, tagname, tokens, styles, attributes, content ):
        """<area> tag handler. Supported tokens,

          * If token is of the form ''<shape>:<coords>'' it translates to
            ``shape="<shape>" coords="<coords>"`` attributes.
          * a quoted string token is interpreted as ``href`` attribute and 
            translated to ``href="string"``.

        ... code-block :: html

            <area circle:100,100,10 "http://pluggdapps.com">
            <!-- translates to -->
            <area shape="circle" coords="100,100,10" 
                  href="http://pluggdapps.com">
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            try    :
                shape, coords = tok.split(':', 1)
                attrs += ' shape="%s" coords="%s"' % (shape, coords)
            except :
                attrs += ' href=%s' % tok
        attrs = attrs.strip()
        return '<area %s>%s</area>' % (attrs, content)

    audio2attr = {
        'autoplay'  : ' autoplay="autoplay"',
        'controls'  : ' controls="controls"',
        'loop'      : ' loop="loop"',
        'auto'      : ' preload="auto"',
        'metadata'  : ' preload="metadata"',
        'none'      : ' preload="none"',
    }
    def tag_audio( self, mach, tagname, tokens, styles, attributes, content ):
        """<audio> tag handler. Support tokens,

          * ``autoplay`` token translates to ``autoplay="autoplay"``
          * ``controls`` token translates to ``controls="controls"``
          * ``loop`` token translates to ``loop="loop"``
          * ``auto`` token translates to ``preload="auto"``
          * ``metadata`` token translates to ``preload="metadata"``
          * ``none`` token translates to ``preload="none"``
          * a quoted string is interpreted as ``src`` attribute and translates
            to ``src=<string>``
    
        ... code-block :: html

            <audio autoplay loop 
                   "http://pluggdapps.com/rocknroll/howtonameit.mp3">
            <!-- translates to -->
            <audio autoplay="autoplay" loop="loop" 
                   src="http://pluggdapps.com/rocknroll/howtonameit.mp3">
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for t in remtoks :
            attr = self.audio2attr.get( t, None )
            attrs += attr if attr else (' src=%s' % t)
        attrs = attrs.strip()
        return '<audio %s>%s</audio>' % (attrs, content)

    def tag_base( self, mach, tagname, tokens, styles, attributes, content ):
        """<base> tag handler. Supported tokens,

          * If a token is present it is interpreted as ``target`` attribute 
            and translates to ``target="<token>"``
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' target="%s"' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<base %s>%s</base>' % (attrs, content)


    def tag_blockquote( self, mach, tagname, tokens, styles, attributes, 
                        content ):
        """<blockquote> tag handler. Supported tokens,
          * a quoted string is interpreted as ``cite`` attribute and 
            translates to ``cite=<string>``
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' cite=%s' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<blockquote %s>%s</blockquote>' % (attrs, content)


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
    def tag_button( self, mach, tagname, tokens, styles, attributes, content ):
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
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            if tok.startswith( 'frame:' ) :
                attrs += ' frametarget="%s"' % tok.split(':', 1)[1]
            elif tok.startswith( 'form:' ) :
                attrs += ' form="%s"' % tok.split(':', 1)[1]
            elif (tok[0], tok[-1]) == ('"', '"') :
                attr = self.button2attr.get( tok, '' )
                attrs += attr or (' formaction=%s' % tok)
        attrs = attrs.strip()
        return '<button %s>%s</button>' % (attrs, content)

    def tag_canvas( self, mach, tagname, tokens, styles, attributes, content ):
        """<canvas> tag handler. Supported tokens,

          * If a specifier token is of the form ``<width>,<height>`` it 
            translates to ``width="<width>" height="<height>"``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' width="%s" height="%s"' % remtoks[0].split(',', 1) ) \
                    if remtoks else ''
        attrs = attrs.strip()
        return '<canvas %s>%s</canvas>' % (attrs, content)

    def tag_col( self, mach, tagname, tokens, styles, attributes, content ):
        """<col> tag handler. Supported tokens,

          * If a token is present, it will be interpreted as ``span``
            attribute and translates to ``span="<span>"``
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' span="%s"' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<col %s>%s</col>' % (attrs, content)


    def tag_colgroup( self, mach, tagname, tokens, styles, attributes, 
                      content ):
        """<colgroup> tag handler. Supported tokens,

          * If a specifier token is present, it will be interpreted as ``span``
            attribute and translates to ``span="<span>"``
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' span="%s"' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<colgroup %s>%s</colgroup>' % (attrs, content)

    command2attr = {
        'checkbox' : ' type="checkbox"',
        'command' : ' type="command"',
        'radio' : ' type="radio"',
    }
    def tag_command(self, mach, tagname, tokens, styles, attributes, content):
        """<command> tag handler. Supported tokens,

          * ``checkbox`` token translates to ``type="checkbox"``
          * ``command`` token translates to ``type="command"``
          * ``radio`` token translates to ``type="radio"``
          * a quoted string is interpreted as ``icon`` attribute and translated
            to ``icon=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for t in remtoks :
            attr = self.command2attr.get( t, None )
            attrs += attr or (' icon=%s' % t)
        attrs = attrs.strip()
        return '<command %s>%s</command>' % (attrs, content)

    def tag_del(self, mach, tagname, tokens, styles, attributes, content):
        """<del> tag handler. Supported tokens,

        * If a non quoted token is present, it will interpreted as ``datetime``
          attribute and translates to ``datetime="<token>"``

        * a quoted string is interpreted as ``cite`` attribute and translated
          to ``cite=<string>``
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            if (tok[0], tok[-1]) == ('"', '"') :
                attrs += ' cite=%s' % tok
            else :
                attrs += ' datetime="%s"' % tok
        attrs = attrs.strip()
        return '<del %s>%s</del>' % (attrs, content)

    def tag_detail( self, mach, tagname, tokens, styles, attributes, content ):
        """<details> tag handler. Supported tokens,

          * ``open`` token translates to ``open="open"``
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' open="%s"' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<detail %s>%s</detail>' % (attrs, content)

    def tag_embed( self, mach, tagname, tokens, styles, attributes, content ):
        """<embed> tag handler. Supported tokens,

          * If token of the form ``<width>,<height>`` it translates to 
            ``width="<width>" height="<height>"``.

          * a quoted string is interpreted as ``src`` attribute and translated
            to ``src=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            if (tok[0], tok[-1]) == ('"', '"') :
                attrs += ' src=%s' % tok
            else :
                attrs += ' width="%s" height="%s"' % tok.split(',', 1)
        attrs = attrs.strip()
        return '<embed %s>%s</embed>' % (attrs, content)

    def tag_fieldset(self, mach, tagname, tokens, styles, attributes, content):
        """<fieldset> tag handler. Supported tokens,

          * If a token is of the form ``f:<formname>``, it translates to
            ``form="<formname>"``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' form="%s"' % remtoks[0].split(':', 1)[1]) if remtoks else ''
        attrs = attrs.strip()
        return '<fieldset %s>%s</fieldset>' % (attrs, content)

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
    def tag_form( self, mach, tagname, tokens, styles, attributes, content ):
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
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            attr = self.form2attr.get( tok, None )
            attrs += attr if attr else (' action=%s' % tok)
        attrs = attrs.strip()
        return '<form %s>%s</form>' % (attrs, content)

    def tag_head( self, mach, tagname, tokens, styles, attributes, content ):
        """<head> tag handler. Supported tokens,

        * a quoted string is interpreted as ``manifest`` attribute and
          translated to ``manifest=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' manifest=%s' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<head %s>%s</head>' % (attrs, content)

    def tag_html( self, mach, tagname, tokens, styles, attributes, content ):
        """<html> tag handler. Supported tokens,

        * a quoted string is interpreted as ``manifest`` attribute and
          translated to ``manifest=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' manifest=%s' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<html %s>%s</html>' % (attrs, content)

    iframe2attr = {
        'seamless' : ' seamless="seamless"',
    }
    def tag_iframe( self, mach, tagname, tokens, styles, attributes, content ):
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
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        sandbox = []
        for t in remtoks :
            if t.startswith( 'allow-' ) :
                sandbox.append(t)
            elif (t[0], t[1]) == ('"', '"') :
                attrs += ' src=%s' % t
            else :
                attr = self.iframe2attr.get( t, '' )
                attrs += attr or ' width="%s" height="%s"' % t.split(',', 1)
        attrs += ' sandbox="%s"' % ' '.join(sandbox) if sandbox else ''
        attrs = attrs.strip()
        return '<iframe %s>%s</iframe>' % (attrs, content)

    img2attr = {
        'ismap' : ' ismap="ismap"',
    }
    def tag_img( self, mach, tagname, tokens, styles, attributes, content ):
        """<img> tag handler. Supported tokens,

          * ``ismap`` token translates to ``ismap="ismap"``
          * If a token is of the form ``<width>,<height>`` it is translated
            to ``width="<width>" height="<height>"``.
          * a quoted string is interpreted as ``src`` attribute and translated
            to //src=<string>//
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            if (tok[0], tok[-1]) == ('"', '"') :
                attrs += ' src=%s' % tok
            else :
                attr = self.img2attr.get( tok, None )
                attrs += attr or ' width="%s" height="%s"' % tok.split(',', 1)
        attrs = attrs.strip()
        return '<img %s>%s</img>' % (attrs, content)

    def tag_ins( self, mach, tagname, tokens, styles, attributes, content ):
        """<ins> tag handler. Supported tokens,

          * If a token is present it will interpreted as ``datetime`` 
            attribute and translated to ``datetime="<token>"``.
          * a quoted string is interpreted as ``cite`` attribute and translated
            to ``cite=<string>``.
        """
        for tok in remtoks :
            if (tok[0], tok[-1]) == ('"', '"') :
                attrs += ' cite=%s' % tok
            else :
                attrs += ' datetime="%s"' % tok
        attrs = attrs.strip()
        return '<ins %s>%s</ins>' % (attrs, content)

    def tag_label( self, mach, tagname, tokens, styles, attributes, content ):
        """<label> tag handler. Supported tokens,

        * If a token looks like ``f:<formname>``, it will be translated to
          ``form="<formname>"``
        * Otherwise the token will be translated to //for="<token>"//
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            if tok.startswith( 'f:' ) :
                attrs += ' form="%s' % tok
            else :
                attrs += ' for="%s"' % tok
        attrs = attrs.strip()
        return '<label %s>%s</label>' % (attrs, content)

    def tag_li( self, mach, tagname, tokens, styles, attributes, content ):
        """<li> tag handler. Supported tokens,

          * If a token is present it will be translated to ``value="<token>"``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' value="%s"' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<li %s>%s</li>' % (attrs, content)

    def tag_link( self, mach, tagname, tokens, styles, attributes, content ):
        """<link> tag handler. Supported tokens,

          * If a token is present it will be translated to ``type="<token>"``.
          * a quoted string is interpreted as ``cite`` attribute and translated
            to ``href=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for t in remtoks :
            attrs += (' href=%s'%t) if (t,t) == ('"','"') else (' type="%s"'%t)
        attrs = attrs.strip()
        return '<link %s>%s</link>' % (attrs, content)

    def tag_menu( self, mach, tagname, tokens, styles, attributes, content ):
        """<menu> tag handler. Supported tokens,

          * If a token is present it will be translated to ``type="<token>"``.
          * a quoted string is interpreted as ``label`` attribute and translated
            to ``label=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for t in remtoks :
            attrs += (' label=%s'%t) if (t,t) == ('"','"') else (' type="%s"'%t)
        attrs = attrs.strip()
        return '<menu %s>%s</menu>' % (attrs, content)

    def tag_meta( self, mach, tagname, tokens, styles, attributes, content ):
        """<meta> tag handler. Supported tokens,

        * If a token is present it will be translated to 
          ``http-equiv="<token>"``.
        * a quoted string is interpreted as ``content`` attribute and translated
          to ``content=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for t in remtoks :
            attrs += (' content=%s'%t) if (t,t) == ('"','"') \
                            else (' http-equiv="%s"'%t)
        attrs = attrs.strip()
        return '<meta %s>%s</meta>' % (attrs, content)

    def tag_meter( self, mach, tagname, tokens, styles, attributes, content ):
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
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            if tok.startswith('f:') :
                attrs += ' form="%s' % tok
                continue
            parts = tok.split('<')
            if len(parts) == 2 :
                attrs += ' low="%s" high="%s"' % tuple( parts )
            elif len(parts) == 3 :
                attrs += ' low="%s" optimum="%s" high="%s"' % tuple( parts )
            else :
                attrs += ' value="%s"' % tok
        attrs = attrs.strip()
        return '<meter %s>%s</meter>' % (attrs, content)

    def tag_object( self, mach, tagname, tokens, styles, attributes, content ):
        """<object> tag handler. Supported tokens,

          * If a token starts with ``form:`` it will be translated to 
            ``form="<formname>"``.
          * If a token is of the form ``<width>,<height>`` it will be
            translated to ``width="<width>" height="<height>"``.
          * a quoted string is interpreted as ``data`` attribute and
            translated as ``data=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            if (tok[0], tok[-1]) == ('"', '"') :
                attrs += ' data=%s' % tok
            elif tok.startswith( 'form:' ) :
                attrs += ' form="%s"' % tok
            else :
                attrs += ' width="%s" height="%s"' % tok.split(',', 1)
        attrs = attrs.strip()
        return '<object %s>%s</object>' % (attrs, content)

    ol2attr = {
        'reversed' : ' reversed="reversed"',
        '1' : ' type="1"',
        'A' : ' type="A"',
        'a' : ' type="a"',
        'l' : ' type="l"',
        'i' : ' type="i"',
    }
    def tag_ol( self, mach, tagname, tokens, styles, attributes, content ):
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
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            attr = self.ol2attr.get( tok, None )
            attrs += attr or ' type="%s" start="%s"' % tok.split(',', 1)
        attrs = attrs.strip()
        return '<ol %s>%s</ol>' % (attrs, content)

    def tag_optgroup(self, mach, tagname, tokens, styles, attributes, content):
        """<optgroup> tag handler. Supported tokens,

          * a quoted string is interpreted as ``label`` attribute and translated
            to ``label=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' label=%s' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<optgroup %s>%s</optgroup>' % (attrs, content)

    def tag_option(self, mach, tagname, tokens, styles, attributes, content):
        """<option> tag handler. Supported tokens,

        * a quoted string is interpreted as ``value`` attribute and translated
          as ``value=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' value=%s' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<option %s>%s</option>' % (attrs, content)

    def tag_output(self, mach, tagname, tokens, styles, attributes, content):
        """<output> tag handler. Supported tokens,

          * If a token is of the form ``<form>:<name>`` it will be translated
            to ``form="<form>" for="<name>"``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' form="%s" for="%s"' % remtoks[0].split(':', 1)) \
                        if remtoks else ''
        attrs = attrs.strip()
        return '<output %s>%s</output>' % (attrs, content)

    def tag_param(self, mach, tagname, tokens, styles, attributes, content):
        """<param> tag handler. Supported tokens,

        * a quoted string is interpreted as ``value`` attribute and translated
          as ``value=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' value=%s' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<param %s>%s</param>' % (attrs, content)

    def tag_progress(self, mach, tagname, tokens, styles, attributes, content):
        """<progress> tag handler. Supported tokens,

          * If token is of the form ``<max>,<value>`` it will be translated to
            ``max="<max>" value="<value>"``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' max="%s" value="%s"' % remtoks[0].split(',', 1)) \
                        if remtoks else ''
        attrs = attrs.strip()
        return '<progress %s>%s</progress>' % (attrs, content)

    def tag_q(self, mach, tagname, tokens, styles, attributes, content):
        """<q> tag handler. Supported tokens,

          * a quoted string is interpreted as ``value`` attribute and 
            translated to ``cite=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' cite=%s' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<q %s>%s</q>' % (attrs, content)

    script2attr = {
        'async' : ' async="async"',
        'defer' : ' defer="defer"',
    }
    def tag_script(self, mach, tagname, tokens, styles, attributes, content):
        """<script> tag handler. Supported tokens,

          * ``async`` token translates to ``async="async"``.
          * ''defer'' token translates to ``defer="defer"``.
          * Otherwise it will be interpreted as ``type`` attribute and 
            translated to ``type="<token>"``.
          * a quoted string is interpreted as ``src`` attribute and 
            as ``src=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            if (tok[0], tok[-1]) == ('"', '"') :
                attrs += ' src=%s' % tok
            else :
                attr = self.script2attr.get( tok, None )
                attrs += attr or ' type="%s"' % tok
        attrs = attrs.strip()
        return '<script %s>%s</script>' % (attrs, content)

    def tag_source(self, mach, tagname, tokens, styles, attributes, content):
        """<source> tag handler. Supported tokens,

          * If a token is present it will be interpreted as ``type`` 
            attribute and translated to ``type="<token>"``.
          * a quoted string is interpreted as ``src`` attribute and 
            as ``src=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            if (tok[0], tok[1]) == ('"', '"') :
                attrs += ' src=%s' % tok
            else :
                attrs += ' type="%s"' % tok
        attrs = attrs.strip()
        return '<source %s>%s</source>' % (attrs, content)

    style2attr = {
        'text/css' : ' type="text/css"',
        'scoped'   : ' scoped="scoped"',
    }
    def tag_style(self, mach, tagname, tokens, styles, attributes, content):
        """<style> tag handler. Supported tokens,

        * ``text/css`` token translates to ``type="text/css"``.
        * ``scoped`` token translates to ``scoped="scoped"``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += ' '+''.join([ self.style2attr.get( t, '' ) for t in remtoks ])
        attrs = attrs.strip()
        return '<style %s>%s</style>' % (attrs, content)

    def tag_table(self, mach, tagname, tokens, styles, attributes, content):
        """<table> tag handler. Supported tokens,

          * ``1`` token translates to ``border="1"``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs += (' border="%s"' % remtoks[0]) if remtoks else ''
        attrs = attrs.strip()
        return '<table %s>%s</table>' % (attrs, content)

    def tag_time(self, mach, tagname, tokens, styles, attributes, content):
        """<time> tag handler. Supported tokens,

          * If a token is present it will be interpreted as ``pubdate``
            attribute and translated as ``pubdate="<token>"``.
          * a quoted string is interpreted as ``datetime`` attribute and 
            translated as ``datetime=<string>``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            if (tok[0], tok[-1]) == ('"', '"') :
                attrs += ' datetime=%s' % tok
            else :
                attrs += ' pubdate="%s"' % tok
        attrs = attrs.strip()
        return '<abbr %s>%s</abbr>' % (attrs, content)
