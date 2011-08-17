from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.ttl.tags       import TagPlugin
from   tayra.ttl.interfaces import ITayraTag

gsm = getGlobalSiteManager()

class HtmlA( TagPlugin ):
    tagname = 'html5.a'
    def specstrings2attrs( self, strings ):
        return 'href=%s' % strings[0]


class HtmlAbbr( TagPlugin ):
    tagname = 'html5.abbr'
    def specstrings2attrs( self, strings ):
        return 'title=%s' % strings[0]


class HtmlArea( TagPlugin ):
    tagname = 'html5.area'
    def specstrings2attrs( self, strings ):
        return 'href=%s' % strings[0]

    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            try :
                shape, coords = atom.split(':', 1)
                defattrs += ' shape="%s" coords="%s"' % (shape, coords)
                break
            except : 
                pass
        return defattrs, []


class HtmlAudio( TagPlugin ):
    tagname = 'html5.audio'
    atom2attr = {
        'autoplay' : ' autoplay="autoplay"',
        'controls' : ' controls="controls"',
        'loop' : ' loop="loop"',
        'auto' : ' preload="auto"',
        'metadata' : ' preload="metadata"',
        'none' : ' preload="none"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ''.join([ self.atom2attr.get(x, '') for x in atoms ])
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'src=%s' % strings[0]


class HtmlBase( TagPlugin ):
    tagname = 'html5.base'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' target="%s"'%atoms[0] if atoms else ' '
        return defattrs


class HtmlBlockquote( TagPlugin ):
    tagname = 'html5.blockquote'
    def specstrings2attrs( self, strings ):
        return 'cite=%s' % strings[0]


class HtmlButton( TagPlugin ):
    tagname = 'html5.button'
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
            attr = atom2attr.get( atom, None )
            if attr != None :
                defattrs += attr
                continue
            if atom.startswith( 'frame:' ):
                defattrs += ' frametarget="%s"' % atom[6:]
                continue
            if atom.startswith( 'form:' ):
                defattrs += ' form="%s"' % atom[5:].replace(',', ' ')
                continue
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'formaction=%s' % strings[0]
         

class HtmlCanvas( TagPlugin ):
    tagname = 'html5.canvas'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        try :
            defattrs += ' width="%s" height="%s"' % atoms[0].split(',')
        except :
            pass
        return defattrs, []


class HtmlCol( TagPlugin ):
    tagname = 'html5.col'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs = ' span="%s"' % atoms[0] if atoms else ''
        return defattrs, []


class HtmlColgroup( TagPlugin ):
    tagname = 'html5.colgroup'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs = ' span="%s"' % atoms[0] if atoms else ''
        return defattrs, []

class HtmlCommand( TagPlugin ):
    tagname = 'html5.command'
    atom2attr = {
        'checkbox' : ' type="checkbox"',
        'command' : ' type="command"',
        'radio' : ' type="radio"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += atom2attr[atoms[0]] if atoms else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'icon=%s' % strings[0]


class HtmlDel( TagPlugin ):
    tagname = 'html5.del'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' datetime="%s"'+atoms[0] if atoms else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'cite=%s' % strings[0]

class HtmlDetails( TagPlugin ):
    tagname = 'html5.details'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' open="open"' if atoms else ''
        return defattrs, []


class HtmlEmbed( TagPlugin ):
    tagname = 'html5.embed'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        try :
            defattrs += ' width="%s" height="%s"' % atoms[0].split(',') if atoms else ''
        except :
            pass
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'src=%s' % strings[0]


class HtmlFieldset( TagPlugin ):
    tagname = 'html5.fieldset'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            if atom.startwith( 'form:' ):
                defattrs += ' form="%s"' % atom.replace(',', ' ')
                continue
        return defattrs, []


class HtmlForm( TagPlugin ):
    tagname = 'html5.form'
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
            defattrs = self.atom2attr.get( atom, '' )
        return defattrs, atoms

    def specstrings2attrs( self, strings ):
        return 'action=%s' % strings[0]


class HtmlHtml( TagPlugin ):
    tagname = 'html5.html'
    def specstrings2attrs( self, strings ):
        return 'manifest=%s' % strings[0]


class HtmlIframe( TagPlugin ):
    tagname = 'html5.iframe'
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
            try :
                defattrs += ' width="%s" height="%s"' % atom.split(',')
            except :
                defattrs += self.atom2attr.get( atom, '' )
        defattrs += ' sandbox="%s"' % ','.join(sandbox) if sandbox else None
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'src=%s' % strings[0]

class HtmlImg( TagPlugin ):
    tagname = 'html5.img'
    atom2attr = {
        'ismap' : ' ismap="ismap"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            if atom[0] == '#' :
                defattrs += 'usemap="%s"' % atom
                continue
            try :
                defattrs += ' width="%s" height="%s"' % tuple(atom.split(','))
            except :
                defattrs += self.atom2attr.get( atom, '' )
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'src=%s' % strings[0]


class HtmlIns( TagPlugin ):
    tagname = 'html5.ins'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' datetime="%s"'+atoms[0] if atoms else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'cite=%s' % strings[0]

class HtmlLabel( TagPlugin ):
    tagname = 'html5.label'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        if atoms :
            try : 
                form, forel = atoms[0].split(':')
                defattrs += ' form="%s" for="%s"' % (form.replace(',', ' '), forel)
            except:
                pass
        return defattrs, []

class HtmlLi( TagPlugin ):
    tagname = 'html5.li'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        if atoms :
            try : defattrs = ' value="%s"' % atoms[0]
            except : pass
        return defattrs, []

class HtmlLink( TagPlugin ):
    tagname = 'html5.link'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        if atoms :
            defattrs += ' type="%s"' % atoms[0].strip()
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'href=%s' % strings[0]

class HtmlMenu( TagPlugin ):
    tagname = 'html5.menu'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' type="%s"' % atoms[0] if atoms else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'label=%s' % strings[0]

class HtmlMeta( TagPlugin ):
    tagname = 'html5.meta'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' http-equiv="%s"' % atoms[0] if atoms else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'content="%s"' % strings[0]

class HtmlMeter( TagPlugin ):
    tagname = 'html5.meter'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        value = None
        for atom in atoms :
            if atom.startswith('form:') :
                defattrs = ' form="%s"' % form.replace(',', ' ')
                continue
            try :
                parts = atom.split('<')
                if len(parts) == 3 :
                    defattrs += ' high="%s" optimum="%s" low="%s"' % parts
                elif len(parts) == 2 :
                    defattrs += ' high="%s" low="%s"' % parts
                continue
            except:
                pass
            try :
                defattrs += ' min="%s" max="%s"' % atom.split('/')
                continue
            except :
                pass
            value = atom
        defattrs += ' value="%s"' % value if value else ''
        return defattrs, []


class HtmlObject( TagPlugin ):
    tagname = 'html5.object'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atom :
            if atom.startswith( 'form:' ) :
                defattrs = ' form="%s"' % form.replace(',', ' ')
                continue
            try :
                defattrs += ' width="%s" height="%s"' % atom.split(',')
                continue
            except:
                pass
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'data=%s' % strings[0]

class HtmlOl( TagPlugin ):
    tagname = 'html5.ol'
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
                    defattrs += ' type="%s" start="%s"' % parts
                else :
                    defattrs += self.atom2attr.get( parts[0], '' )
            except :
                pass
        return defattrs, []


class HtmlOptgroup( TagPlugin ):
    tagname = 'html5.optgroup'
    def specstrings2attrs( self, strings ):
        return 'label=%s' % strings[0]


class HtmlOption( TagPlugin ):
    tagname = 'html5.option'
    def specstrings2attrs( self, strings ):
        return 'value=%s' % strings[0]


class HtmlOutput( TagPlugin ):
    tagname = 'html5.output'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        if atoms :
            try : 
                form, forel = atoms[0].split(':')
                defattrs += ' form="%s" for="%s"' % (form.replace(',', ' '), forel)
            except:
                pass
        return defattrs, []


class HtmlParam( TagPlugin ):
    tagname = 'html5.param'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' value="%s"' % atoms[0] if atoms else None
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'value=%s' % strings[0]


class HtmlProgress( TagPlugin ):
    tagname = 'html5.progress'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        if atoms :
            try : defattrs += ' max="%s" value="%s"' % atoms.split(',')
            except : pass
        return defattrs, []

class HtmlQ( TagPlugin ):
    tagname = 'html5.q'
    def specstrings2attrs( self, strings ):
        return 'cite=%s' % strings[0]


class HtmlScript( TagPlugin ):
    tagname = 'html5.script'
    atom2attr = {
        'async' : ' async="async"',
        'defer' : ' defer="defer"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        type_ = None
        for atom in atoms :
            x = self.atom2attr.get( atom, '' )
            if x :
                defattrs += x
                continue
            else :
                type_ = atom
        defattrs += ' type="%s"' % type_ if type_ else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'src=%s' % strings[0]


class HtmlSource( TagPlugin ):
    tagname = 'html5.source'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' type=%s"' % atoms[0] if atoms else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'src=%s' % strings[0]


class HtmlStyle( TagPlugin ):
    tagname = 'html5.style'
    atom2attr = {
        'text/css' : ' type="text/css"',
        'scoped'   : ' scoped="scoped"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            defattrs += self.atom2attr.get( atom, '')
        return defattrs, []


class HtmlTable( TagPlugin ):
    tagname = 'html5.table'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' border="1"' % atoms[0] if atoms else ''
        return defattrs, []


class HtmlTime( TagPlugin ):
    tagname = 'html5.time'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' pubdate="%s"' % atoms[0] if atom else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'datetime=%s' % strings[0]

for k,cls in globals().items() :
    if k.startswith( 'Html' ) :
        gsm.registerUtility( cls(), ITayraTag, cls.tagname )
