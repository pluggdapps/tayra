from   zope.component       import getGlobalSiteManager
from   zope.interface       import implements

from   tayra.ttl.tags       import TagPlugin
from   tayra.ttl.interfaces import ITayraTag

gsm = getGlobalSiteManager()

class HtmlA( TagPlugin ):
    pluginname = 'html5.a'
    def specstrings2attrs( self, strings ):
        return 'href=%s' % strings[0] if strings else ''


class HtmlAbbr( TagPlugin ):
    pluginname = 'html5.abbr'
    def specstrings2attrs( self, strings ):
        return 'title=%s' % strings[0] if strings else ''


class HtmlArea( TagPlugin ):
    pluginname = 'html5.area'
    def specstrings2attrs( self, strings ):
        return 'href=%s' % strings[0] if strings else ''

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
        return 'src=%s' % strings[0] if strings else ''

    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ''.join([ self.atom2attr.get(x, '') for x in atoms ])
        return defattrs, []


class HtmlBase( TagPlugin ):
    pluginname = 'html5.base'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' target="%s"'%atoms[0] if atoms else ' '
        return defattrs


class HtmlBlockquote( TagPlugin ):
    pluginname = 'html5.blockquote'
    def specstrings2attrs( self, strings ):
        return 'cite=%s' % strings[0] if strings else ''


class HtmlButton( TagPlugin ):
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
        return 'formaction=%s' % strings[0] if strings else ''
         

class HtmlCanvas( TagPlugin ):
    pluginname = 'html5.canvas'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            try : defattrs += ' width="%s" height="%s"' % atom.split(',')
            except : pass
        return defattrs, []


class HtmlCol( TagPlugin ):
    pluginname = 'html5.col'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' span="%s"' % atoms[0] if atoms else ''
        return defattrs, []


class HtmlColgroup( TagPlugin ):
    pluginname = 'html5.colgroup'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' span="%s"' % atoms[0] if atoms else ''
        return defattrs, []

class HtmlCommand( TagPlugin ):
    pluginname = 'html5.command'
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
        return 'icon=%s' % strings[0] if strings else ''


class HtmlDel( TagPlugin ):
    pluginname = 'html5.del'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' datetime="%s"'+atoms[0] if atoms else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'cite=%s' % strings[0] if strings else ''

class HtmlDetails( TagPlugin ):
    pluginname = 'html5.details'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' open="open"' if atoms else ''
        return defattrs, []


class HtmlEmbed( TagPlugin ):
    pluginname = 'html5.embed'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            try : defattrs += ' width="%s" height="%s"' % atom.split(',')
            except : pass
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'src=%s' % strings[0] if strings else ''


class HtmlFieldset( TagPlugin ):
    pluginname = 'html5.fieldset'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            if atom.startwith( 'f:' ):
                defattrs += ' form="%s"' % atom.replace(',', ' ')
                continue
        return defattrs, []


class HtmlForm( TagPlugin ):
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
            defattrs += self.atom2attr.get( atom, '' )
        return defattrs, atoms

    def specstrings2attrs( self, strings ):
        return 'action=%s' % strings[0] if strings else ''


class HtmlHtml( TagPlugin ):
    pluginname = 'html5.html'
    def specstrings2attrs( self, strings ):
        return 'manifest=%s' % strings[0] if strings else ''


class HtmlIframe( TagPlugin ):
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
            s = self.atom2attr.get( atom, '' )
            if s :
                defattrs += s
                continue
            try : defattrs += ' width="%s" height="%s"' % atom.split(',')
            except : pass
        defattrs += ' sandbox="%s"' % ','.join(sandbox) if sandbox else None
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'src=%s' % strings[0] if strings else ''

class HtmlImg( TagPlugin ):
    pluginname = 'html5.img'
    atom2attr = {
        'ismap' : ' ismap="ismap"',
    }
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atoms :
            if atom[0] == '#' :
                defattrs += 'usemap="%s"' % atom
                continue
            s = self.atom2attr.get( atom, '' )
            if s :
                defattrs += s
                continue
            try : defattrs += ' width="%s" height="%s"' % tuple(atom.split(','))
            except : pass
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'src=%s' % strings[0] if strings else ''


