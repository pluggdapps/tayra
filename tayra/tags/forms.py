# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2011 SKR Farms (P) LTD.

"""The following HTML5 elements pertain to browser form handling,
    <keygen>
    <button>,   <datalist>,
    <fieldset>, <legend>,   <form>
    <input>,    <label>,    <optgroup>, <option>    <select>    <textarea>
"""

# -*- coding: utf-8 -*-

import re

from   zope.component   import getGlobalSiteManager
from   zope.interface   import implements

from   tayra.tags       import TagPlugin
from   tayra.interfaces import ITayraTag

gsm = getGlobalSiteManager()

_atom2attrs = {
    'on' : ' autocomplete="on"',
    'off' : ' autocomplete="off"',
    'autofocus' : ' autofocus="autofocus"',
    'application/x-www-form-urlencoded' : ' enctype="application/x-www-form-urlencoded"',
    'multipart/form-data' : ' enctype="multipart/form-data"',
    'text/plain' : ' enctype="text/plain"',
    'get' : ' formmethod="get"',
    'post' : ' formmethod="post"',
    'novalidate' : ' formnovalidate="novalidate"',
    'required' : ' required="required"',
    'checked' : ' checked="checked"',
    'hard' : ' wrap="hard"',
    'soft' : ' wrap="soft"',
}

# some more of the attributes
#       [list], `pattern`, %pattern%, h:placeholder, f:form, a:formaction,
#       min < step < max
#       maxlength:size
#       height,width
reglist = r'(\[[^ ]*?\])'
regpatt = r'(`[^`]*?`)|(%[^%]*?%)'
reghelp = r'(h:[^ ]*?)'
regform = r'(f:[^ ]*?)'
regactn = r'(a:[^ ]*?)'
regrang = r'([0-9]*<[0-9]*)|([0-9]*<[0-9]*<[0-9]*)'
reglen  = r'([0-9]*:[0-9]*)'
regport = r'([0-9%]*,[0-9%]*)'
regint  = r'([0-9]*)'
regexp = re.compile( r"%s|%s|%s|%s|%s|%s|%s|%s" % (
    reglist, regpatt, reghelp, regform, regactn, regrang, reglen, regport
))
handlers = [
    lambda x : ' list="%s"'         % x[1:-1],
    lambda x : ' pattern="%s"'      % x[1:-1],
    lambda x : ' pattern="%s"'      % x[1:-1],
    lambda x : ' placeholder="%s"'  % x[3:-1].replace('+', ' '),
    lambda x : ' form="%s"'         % x[2:],
    lambda x : ' formaction="%s"'   % x[2:].replace('+', ' '),
    lambda x : ' min="%s" step="%s" max="%s"' % x.split('<', 2),
    lambda x : ' min="%s" max="%s"' % x.split('<', 1),
    lambda x : ' maxlength="%s" size="%s"' % x.split(':', 1),
    lambda x : ' height="%s" width="%s"' % x.split(',', 1),
]

typeattrs = {
    'inpbutton' : ' type="button"',
    'inpchk'    : ' type="checkbox"',
    'inpcolor'  : ' type="color"',
    'inpdate'   : ' type="date"',
    'inpdt'     : ' type="datetime"',
    'inplocal'  : ' type="datetime-local"',
    'inpemail'  : ' type="email"',
    'inpfile'   : ' type="file"',
    'inphidden' : ' type="hidden"',
    'inpimg'    : ' type="image"',
    'inpmonth'  : ' type="month"',
    'inpnum'    : ' type="number"',
    'inppass'   : ' type="password"',
    'inpradio'  : ' type="radio"',
    'inprange'  : ' type="range"',
    'inpreset'  : ' type="reset"',
    'inpsearch' : ' type="search"',
    'inpsub'    : ' type="submit"',
    'inptel'    : ' type="tel"',
    'inptext'   : ' type="text"',
    'inptime'   : ' type="time"',
    'inpurl'    : ' type="url"',
    'inpweek'   : ' type="week"',
}

class TagInput( TagPlugin ):
    def specstrings2attrs( self, strings ):
        return 'value=%s' % strings[0] if strings else u''

    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        rematoms = []
        for atom in atoms :
            s = _atom2attrs.get( atom, u'' )
            if s : defattrs += s
            else : rematoms.append( atom )

        rematoms = u' '.join( rematoms )
        matches = regexp.findall( rematoms )
        for match in matches :
            for i in range(8) :
                if not match[i] : continue
                try : defattrs += handlers[i]( match[i] )
                except : continue
                break
        defattrs += typeattrs.get( self.pluginname[12:], u'' )
        return defattrs, []

    def maketagname( self, tagopen ):
        return 'input'

