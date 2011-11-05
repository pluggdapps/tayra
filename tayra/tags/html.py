# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

# -*- coding: utf-8 -*-

from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.tags           import TagPlugin
from   tayra.interfaces     import ITayraTag

gsm = getGlobalSiteManager()

class HtmlA( TagPlugin ):
    """<a> tag handler.
    * '/string specifier/' is interpreted as //href// attribute and translates
      to //href=<string>//
    
    | <a "http://pluggdapps.com"> pluggdapps-link
    translates to
    | <a href="http://pluggdapps.com"> pluggdapps-link </a>
    """
    pluginname = 'html5.a'
    def specstrings2attrs( self, strings ):
        return u'href=%s' % strings[0] if strings else u''


class HtmlAbbr( TagPlugin ):
    """<abbr> tag handler.
    * '/string specifier/' is interpreted as //title// attribute and translates
      to //title=<string>//
    """
    pluginname = 'html5.abbr'
    def specstrings2attrs( self, strings ):
        return u'title=%s' % strings[0] if strings else u''


class HtmlArea( TagPlugin ):
    """<area> tag handler.
    * If atom is of the form ''<shape>:<coords>'' it translates to
      //shape="<shape>" coords="<coords>"// attributes
    * '/string specifier/' is interpreted as //href// attribute and translates
      to //href=<string>//

    | <area circle:100,100,10 "http://pluggdapps.com">
    translates to
    | <area shape="circle" coords="100,100,10" href="http://pluggdapps.com">
    """
    pluginname = 'html5.area'
    def specstrings2attrs( self, strings ):
        return u'href=%s' % strings[0] if strings else u''

    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            try :
                shape, coords = atom.split(':', 1)
                defattrs += u' shape="%s" coords="%s"' % (shape, coords)
                break
            except : 
                pass
        return defattrs, []


class HtmlAudio( TagPlugin ):
    """<audio> tag handler.
    * ''autoplay'' atom translates to //autoplay="autoplay"//
    * ''controls'' atom translates to //controls="controls"//
    * ''loop'' atom translates to //loop="loop"//
    * ''auto'' atom translates to //preload="auto"//
    * ''metadata'' atom translates to //preload="metadata"//
    * ''none'' atom translates to //preload="none"//
    * '/string specifier/' is interpreted as //src// attribute and translates
      to //src=<string>//

    | <audio autoplay loop "http://pluggdapps.com/rocknroll/howtonameit.mp3">
    translates to
    | <audio autoplay="autoplay" loop="loop" src="http://pluggdapps.com/rocknroll/howtonameit.mp3">
    """
    pluginname = 'html5.audio'
    atom2attr = {
        'autoplay' : ' autoplay="autoplay"',
        'controls' : ' controls="controls"',
        'loop' : ' loop="loop"',
        'auto' : ' preload="auto"',
        'metadata' : ' preload="metadata"',
        'none' : ' preload="none"',
    }
    def specstrings2attrs( self, strings ):
        return u'src=%s' % strings[0] if strings else u''

    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u''.join([ self.atom2attr.get(x, u'') for x in atoms ])
        return defattrs, []


class HtmlBase( TagPlugin ):
    """<base> tag handler.
    * If an atom is present it is interpreted as target attribute and translates
      to //target="<atom>"//
    """
    pluginname = 'html5.base'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' target="%s"'%atoms[0] if atoms else ' '
        return defattrs


class HtmlBlockquote( TagPlugin ):
    """<blockquote> tag handler.
    * '/string specifier/' is interpreted as //cite// attribute and translates
      to //cite=<string>//
    """
    pluginname = 'html5.blockquote'
    def specstrings2attrs( self, strings ):
        return u'cite=%s' % strings[0] if strings else u''