class HtmlIns( TagPlugin ):
    pluginname = 'html5.ins'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' datetime="%s"'+atoms[0] if atoms else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'cite=%s' % strings[0] if strings else ''

class HtmlLabel( TagPlugin ):
    pluginname = 'html5.label'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        forel = ''
        for atom in atoms :
            if atom.startswith( 'f:' ) :
                defattrs += ' form="%s"' % atom
            else :
                forel += ' for="%s"' % atom
        defattrs += forel
        return defattrs, []

class HtmlLi( TagPlugin ):
    pluginname = 'html5.li'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        if atoms :
            try : defattrs += ' value="%s"' % atoms[0]
            except : pass
        return defattrs, []

class HtmlLink( TagPlugin ):
    pluginname = 'html5.link'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' type="%s"' % atoms[0].strip() if atoms else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'href=%s' % strings[0] if strings else ''

class HtmlMenu( TagPlugin ):
    pluginname = 'html5.menu'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' type="%s"' % atoms[0] if atoms else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'label=%s' % strings[0] if strings else ''

class HtmlMeta( TagPlugin ):
    pluginname = 'html5.meta'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' http-equiv="%s"' % atoms[0] if atoms else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'content="%s"' % strings[0] if strings else ''

class HtmlMeter( TagPlugin ):
    pluginname = 'html5.meter'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        value = None
        for atom in atoms :
            if atom.startswith('f:') :
                defattrs += ' form="%s"' % form.replace(',', ' ')
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
    pluginname = 'html5.object'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        for atom in atom :
            if atom.startswith( 'form:' ) :
                defattrs += ' form="%s"' % form.replace(',', ' ')
                continue
            try :
                defattrs += ' width="%s" height="%s"' % atom.split(',')
                continue
            except:
                pass
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'data=%s' % strings[0] if strings else ''

class HtmlOl( TagPlugin ):
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
                    defattrs += ' type="%s" start="%s"' % parts
                else :
                    defattrs += self.atom2attr.get( parts[0], '' )
            except :
                pass
        return defattrs, []


class HtmlOptgroup( TagPlugin ):
    pluginname = 'html5.optgroup'
    def specstrings2attrs( self, strings ):
        return 'label=%s' % strings[0] if strings else ''


class HtmlOption( TagPlugin ):
    pluginname = 'html5.option'
    def specstrings2attrs( self, strings ):
        return 'value=%s' % strings[0] if strings else ''


class HtmlOutput( TagPlugin ):
    pluginname = 'html5.output'
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
    pluginname = 'html5.param'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' value="%s"' % atoms[0] if atoms else None
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'value=%s' % strings[0] if strings else ''


class HtmlProgress( TagPlugin ):
    pluginname = 'html5.progress'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        if atoms :
            try : defattrs += ' max="%s" value="%s"' % atoms.split(',')
            except : pass
        return defattrs, []

class HtmlQ( TagPlugin ):
    pluginname = 'html5.q'
    def specstrings2attrs( self, strings ):
        return 'cite=%s' % strings[0] if strings else ''


class HtmlScript( TagPlugin ):
    pluginname = 'html5.script'
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
        return 'src=%s' % strings[0] if strings else ''


class HtmlSource( TagPlugin ):
    pluginname = 'html5.source'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' type=%s"' % atoms[0] if atoms else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'src=%s' % strings[0] if strings else ''


class HtmlStyle( TagPlugin ):
    pluginname = 'html5.style'
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
    pluginname = 'html5.table'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' border="1"' % atoms[0] if atoms else ''
        return defattrs, []


class HtmlTime( TagPlugin ):
    pluginname = 'html5.time'
    def specatoms2attrs( self, atoms ):
        defattrs, atoms = TagPlugin.specatoms2attrs( self, atoms )
        defattrs += ' pubdate="%s"' % atoms[0] if atom else ''
        return defattrs, []

    def specstrings2attrs( self, strings ):
        return 'datetime=%s' % strings[0] if strings else ''

for k,cls in globals().items() :
    if k.startswith( 'Html' ) :
        gsm.registerUtility( cls(), ITayraTag, cls.pluginname )