_inputdoc = """
* ''on'' atom translates to //autocomplete="on"//
* ''off'' atom translates to //autocomplete="off"'//
* ''autofocus'' atom translates to //autofocus="autofocus"//
* ''application/x-www-form-urlencoded'' atom translates to
   //enctype="application/x-www-form-urlencoded"//
* ''multipart/form-data'' atom translates to
   //enctype="multipart/form-data"//
* ''text/plain'' atom translates to //enctype="text/plain"//
* ''get'' atom translates to //formmethod="get"//
* ''post'' atom translates to //formmethod="post"//
* ''novalidate'' atom translates to //formnovalidate="novalidate"//
* ''required'' atom translates to //required="required"//
* ''checked'' atom translates to //checked="checked"//
* ''hard'' atom translates to //wrap="hard"//
* ''soft'' atom translates to //wrap="soft"//
* If an atom is comma seperated items of the form, [item1,item2] will
  be interpreted as //list// attribute and translates to
  //list="item1,item2"//
* If an atom has the syntax, `pattern` or %pattern% it will be interpreted
  as //pattern// attribute and translates to //pattern="pattern"//
* If an atom is of the form //h:placeholder// it will be interpreted as
  //placeholder// attribute and translates to //placeholder="placeholder"//.
  If help string has several words seperated by white-space, replace spaces
  with //+// character. If help string is more complicated containing several
  special characters it is better to avoid //h:...// format and define them
  directly as an attribute.
* If an atom is of the form //f:formname// it will be translated to
  //form="formname"//
* If an atom is of the form //a:formaction// it will be translated to
  //formaction="formaction"//. If action-url contains white-spaces, replace
  them with //+// character.
* If an atom has the syntax //min<step<max// where min, step and max are
  integers, it translates to //min="min" step="step" max="max"//
* If an atom has the syntax //min<max// where min and max are integers, it
  translates to //min="min" max="max"//
* If an atom has the syntax //maxlength:size// where maxlength and size are
  integers, it translates to //maxlength="maxlength" size="size"//
* If an atom has the syntax //height,width// where height and width are
  integers, it translates to //height="height" width="width"//
* ''string specifier'' is interpreted as //value// attribute and translated
  as //value=<string>//
"""
class HtmlInpbutton( TagInput ):
    """<input type="button"> handler"""
    pluginname = 'html5.forms.inpbutton'

class HtmlInpchk( TagInput ):
    """<input type="check"> handler"""
    pluginname = 'html5.forms.inpchk'

class HtmlInpcolor( TagInput ):
    """<input type="color"> handler"""
    pluginname = 'html5.forms.inpcolor'

class HtmlInpdate( TagInput ):
    """<input type="date"> handler"""
    pluginname = 'html5.forms.inpdate'

class HtmlInpdt( TagInput ):
    """<input type="datetime"> handler"""
    pluginname = 'html5.forms.inpdt'

class HtmlInpdtlocal( TagInput ):
    """<input type="datetime-local"> handler"""
    pluginname = 'html5.forms.inpdtlocal'

class HtmlInpemail( TagInput ):
    """<input type="email"> handler"""
    pluginname = 'html5.forms.inpemail'

class HtmlInpfile( TagInput ):
    """<input type="file"> handler"""
    pluginname = 'html5.forms.inpfile'

class HtmlInphidden( TagInput ):
    """<input type="hidden"> handler"""
    pluginname = 'html5.forms.inphidden'

class HtmlInpimg( TagInput ):
    """<input type="image"> handler"""
    pluginname = 'html5.forms.inpimg'
    def specstrings2attrs( self, strings ):
        return 'src=%s' % strings[0] if strings else u''

class HtmlInpmonth( TagInput ):
    """<input type="month"> handler"""
    pluginname = 'html5.forms.inpmonth'

class HtmlInpnum( TagInput ):
    """<input type="number"> handler"""
    pluginname = 'html5.forms.inpnum'

class HtmlInppass( TagInput ):
    """<input type="password"> handler"""
    pluginname = 'html5.forms.inppass'

class HtmlInpradio( TagInput ):
    """<input type="radio"> handler"""
    pluginname = 'html5.forms.inpradio'

class HtmlInprange( TagInput ):
    """<input type="range"> handler"""
    pluginname = 'html5.forms.inprange'

class HtmlInpreset( TagInput ):
    """<input type="reset"> handler"""
    pluginname = 'html5.forms.inpreset'