class HtmlButton( TagPlugin ):
    """<buttom> tag handler.
    * ''button'' atom translates to //type="button"//
    * ''reset'' atom translates to //type="reset"//
    * ''submit'' atom translates to //type="submit"//
    * ''autofocus'' atom translates to //autofocus="autofocus"//
    * ''application/x-www-form-urlencoded'' atom translates to
      //formenctype="application/x-www-form-urlencoded"//
    * ''multipart/form-data'' atom translates to 
      //formenctype="multipart/form-data"//
    * ''text/plain'' atom translates to //formenctype="text/plain"//
    * ''get'' atom translates to //formmethod="get"//
    * ''post'' atom translates to //formmethod="post"//
    * ''formnovalidate'' atom translates to //formnovalidate="formnovalidate"//
    * ''_blank'' atom translates to //target="_blank"//
    * ''_self'' atom translates to //target="_self"//
    * ''_parent'' atom translates to //target="_parent"//
    * ''_top'' atom translates to //target="_top"//
    * If an atom starts with //frame:<frametarget>// it will be translated to
      //frametarget="<frametarget>"//
    * If an atom starts with //form:<formname>// it will be translated to
      //form="<formname>"//
    * '/string specifier/' is interpreted as //formaction// attribute and
      translates to //formaction=<string>//
    """
    pluginname = 'html5.button'
    atom2attr = {
        'button' : ' type="button"',
        'reset' : ' type="reset"',
        'submit' : ' type="submit"',
        'autofocus' : ' autofocus="autofocus"',
        'application/x-www-form-urlencoded':' formenctype="application/x-www-form-urlencoded"',
        'multipart/form-data' : ' formenctype="multipart/form-data"',
        'text/plain' : ' formenctype="text/plain"',
        'get' : ' formmethod="get"',
        'post' : ' formmethod="post"',
        'formnovalidate' : ' formnovalidate="formnovalidate"',
        '_blank' : ' target="_blank"',
        '_self' : ' target="_self"',
        '_parent' : ' target="_parent"',
        '_top' : ' target="_top"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            attr = self.atom2attr.get( atom, None )
            if attr != None :
                defattrs += attr
                continue
            if atom.startswith( 'frame:' ):
                defattrs += u' frametarget="%s"' % atom[6:]
                continue
            if atom.startswith( 'form:' ):
                defattrs += u' form="%s"' % atom[5:].replace(',', ' ')
                continue
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'formaction=%s' % strings[0] if strings else u''
         

class HtmlCanvas( TagPlugin ):
    """<canvas> tag handler.
    * If a specifier atom is of the form //<width>,<height>// it translates to
      //width="<width>" height="<height>"//.
    """
    pluginname = 'html5.canvas'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            try : defattrs += u' width="%s" height="%s"' % atom.split(',')
            except : pass
        return defattrs, []


class HtmlCol( TagPlugin ):
    """<col> tag handler.
    * If a specifier atom is present, it will be interpreted as //span//
      attribute and translates to //span="<span>"//
    """
    pluginname = 'html5.col'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' span="%s"' % atoms[0] if atoms else u''
        return defattrs, []


class HtmlColgroup( TagPlugin ):
    """<colgroup> tag handler.
    * If a specifier atom is present, it will be interpreted as //span//
      attribute and translates to //span="<span>"//
    """
    pluginname = 'html5.colgroup'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' span="%s"' % atoms[0] if atoms else u''
        return defattrs, []

class HtmlCommand( TagPlugin ):
    """<command> tag handler.
    * ''checkbox'' atom translates to //type="checkbox"//
    * ''command'' atom translates to //type="command"//
    * ''radio'' atom translates to //type="radio"//
    * '/string specifier/' is interpreted as //icon// attribute and translates
      to //icon=<string>//
    """
    pluginname = 'html5.command'
    atom2attr = {
        'checkbox' : ' type="checkbox"',
        'command' : ' type="command"',
        'radio' : ' type="radio"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += self.atom2attr[atoms[0]] if atoms else u''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'icon=%s' % strings[0] if strings else u''


class HtmlDel( TagPlugin ):
    """<del> tag handler.
    * If a specifier atom is present it will interpreted as //datetime//
      attribute and translates to //datetime="<atom>"//
    * '/string specifier/' is interpreted as //cite// attribute and translates
      to //cite=<string>//
    """
    pluginname = 'html5.del'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' datetime="%s"'+atoms[0] if atoms else u''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'cite=%s' % strings[0] if strings else u''

class HtmlDetails( TagPlugin ):
    """<details> tag handler.
    * ''open'' atom translates to //open="open"//
    """
    pluginname = 'html5.details'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' open="open"' if atoms else u''
        return defattrs, []


class HtmlEmbed( TagPlugin ):
    """<embed> tag handler.
    * If a specifier atom is of the form //<width>,<height>// it translates
      to //width="<width>" height="<height>"//.
    * '/string specifier/' is interpreted as //src// attribute and translates
      to //src=<string>//
    """
    pluginname = 'html5.embed'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            try : defattrs += u' width="%s" height="%s"' % atom.split(',')
            except : pass
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'src=%s' % strings[0] if strings else u''


class HtmlFieldset( TagPlugin ):
    """<fieldset> tag handler.
    * If a specifier atom looks like //f:<formname>//, it translates to
      //form="<formname>"//
    """
    pluginname = 'html5.fieldset'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            if atom.startwith( 'f:' ):
                defattrs += u' form="%s"' % atom.replace(',', ' ')
                continue
        return defattrs, []


class HtmlForm( TagPlugin ):
    """<form> tag handler.
    * ''on'' atom translates to //autocomplete="on"//
    * ''off'' atom translates to //autocomplete="off"//
    * ''application/x-www-form-urlencoded'' atom translates to
      //enctype="application/x-www-form-urlencoded"//
    * ''multipart/form-data'' atom translates to 
      //enctype="multipart/form-data"//
    * ''text/plain'' atom translates to //menctype="text/plain"//
    * ''get'' atom translates to //formmethod="get"//
    * ''post'' atom translates to //formmethod="post"//
    * ''novalidate'' atom translates to //novalidate="novalidate"//
    * '/string specifier/' is interpreted as //action// attribute and
      translates to //action=<string>//
    """
    pluginname = 'html5.form'
    atom2attr = {
        'on' : ' autocomplete="on"',
        'off' : ' autocomplete="off"',
        'application/x-www-form-urlencoded' : ' enctype="application/x-www-form-urlencoded"',
        'multipart/form-data' : ' enctype="multipart/form-data"',
        'text/plain' : ' enctype="text/plain"',
        'get' : ' method="get"',
        'post' : ' method="post"',
        'novalidate' : ' novalidate="novalidate"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            defattrs += self.atom2attr.get( atom, u'' )
        return defattrs, atoms

    def specstrings2attrs( self, strings ):
        return u'action=%s' % strings[0] if strings else u''


class HtmlHead( TagPlugin ):
    """<head> tag handler.
    * '/string specifier/' is interpreted as //manifest// attribute and
      translates to //manifest=<string>//
    """
    pluginname = 'html5.head'
    def specstrings2attrs( self, strings ):
        return u'manifest=%s' % strings[0] if strings else u''


class HtmlHtml( TagPlugin ):
    """<html> tag handler.
    * '/string specifier/' is interpreted as //manifest// attribute and
      translates to //manifest=<string>//
    """
    pluginname = 'html5.html'
    def specstrings2attrs( self, strings ):
        return u'manifest=%s' % strings[0] if strings else u''


class HtmlIframe( TagPlugin ):
    """<frame> tag handler.
    * ''seamless'' atom translates to //seamless="seamless"//
    * If an atom is of the form //<width>,<height>// where width and height are
      integers, it translates to //width="<width>" height="<height>"//.
    * If an atoms starts with //allow-// it will be joined together as comma
      separated value to //sandbox// attribute.
    * '/string specifier/' is interpreted as //src// attribute and translates
      to //src=<string>//
    """
    pluginname = 'html5.iframe'
    atom2attr = {
        'seamless' : ' seamless="seamless"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        sandbox = []
        for atom in atoms :
            if atom.startswith( 'allow-' ) :
                sandbox.append( atom )
                continue
            s = self.atom2attr.get( atom, u'' )
            if s :
                defattrs += s
                continue
            try : defattrs += ' width="%s" height="%s"' % atom.split(',')
            except : pass
        defattrs += ( u' sandbox="%s"' % u','.join(sandbox) ) if sandbox else u''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'src=%s' % strings[0] if strings else u''

class HtmlImg( TagPlugin ):
    """<img> tag handler.
    * ''ismap'' atom translates to //ismap="ismap"//
    * If an atom is of the form //#<usemap>//, it translates to
      //usemap="<usemap>"//
    * If an atom is of the form //<width>,<height>// it translates to
      //width="<width>" height="<height>"//.
    * '/string specifier/' is interpreted as //src// attribute and translates
      to //src=<string>//
    """
    pluginname = 'html5.img'
    atom2attr = {
        'ismap' : ' ismap="ismap"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            if atom[0] == '#' :
                defattrs += u'usemap="%s"' % atom
                continue
            s = self.atom2attr.get( atom, u'' )
            if s :
                defattrs += s
                continue
            try : defattrs += u' width="%s" height="%s"' % tuple(atom.split(','))
            except : pass
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'src=%s' % strings[0] if strings else u''


class HtmlIns( TagPlugin ):
    """<ins> tag handler.
    * If any atom is present it will interpreted as //datetime// attribute and
      translates to //datetime="<atom>"//
    * '/string specifier/' is interpreted as //cite// attribute and translates
      to //cite=<string>//
    """
    pluginname = 'html5.ins'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' datetime="%s"'+atoms[0] if atoms else u''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'cite=%s' % strings[0] if strings else u''

class HtmlLabel( TagPlugin ):
    """<label> tag handler.
    * If an atom looks like //f:<formname>//, it will be translated to
      //form="<formname>"//
    * Otherwise the atom will be translated to //for="<atom>"//
    """
    pluginname = 'html5.label'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        forel = u''
        for atom in atoms :
            if atom.startswith( 'f:' ) :
                defattrs += u' form="%s"' % atom
            else :
                forel += u' for="%s"' % atom
        defattrs += forel
        return defattrs, []

class HtmlLi( TagPlugin ):
    """<li> tag handler
    * If an atom is present it will be translated to //value="<atom>"//
    """
    pluginname = 'html5.li'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' value="%s"' % atoms[0].strip() if atoms else u''
        return defattrs, []

class HtmlLink( TagPlugin ):
    """<link> tag handler
    * If an atom is present it will be translated to //type="<atom>"//
    * '/string specifier/' is interpreted as //href// attribute and translated
      as //href=<string>//
    """
    pluginname = 'html5.link'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' type="%s"' % atoms[0].strip() if atoms else u''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'href=%s' % strings[0] if strings else u''

class HtmlMenu( TagPlugin ):
    """<menu> tag handler
    * If an atom is present it will be translated to //type="<atom>"//
    * '/string specifier/' is interpreted as //label// attribute and translated
      as //label=<string>//
    """
    pluginname = 'html5.menu'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' type="%s"' % atoms[0] if atoms else u''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'label=%s' % strings[0] if strings else u''

class HtmlMeta( TagPlugin ):
    """<meta> tag handler
    * If an atom is present it will be translated to //http-equiv="<atom>"//
    * '/string specifier/' is interpreted as //content// attribute and translated
      as //content=<string>//
    """
    pluginname = 'html5.meta'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' http-equiv="%s"' % atoms[0] if atoms else u''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'content="%s"' % strings[0] if strings else u''

class HtmlMeter( TagPlugin ):
    """<meter> tag hanler
    * If an atom starts with //f:<formname>// it will be translated to
      //form="<formname>"//
    * If an atom is of the form //low < high// it will be translated to
      //low="<low>" high="<high>"//
    * If an atom is of the form //low < optimum < high// it will be translated
      to //low="<low>" optimum="<optimum>" high="<high>"//
    * Otherwise the atom will be interpreted as //value// attribute and
      translated as //value="<value>"//
    """
    pluginname = 'html5.meter'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        value = None
        for atom in atoms :
            if atom.startswith('f:') :
                defattrs += u' form="%s"' % form.replace(',', ' ')
                continue
            try :
                parts = atom.split('<')
                if len(parts) == 3 :
                    defattrs += u' low="%s" optimum="%s" high="%s"' % parts
                elif len(parts) == 2 :
                    defattrs += u' low="%s" high="%s"' % parts
                continue
            except:
                pass
            try :
                defattrs += u' min="%s" max="%s"' % atom.split('/')
                continue
            except :
                pass
            value = atom
        defattrs += u' value="%s"' % value if value else u''
        return defattrs, []


class HtmlObject( TagPlugin ):
    """<object> tag handler
    * If an atom starts with //form:<formname>// it will be translated to
      //form="<formname>"//
    * If an atom is of the form //<width>,<height>// it will translated to
      //width="<width>" height="<height>"//.
    * '/string specifier/' is interpreted as //data// attribute and translated
      as //data=<string>//
    """
    pluginname = 'html5.object'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atom :
            if atom.startswith( 'form:' ) :
                defattrs += u' form="%s"' % form.replace(',', ' ')
                continue
            try :
                defattrs += u' width="%s" height="%s"' % atom.split(',')
                continue
            except:
                pass
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'data=%s' % strings[0] if strings else u''

class HtmlOl( TagPlugin ):
    """<ol> tag handler
    * ''reversed'' atom translates to //reversed="reversed"//
    * ''1'' atom translates to //type="1"//
    * ''A'' atom translates to //type="A"//
    * ''a'' atom translates to //type="a"//
    * ''l'' atom translates to //type="l"//
    * ''i'' atom translates to //type="i"//
    * If atom is of the form //<type>,<start>//, it will be translated to
      //type="<type>" start="<start>"//
    """
    pluginname = 'html5.ol'
    atom2attr = {
        'reversed' : ' reversed="reversed"',
        '1' : ' type="1"',
        'A' : ' type="A"',
        'a' : ' type="a"',
        'l' : ' type="l"',
        'i' : ' type="i"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            try :
                parts = atom.split(',')
                if len(parts) == 2 :
                    defattrs += u' type="%s" start="%s"' % parts
                else :
                    defattrs += self.atom2attr.get( parts[0], u'' )
            except :
                pass
        return defattrs, []


class HtmlOptgroup( TagPlugin ):
    """<optgroup> tag handler
    * '/string specifier/' is interpreted as //label// attribute and translated
      as //label=<string>//
    """
    pluginname = 'html5.optgroup'
    def specstrings2attrs( self, strings ):
        return u'label=%s' % strings[0] if strings else u''


class HtmlOption( TagPlugin ):
    """<option> tag handler
    * '/string specifier/' is interpreted as //value// attribute and translated
      as //value=<string>//
    """
    pluginname = 'html5.option'
    def specstrings2attrs( self, strings ):
        return u'value=%s' % strings[0] if strings else u''


class HtmlOutput( TagPlugin ):
    """<output> tag handler
    * If atom is of the form //<form>:<name>// it will be translated to
      //form="<form>" for="<name>"//
    """
    pluginname = 'html5.output'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        if atoms :
            try : 
                form, forel = atoms[0].split(':')
                defattrs += u' form="%s" for="%s"' % (form.replace(',', ' '), forel)
            except:
                pass
        return defattrs, []


class HtmlParam( TagPlugin ):
    """<param> tag handler
    * If an atom is present it will be interpreted as //value// attribute and
    translated to //value="<value>"//
    * '/string specifier/' is interpreted as //value// attribute and translated
      as //value=<string>//
    """
    pluginname = 'html5.param'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' value="%s"' % atoms[0] if atoms else None
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'value=%s' % strings[0] if strings else u''


class HtmlProgress( TagPlugin ):
    """<progress> tag handler
    * If atom is of the form //<max>,<value>// it will be translated to
      //max="<max>" value="<value>"//
    """
    pluginname = 'html5.progress'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        if atoms :
            try : defattrs += u' max="%s" value="%s"' % atoms.split(',')
            except : pass
        return defattrs, []

class HtmlQ( TagPlugin ):
    """<q> tag handler
    * '/string specifier/' is interpreted as //cite// attribute and translated
      as //cite=<string>//
      """
    pluginname = 'html5.q'
    def specstrings2attrs( self, strings ):
        return u'cite=%s' % strings[0] if strings else u''


class HtmlScript( TagPlugin ):
    """<script> tag handler
    * ''async'' atom translates to //async="async"//
    * ''defer'' atom translates to //defer="defer"//
    * Otherwise it will be interpreted as //type// attribute and translated 
      as //type="<atom>"//
    * '/string specifier/' is interpreted as //src// attribute and translated
      as //src=<string>//
    """
    pluginname = 'html5.script'
    atom2attr = {
        'async' : ' async="async"',
        'defer' : ' defer="defer"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        type_ = None
        for atom in atoms :
            x = self.atom2attr.get( atom, u'' )
            if x :
                defattrs += x
                continue
            else :
                type_ = atom
        defattrs += u' type="%s"' % type_ if type_ else u''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'src=%s' % strings[0] if strings else u''


class HtmlSource( TagPlugin ):
    """<source> tag handler
    * If an atom is present it will be interpreted as //type// attribute and
      translated as //type="<atom>"//
    * '/string specifier/' is interpreted as //src// attribute and translated
      as //src=<string>//
    """
    pluginname = 'html5.source'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' type=%s"' % atoms[0] if atoms else u''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'src=%s' % strings[0] if strings else u''


class HtmlStyle( TagPlugin ):
    """<style> tag handler
    * ''text/css'' atom translates to //type="text/css"//
    * ''scoped'' atom translates to //scoped="scoped"//
    """
    pluginname = 'html5.style'
    atom2attr = {
        'text/css' : ' type="text/css"',
        'scoped'   : ' scoped="scoped"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            defattrs += self.atom2attr.get( atom, u'')
        return defattrs, []


class HtmlTable( TagPlugin ):
    """<table> tag handler
    * ''1'' atom translates to //border="1"//
    """
    pluginname = 'html5.table'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' border="1"' if atoms else u''
        return defattrs, []


class HtmlTime( TagPlugin ):
    """<time> tag handler
    * If an atom is present it will be interpreted as //pubdate// attribute and
      translated as //pubdate="<atom>"//
    * '/string specifier/' is interpreted as //datetime// attribute and translated
      as //datetime=<string>//
    """
    pluginname = 'html5.time'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += u' pubdate="%s"' % atoms[0] if atom else u''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return u'datetime=%s' % strings[0] if strings else u''

for k,cls in globals().items() :
    if k.startswith( 'Html' ) :
        gsm.registerUtility( cls(), ITayraTag, cls.pluginname )
