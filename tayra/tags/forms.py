"""The following HTML5 elements pertain to browser form handling,
    <keygen>
    <button>,   <datalist>,
    <fieldset>, <legend>,   <form>
    <input>,    <label>,    <optgroup>, <option>    <select>    <textarea>
"""

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
#       [list], +pattern+, h:placeholder, f:form, a:formaction,
#       min < step < max
#       maxlength:size
#       height,width
reglist = r'(\[[^ ]*?\])'
regpatt = r'(`[^`]*?`)|(%[^%]*?%)'
reghelp = r'(h:"[^"]*?")|(h:\'[^\']*?\')'
regform = r'(f:[^ ]*?)'
regactn = r'(a:[^ ]*?)'
regrang = r'([0-9]*<[0-9]*)|([0-9]*<[0-9]*<[0-9]*)'
reglen  = r'([0-9]*:[0-9]*)'
regport = r'([0-9%]*,[0-9%]*)'
regint  = r'([0-9]*)'
regexp = re.compile( r"%s|%s|%s|%s|%s|%s" % (
    reglist, regpatt, regform, regrang, reglen, regport
))
handlers = [
    lambda x : ' list="%s"'         % x[1:-1],
    lambda x : ' pattern="%s"'      % x[1:-1],
    lambda x : ' pattern="%s"'      % x[1:-1],
#   lambda x : ' placeholder=%s'    % x[2:],
#   lambda x : ' placeholder="%s"'  % x[3:-1],
    lambda x : ' form="%s"'         % x[2:],
#   lambda x : ' formaction="%s"'   % x[2:],
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
        return 'value=%s' % strings[0] if strings else ''

    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        rematoms = []
        for atom in atoms :
            s = _atom2attrs.get( atom, '' )
            if s : defattrs += s
            else : rematoms.append( atom )

        rematoms = ' '.join( rematoms )
        matches = regexp.findall( rematoms )
        for match in matches :
            for i in range(8) :
                if not match[i] : continue
                try : defattrs += handlers[i]( match[i] )
                except : continue
                break
        defattrs += typeattrs.get( self.pluginname[12:], '' )
        return defattrs, []

    def maketagname( self, tagopen ):
        return 'input'


class HtmlInpbutton( TagInput ):
    pluginname = 'html5.forms.inpbutton'

class HtmlInpchk( TagInput ):
    pluginname = 'html5.forms.inpchk'

class HtmlInpcolor( TagInput ):
    pluginname = 'html5.forms.inpcolor'

class HtmlInpdate( TagInput ):
    pluginname = 'html5.forms.inpdate'

class HtmlInpdt( TagInput ):
    pluginname = 'html5.forms.inpdt'

class HtmlInpdtlocal( TagInput ):
    pluginname = 'html5.forms.inpdtlocal'

class HtmlInpemail( TagInput ):
    pluginname = 'html5.forms.inpemail'

class HtmlInpfile( TagInput ):
    pluginname = 'html5.forms.inpfile'

class HtmlInphidden( TagInput ):
    pluginname = 'html5.forms.inphidden'

class HtmlInpimg( TagInput ):
    pluginname = 'html5.forms.inpimg'
    def specstrings2attrs( self, strings ):
        return 'src=%s' % strings[0] if strings else ''

class HtmlInpmonth( TagInput ):
    pluginname = 'html5.forms.inpmonth'

class HtmlInpnum( TagInput ):
    pluginname = 'html5.forms.inpnum'

class HtmlInppass( TagInput ):
    pluginname = 'html5.forms.inppass'

class HtmlInpradio( TagInput ):
    pluginname = 'html5.forms.inpradio'

class HtmlInprange( TagInput ):
    pluginname = 'html5.forms.inprange'

class HtmlInpreset( TagInput ):
    pluginname = 'html5.forms.inpreset'

class HtmlInpsearch( TagInput ):
    pluginname = 'html5.forms.inpsearch'

class HtmlInpsub( TagInput ):
    pluginname = 'html5.forms.inpsub'

class HtmlInptel( TagInput ):
    pluginname = 'html5.forms.inptel'

class HtmlInptext( TagInput ):
    pluginname = 'html5.forms.inptext'

class HtmlInptime( TagInput ):
    pluginname = 'html5.forms.inptime'

class HtmlInpurl( TagInput ):
    pluginname = 'html5.forms.inpurl'

class HtmlInpweek( TagInput ):
    pluginname = 'html5.forms.inpweek'


ta_regexp = re.compile( r"%s|%s|%s|%s" % (reghelp, regform, regint, regport))
ta_handlers = [
    lambda x : ' placeholder=%s'    % x[2:],
    lambda x : ' placeholder="%s"'  % x[3:-1],
    lambda x : ' form="%s"'         % x[2:],
    lambda x : ' maxlength="%s"'    % int(x),
    lambda x : ' cols="%s" rows="%s"' % x.split(',', 1)
]

class HtmlTextArea( TagPlugin ):
    pluginname = 'html5.forms.textarea'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        rematoms = []
        for atom in atoms :
            s = _atom2attrs.get( atom, '' )
            if s : defattrs += s
            else : rematoms.append( atom )

        rematoms = ' '.join( rematoms )
        matches = ta_regexp.findall( rematoms )
        for match in matches :
            for i in range(8) :
                if not match[i] : continue
                try : defattrs += ta_handlers[i]( match[i] )
                except : continue
                break
        return defattrs, []

class HtmlSelect( TagPlugin ):
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

for k,cls in globals().items() :
    if k.startswith( 'Html' ) :
        gsm.registerUtility( cls(), ITayraTag, cls.pluginname )