class HtmlInpsearch( TagInput ):
    """<input type="search"> handler"""
    pluginname = 'html5.forms.inpsearch'

class HtmlInpsub( TagInput ):
    """<input type="submit"> handler"""
    pluginname = 'html5.forms.inpsub'

class HtmlInptel( TagInput ):
    """<input type="tel"> handler"""
    pluginname = 'html5.forms.inptel'

class HtmlInptext( TagInput ):
    """<input type="text"> handler"""
    pluginname = 'html5.forms.inptext'

class HtmlInptime( TagInput ):
    """<input type="time"> handler"""
    pluginname = 'html5.forms.inptime'

class HtmlInpurl( TagInput ):
    """<input type="url"> handler"""
    pluginname = 'html5.forms.inpurl'

class HtmlInpweek( TagInput ):
    """<input type="week"> handler"""
    pluginname = 'html5.forms.inpweek'

# Register plugin component
for k, cls in globals().items() :
    if k.startswith( 'HtmlInp' ) :
        obj = cls()
        obj.__doc__ = cls.__doc__ + _inputdoc
        gsm.registerUtility( obj, ITayraTag, obj.pluginname )

ta_regexp = re.compile( r"%s|%s|%s|%s" % (reghelp, regform, regint, regport))
ta_handlers = [
    lambda x : ' placeholder=%s'    % x[2:],
    lambda x : ' placeholder="%s"'  % x[3:-1],
    lambda x : ' form="%s"'         % x[2:],
    lambda x : ' maxlength="%s"'    % int(x),
    lambda x : ' cols="%s" rows="%s"' % x.split(',', 1)
]

class HtmlTextArea( TagPlugin ):
    """<textarea> handler
    * ''on'' atom translates to //autocomplete="on"//
    * ''off'' atom translates to //autocomplete="off"//
    * ''autofocus'' atom translates to //autofocus="autofocus"//
    * ''application/x-www-form-urlencoded'' atom translates to
       //enctype="application/x-www-form-urlencoded"//
    * ''multipart/form-data'' atom translates to
       //enctype="multipart/form-data"//
    * ''text/plain'' atom translates to //enctype="text/plain"//
    * ''get'' atom translates to //formmethod="get"//
    * ''post'' atom translates to //formmethod="post"//
    * ''novalidate'' atom translates to //formnovalidate="novalidate"//
    * ''required'' atom translates to //required="required"//
    * ''checked'' atom translates to //checked="checked"//
    * ''hard'' atom translates to //wrap="hard"//
    * ''soft'' atom translates to //wrap="soft"//
    * If an atom is of the form //h:placeholder// it will be interpreted as
      //placeholder// attribute and translates to //placeholder="placeholder"//.
      If help string has several words seperated by white-space, replace spaces
      with //+// character. If help string is more complicated containing several
      special characters it is better to avoid //h:...// format and define them
      directly as an attribute.
    * If an atom is of the form //f:formname// it translates to
      //form="formname"//
    * If an atom has the syntax //maxlength// where maxlength is an integer, 
      it translates to //maxlength="maxlength"//
    * If an atom has the syntax //cols,rows// where cols and rows are
      integers, it translates to //cols="cols" rows="rows"//
    """
    pluginname = 'html5.forms.textarea'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        rematoms = []
        for atom in atoms :
            s = _atom2attrs.get( atom, u'' )
            if s : defattrs += s
            else : rematoms.append( atom )

        rematoms = u' '.join( rematoms )
        matches = ta_regexp.findall( rematoms )
        for match in matches :
            for i in range(4) :
                if not match[i] : continue
                try : defattrs += ta_handlers[i]( match[i] )
                except : continue
                break
        return defattrs, []

class HtmlSelect( TagPlugin ):
    """<select> handler
    * ''autofocus'' atom translates to //autofocus="autofocus"//
    * If an atom is of the form //f:formname// it will be translated to
      //form="formname"//
    * Otherwise the atom is interpreted as integer //size//, and translates
      to //size="size"//
    """
    pluginname = 'html5.forms.select'
    atom2attr = {
        'autofocus' : ' autofocus="autofocus"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            try :
                defattrs = ' size="%s"' % int(atom)
                continue
            except :
                pass
            if atom.startswith('f:') :
                defattrs += ' form="%s"' % atom
        return defattrs, []

gsm.registerUtility( HtmlTextArea(), ITayraTag, HtmlTextArea.pluginname )
gsm.registerUtility( HtmlSelect(), ITayraTag, HtmlSelect.pluginname )
