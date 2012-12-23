# -*- coding: utf-8 -*-

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 R Pratap Chakravarthy

import re

from   tayra.tags       import TayraTags

class TayraHTML5Forms( TayraTags ):
    """Plugin to handle HTML input elements.
      * ``on`` token translates to ``autocomplete="on"``.
      * ``off`` token translates to ``autocomplete="off"'``.
      * ``autofocus`` token translates to ``autofocus="autofocus"``.
      * ``application/x-www-form-urlencoded`` token translates to
         ``enctype="application/x-www-form-urlencoded"``.
      * ``multipart/form-data`` token translates to
         ``enctype="multipart/form-data"``.
      * ``text/plain`` token translates to ``enctype="text/plain"//.
      * ``get`` token translates to ``formmethod="get"``.
      * ``post`` token translates to ``formmethod="post"``.
      * ``novalidate`` token translates to ``formnovalidate="novalidate"``.
      * ``required`` token translates to ``required="required"``.
      * ``checked`` token translates to ``checked="checked"``.
      * ``hard`` atom translates to ``wrap="hard"``.
      * ``soft`` atom translates to ``wrap="soft"``.
      * If a token is comma seperated items of the form [item1,item2] it will
        be interpreted as ``list`` attribute and translates to 
        ``list="item1,item2"``.
      * If a token has the syntax, `pattern` or %pattern% it will be interpreted
        as ``pattern`` attribute and translates to ``pattern="pattern"``
      * If a token is of the form ``h:placeholder`` it will be interpreted as
        ``placeholder`` attribute and translates to 
        ``placeholder="placeholder"``.
        If help string has several words seperated by white-space, replace
        spaces with ``+`` character. If help string is more complicated
        containing several special characters it is better to avoid ``h:...``
        format and define them directly as an attribute.
      * If a token is of the form ``f:formname`` it will be translated to
        ``form="formname"``.
      * If a token is of the form ``a:formaction`` it will be translated to
        ``formaction="formaction"``. If action-url contains white-spaces,
        replace them with ``+`` character.
      * If a token has the syntax ``min<step<max`` where min, step and max are
        integers, it translates to ``min="min" step="step" max="max"``.
      * If a token has the syntax ``min<max`` where min and max are integers,
        it is translated to ``min="min" max="max"``.
      * If a token has the syntax ``maxlength:size`` where maxlength and size
        are integers, it translates to ``maxlength="ma``ength" size="size"``
      * If a token has the syntax ``width,height`` where width and height are
        integers, it translates to ``height="height" width="width"``.
      * a quoted string is interpreted as ``src`` attribute and translated
        to ``value=<string>``.
    """

    token2attrs = {
        'on'        : ' autocomplete="on"',
        'off'       : ' autocomplete="off"',
        'autofocus' : ' autofocus="autofocus"',
        'application/x-www-form-urlencoded' : \
                    ' enctype="application/x-www-form-urlencoded"',
        'multipart/form-data' : ' enctype="multipart/form-data"',
        'text/plain': ' enctype="text/plain"',
        'get'       : ' formmethod="get"',
        'post'      : ' formmethod="post"',
        'novalidate': ' formnovalidate="novalidate"',
        'required'  : ' required="required"',
        'checked'   : ' checked="checked"',
        'hard'      : ' wrap="hard"',
        'soft'      : ' wrap="soft"',
    }

    reglist = r'(\[[^ ]*?\])'           # [list]
    regpatt = r'(`[^`]*?`)|(%[^%]*?%)'  # `pattern`, %pattern%
    reghelp = r'(h:[^ ]*?)'             # h:placeholder,
    regform = r'(f:[^ ]*?)'             # f:form
    regactn = r'(a:[^ ]*?)'             # a:formaction
    regrang = r'([0-9]*<[0-9]*)|([0-9]*<[0-9]*<[0-9]*)' # min<step<max, min<max
    reglen  = r'([0-9]*:[0-9]*)'        # maxlength:size
    regport = r'([0-9%]*,[0-9%]*)'      # width,height
    regquot = r'("[^"\\]*(?:\\.[^"\\]*)*")' # string (value or otherwise)
    regexp = re.compile( r'|'.join([ 
                reglist, regpatt, reghelp, regform, regactn, regrang, reglen,
                regport, regquot ]))
    handlers = [
        lambda x : ' list="%s"'         % x[1:-1],
        lambda x : ' pattern="%s"'      % x[1:-1],
        lambda x : ' pattern="%s"'      % x[1:-1],
        lambda x : ' placeholder="%s"'  % x[3:-1].replace('+', ' '),
        lambda x : ' form="%s"'         % x[2:],
        lambda x : ' formaction="%s"'   % x[2:].replace('+', ' '),
        lambda x : ' min="%s" max="%s"' % x.split('<', 1),
        lambda x : ' min="%s" step="%s" max="%s"' % x.split('<', 2),
        lambda x : ' maxlength="%s" size="%s"' % x.split(':', 1),
        lambda x : ' height="%s" width="%s"' % x.split(',', 1),
        lambda x : ' value=%s' % x
    ]

    def handle( self, mach, tagname, tokens, styles, attributes, content ):
        fn = getattr(self, 'tag_'+tagname, None)
        if fn :
            l = len(content) - len(content.rstrip())
            content, nl = (content[:-l], content[-l:]) if l else (content, '')
            html = fn(mach, tagname, tokens, styles, attributes, content) + nl
        else :
            html = None
        return html

    def parse_input_attributes( self, attrs, tokens, regex, handlers ):
        c = len(handlers)
        for m in regex.findall( ' '.join( tokens )) :
            for i in range(c) :
                if not m[i] : continue
                attrs += handlers[i]( m[i] )
                break
        return attrs

    def tag_inpbutton(self,mach,tagname, tokens, styles, attributes, content):
        """<input type="button"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="button" %s>%s</input>' % (attrs, content)

    def tag_inpchk(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="check"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="checkbox" %s>%s</input>' % (attrs, content)

    def tag_inpcolor(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="color"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="color" %s>%s</input>' % (attrs, content)

    def tag_inpdate(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="date"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="date" %s>%s</input>' % (attrs, content)

    def tag_inpdt(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="datetime"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="datetime" %s>%s</input>' % (attrs, content)

    def tag_inpdtlocal(self,mach,tagname,tokens,styles,attributes,content):
        """<input type="datetime-local"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="datetime-local" %s>%s</input>' % (attrs, content)

    def tag_inpemail(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="email"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="email" %s>%s</input>' % (attrs, content)

    def tag_inpfile(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="file"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="file" %s>%s</input>' % (attrs, content)

    def tag_inphidden(self,mach, tagname, tokens, styles, attributes,content):
        """<input type="hidden"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="hidden" %s>%s</input>' % (attrs, content)

    imghandlers = handlers[:]
    imghandlers[10] = lambda x : ' src=%s' % x
    def tag_inpimg(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="image"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.imghandlers )
        attrs = attrs.strip()
        return '<input type="image" %s>%s</input>' % (attrs, content)

    def tag_inpmonth(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="month"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="month" %s>%s</input>' % (attrs, content)

    def tag_inpnum(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="number"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="number" %s>%s</input>' % (attrs, content)

    def tag_inppass(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="password"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="password" %s>%s</input>' % (attrs, content)

    def tag_inpradio(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="radio"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="radio" %s>%s</input>' % (attrs, content)

    def tag_inprange(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="range"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="range" %s>%s</input>' % (attrs, content)

    def tag_inpreset(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="reset"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="reset" %s>%s</input>' % (attrs, content)

    def tag_inpsearch(self, mach, tagname, tokens, styles, attributes,content):
        """<input type="search"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="search" %s>%s</input>' % (attrs, content)

    def tag_inpsub(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="submit"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="submit" %s>%s</input>' % (attrs, content)

    def tag_inptel(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="tel"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="tel" %s>%s</input>' % (attrs, content)

    def tag_inptext(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="text"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="text" %s>%s</input>' % (attrs, content)

    def tag_inptime(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="time"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="time" %s>%s</input>' % (attrs, content)

    def tag_inpurl(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="url"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="url" %s>%s</input>' % (attrs, content)

    def tag_inpweek(self, mach, tagname, tokens, styles, attributes, content):
        """<input type="week"> handler"""
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.regexp, self.handlers )
        attrs = attrs.strip()
        return '<input type="week" %s>%s</input>' % (attrs, content)

    regint  = r'([0-9]*)'
    taregexp = re.compile( '|'.join([ reghelp, regform, regint, regport ]))
    tahandlers = [
        lambda x : ' placeholder=%s'    % x[2:],
        lambda x : ' placeholder="%s"'  % x[3:-1],
        lambda x : ' form="%s"'         % x[2:],
        lambda x : ' maxlength="%s"'    % int(x),
        lambda x : ' cols="%s" rows="%s"' % x.split(',', 1)
    ]
    def tag_textarea(self, mach, tagname, tokens, styles, attributes, content):
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        attrs = self.parse_input_attributes( 
                            attrs, tokens, self.taregexp, self.tahandlers )
        attrs = attrs.strip()
        return '<textarea %s>%s</textarea>' % (attrs, content)

    select2attr = {
        'autofocus' : ' autofocus="autofocus"',
    }
    def tag_select(self, mach, tagname, tokens, styles, attributes, content):
        """<select> handler. Supported tokens,

          * ``autofocus`` atom translates to ``autofocus="autofocus"``.
          * If a token is of the form ``f:formname`` it will be translated to
            ``form="formname"``.
          * Otherwise the atom is interpreted as integer ``size``, and 
            translated to ``size="size"``.
        """
        attrs, remtoks = self.parse_specs( tokens, styles, attributes )
        for tok in remtoks :
            if tok.startswith('f:') :
                attrs += ' form=%s' % tok
            else :
                attr = self.select2attr.get( tok, '' )
                attrs += attr or (' size="%s"' % tok)
        attrs = attrs.strip()
        return '<select %s>%s</select>' % (attrs, content)
