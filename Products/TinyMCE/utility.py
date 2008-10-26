from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility
from zope.interface import classProvides
from AccessControl import ClassSecurityInfo

from Products.TinyMCE.libs import json
from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.interfaces.utility import ITinyMCELayout
from Products.TinyMCE.interfaces.utility import ITinyMCEToolbar
from Products.TinyMCE.interfaces.utility import ITinyMCELibraries
from Products.TinyMCE.interfaces.utility import ITinyMCEResourceTypes

from OFS.SimpleItem import SimpleItem

def form_adapter(context):
    """Form Adapter"""
    return getUtility(ITinyMCE)

class TinyMCE(SimpleItem):
    """TinyMCE Utility"""
    implements(ITinyMCE)
    classProvides(
        ITinyMCELayout,
        ITinyMCEToolbar,
        ITinyMCELibraries,
        ITinyMCEResourceTypes
        )
    security = ClassSecurityInfo()

    resizing = FieldProperty(ITinyMCELayout['resizing'])
    autoresize = FieldProperty(ITinyMCELayout['autoresize'])
    editor_width = FieldProperty(ITinyMCELayout['editor_width'])
    editor_height = FieldProperty(ITinyMCELayout['editor_height'])
    directionality = FieldProperty(ITinyMCELayout['directionality'])
    content_css = FieldProperty(ITinyMCELayout['content_css'])
    styles = FieldProperty(ITinyMCELayout['styles'])
    tablestyles = FieldProperty(ITinyMCELayout['tablestyles'])

    toolbar_width = FieldProperty(ITinyMCEToolbar['toolbar_width'])
    
    toolbar_external = FieldProperty(ITinyMCEToolbar['toolbar_external'])

    toolbar_save = FieldProperty(ITinyMCEToolbar['toolbar_save'])

    toolbar_cut = FieldProperty(ITinyMCEToolbar['toolbar_cut'])
    toolbar_copy = FieldProperty(ITinyMCEToolbar['toolbar_copy'])
    toolbar_paste = FieldProperty(ITinyMCEToolbar['toolbar_paste'])
    toolbar_pastetext = FieldProperty(ITinyMCEToolbar['toolbar_pastetext'])
    toolbar_pasteword = FieldProperty(ITinyMCEToolbar['toolbar_pasteword'])

    toolbar_undo = FieldProperty(ITinyMCEToolbar['toolbar_undo'])
    toolbar_redo = FieldProperty(ITinyMCEToolbar['toolbar_redo'])

    toolbar_search = FieldProperty(ITinyMCEToolbar['toolbar_search'])
    toolbar_replace = FieldProperty(ITinyMCEToolbar['toolbar_replace'])

    toolbar_style = FieldProperty(ITinyMCEToolbar['toolbar_style'])

    toolbar_bold = FieldProperty(ITinyMCEToolbar['toolbar_bold'])
    toolbar_italic = FieldProperty(ITinyMCEToolbar['toolbar_italic'])
    toolbar_underline = FieldProperty(ITinyMCEToolbar['toolbar_underline'])
    toolbar_strikethrough = FieldProperty(ITinyMCEToolbar['toolbar_strikethrough'])
    toolbar_sub = FieldProperty(ITinyMCEToolbar['toolbar_sub'])
    toolbar_sup = FieldProperty(ITinyMCEToolbar['toolbar_sup'])

    toolbar_forecolor = FieldProperty(ITinyMCEToolbar['toolbar_forecolor'])
    toolbar_backcolor = FieldProperty(ITinyMCEToolbar['toolbar_backcolor'])

    toolbar_justifyleft = FieldProperty(ITinyMCEToolbar['toolbar_justifyleft'])
    toolbar_justifycenter = FieldProperty(ITinyMCEToolbar['toolbar_justifycenter'])
    toolbar_justifyright = FieldProperty(ITinyMCEToolbar['toolbar_justifyright'])
    toolbar_justifyfull = FieldProperty(ITinyMCEToolbar['toolbar_justifyfull'])

    toolbar_bullist = FieldProperty(ITinyMCEToolbar['toolbar_bullist'])
    toolbar_numlist = FieldProperty(ITinyMCEToolbar['toolbar_numlist'])
    toolbar_outdent = FieldProperty(ITinyMCEToolbar['toolbar_outdent'])
    toolbar_indent = FieldProperty(ITinyMCEToolbar['toolbar_indent'])

    toolbar_tablecontrols = FieldProperty(ITinyMCEToolbar['toolbar_tablecontrols'])

    toolbar_link = FieldProperty(ITinyMCEToolbar['toolbar_link'])
    toolbar_unlink = FieldProperty(ITinyMCEToolbar['toolbar_unlink'])
    toolbar_anchor = FieldProperty(ITinyMCEToolbar['toolbar_anchor'])
    toolbar_image = FieldProperty(ITinyMCEToolbar['toolbar_image'])
    toolbar_media = FieldProperty(ITinyMCEToolbar['toolbar_media'])

    toolbar_charmap = FieldProperty(ITinyMCEToolbar['toolbar_charmap'])
    toolbar_hr = FieldProperty(ITinyMCEToolbar['toolbar_hr'])
    toolbar_advhr = FieldProperty(ITinyMCEToolbar['toolbar_advhr'])
    toolbar_insertdate = FieldProperty(ITinyMCEToolbar['toolbar_insertdate'])
    toolbar_inserttime = FieldProperty(ITinyMCEToolbar['toolbar_inserttime'])
    toolbar_emotions = FieldProperty(ITinyMCEToolbar['toolbar_emotions'])
    toolbar_nonbreaking = FieldProperty(ITinyMCEToolbar['toolbar_nonbreaking'])
    toolbar_pagebreak = FieldProperty(ITinyMCEToolbar['toolbar_pagebreak'])

    toolbar_print = FieldProperty(ITinyMCEToolbar['toolbar_print'])
    toolbar_preview = FieldProperty(ITinyMCEToolbar['toolbar_preview'])
    toolbar_iespell = FieldProperty(ITinyMCEToolbar['toolbar_iespell'])
    toolbar_removeformat = FieldProperty(ITinyMCEToolbar['toolbar_removeformat'])
    toolbar_cleanup = FieldProperty(ITinyMCEToolbar['toolbar_cleanup'])
    toolbar_visualaid = FieldProperty(ITinyMCEToolbar['toolbar_visualaid'])
    toolbar_visualchars = FieldProperty(ITinyMCEToolbar['toolbar_visualchars'])
    toolbar_code = FieldProperty(ITinyMCEToolbar['toolbar_code'])
    toolbar_fullscreen = FieldProperty(ITinyMCEToolbar['toolbar_fullscreen'])
    
    containsobjects = FieldProperty(ITinyMCEResourceTypes['containsobjects'])
    containsanchors = FieldProperty(ITinyMCEResourceTypes['containsanchors'])
    linkable = FieldProperty(ITinyMCEResourceTypes['linkable'])
    imageobjects = FieldProperty(ITinyMCEResourceTypes['imageobjects'])

    security.declareProtected('View', 'isTinyMCEEnabled')
    def isTinyMCEEnabled(self, useragent='', allowAnonymous=False, REQUEST=None, context=None, fieldName=None):
        if not REQUEST:
            REQUEST = self.REQUEST
        def numerics(s):
            """Convert a string into a tuple of all digit sequences"""
            seq = ['']
            for c in s:
                if c.isdigit():
                    seq[-1] = seq[-1] + c
                elif seq[-1]:
                    seq.append('')
            return tuple([ int(val) for val in seq if val])

        # First check whether the user actually wants kupu
        pm = getToolByName(self, 'portal_membership')
        if pm.isAnonymousUser() and not allowAnonymous:
            return False

        user = pm.getAuthenticatedMember()
        if not pm.isAnonymousUser():
            editor = user.getProperty('wysiwyg_editor')
            if editor and editor.lower() != 'tinymce':
                return False

        # Then check whether the current content allows html
        if context is not None and fieldName and hasattr(context, 'getWrappedField'):
            field = context.getWrappedField(fieldName)
            if field:
                allowedTypes = getattr(field, 'allowable_content_types', None)
                if allowedTypes is not None and not 'text/html' in [t.lower() for t in allowedTypes]:
                    return False

        # Then check whether their browser supports it.
        if not useragent:
            useragent = REQUEST['HTTP_USER_AGENT']

        if 'BEOS' in useragent:
            return False

        def getver(s):
            """Extract a version number given the string which precedes it"""
            pos = useragent.find(s)
            if pos >= 0:
                tail = useragent[pos+len(s):].strip()
                verno = numerics(tail.split(' ')[0])
                return verno
            return None

        try:
            v = getver('Opera/')
            if not v:
                v = getver('Opera ')
            if v:
                return v >= (9,0)

            mozillaver = getver('Mozilla/')
            if mozillaver > (5,0):
                return True
            elif mozillaver == (5,0):
                verno = getver(' rv:')
                if verno:
                    return verno >= (1,3,1)
                verno = getver(' AppleWebKit/')
                if verno:
                    return verno >= (525,1)
                    verno = getver(' Safari/')
                    if verno:
                        return verno >= (522,12)

            verno = getver('MSIE')
            if verno:
                return verno >= (5,5)
        except:
            # In case some weird browser makes the test code blow up.
            pass
        return False

    security.declarePrivate('getEnabledButtons')
    def getEnabledButtons(self):
        buttons = []

        # Get enabled buttons from control panel
        if self.toolbar_save:
            buttons.append('save')

        if self.toolbar_cut:
            buttons.append('cut')
        if self.toolbar_copy:
            buttons.append('copy')
        if self.toolbar_paste:
            buttons.append('paste')

        if self.toolbar_pastetext:
            buttons.append('pastetext')
        if self.toolbar_pasteword:
            buttons.append('pasteword')

        if self.toolbar_undo:
            buttons.append('undo')
        if self.toolbar_redo:
            buttons.append('redo')

        if self.toolbar_search:
            buttons.append('search')
        if self.toolbar_replace:
            buttons.append('replace')

        if self.toolbar_style:
            buttons.append('style')

        if self.toolbar_bold:
            buttons.append('bold')
        if self.toolbar_italic:
            buttons.append('italic')
        if self.toolbar_underline:
            buttons.append('underline')
        if self.toolbar_strikethrough:
            buttons.append('strikethrough')
        if self.toolbar_sub:
            buttons.append('sub')
        if self.toolbar_sup:
            buttons.append('sup')

        if self.toolbar_forecolor:
            buttons.append('forecolor')
        if self.toolbar_backcolor:
            buttons.append('backcolor')

        if self.toolbar_justifyleft:
            buttons.append('justifyleft')
        if self.toolbar_justifycenter:
            buttons.append('justifycenter')
        if self.toolbar_justifyright:
            buttons.append('justifyright')
        if self.toolbar_justifyfull:
            buttons.append('justifyfull')

        if self.toolbar_bullist:
            buttons.append('bullist')
        if self.toolbar_numlist:
            buttons.append('numlist')
        if self.toolbar_outdent:
            buttons.append('outdent')
        if self.toolbar_indent:
            buttons.append('indent')

        if self.toolbar_tablecontrols:
            buttons.append('tablecontrols')

        if self.toolbar_link:
            buttons.append('link')
        if self.toolbar_unlink:
            buttons.append('unlink')
        if self.toolbar_anchor:
            buttons.append('anchor')
        if self.toolbar_image:
            buttons.append('image')
        if self.toolbar_media:
            buttons.append('media')

        if self.toolbar_charmap:
            buttons.append('charmap')
        if self.toolbar_hr:
            buttons.append('hr')
        if self.toolbar_advhr:
            buttons.append('advhr')
        if self.toolbar_insertdate:
            buttons.append('insertdate')
        if self.toolbar_inserttime:
            buttons.append('inserttime')
        if self.toolbar_emotions:
            buttons.append('emotions')
        if self.toolbar_nonbreaking:
            buttons.append('nonbreaking')
        if self.toolbar_pagebreak:
            buttons.append('pagebreak')

        if self.toolbar_print:
            buttons.append('print')
        if self.toolbar_preview:
            buttons.append('preview')
        if self.toolbar_iespell:
            buttons.append('iespell')
        if self.toolbar_removeformat:
            buttons.append('removeformat')
        if self.toolbar_cleanup:
            buttons.append('cleanup')
        if self.toolbar_visualaid:
            buttons.append('visualaid')
        if self.toolbar_visualchars:
            buttons.append('visualchars')
        if self.toolbar_code:
            buttons.append('code')
        if self.toolbar_fullscreen:
            buttons.append('fullscreen')

        # Return the buttons
        return buttons

    security.declarePrivate ('translateButtonsFromKupu')
    def translateButtonsFromKupu(self, buttons):

        return_buttons = []
        
        for button in buttons:
            if button == 'save-button':
                return_buttons.append('save')
            elif button == 'bg-basicmarkup':
                pass
            elif button == 'bold-button':
                return_buttons.append('bold')
            elif button == 'italic-button':
                return_buttons.append('italic')
            elif button == 'bg-supsuper-button':
                pass
            elif button == 'subscript':
                return_buttons.append('sub')
            elif button == 'supscript':
                return_buttons.append('sup')
            elif button == 'bg-colorchooser':
                pass
            elif button == 'forecolor-button':
                return_buttons.append('forecolor')
            elif button == 'hilitecolor-button':
                return_buttons.append('backcolor')
            elif button == 'bg-justify':
                pass
            elif button == 'justifyleft-button':
                return_buttons.append('justifyleft')
            elif button == 'justifycenter-button':
                return_buttons.append('justifycenter')
            elif button == 'justifyright-button':
                return_buttons.append('justifyright')
            elif button == 'bg-list':
                pass
            elif button == 'list-ol-addbutton':
                return_buttons.append('numlist')
            elif button == 'list-ul-addbutton':
                return_buttons.append('bullist')
            elif button == 'definitionlist':
                pass
            elif button == 'bg-indent':
                pass
            elif button == 'outdent-button':
                return_buttons.append('outdent')
            elif button == 'indent-button':
                return_buttons.append('indent')
            elif button == 'bg-drawers':
                pass
            elif button == 'imagelibdrawer-button':
                return_buttons.append('image')
            elif button == 'linklibdrawer-button' or button == 'linkdrawer-button' or button == 'anchors-button':
                if 'link' not in return_buttons:
                    return_buttons.append('link')
            elif button == 'embed-tab':
                return_buttons.append('media')
            elif button == 'manage-anchors-tab':
                return_buttons.append('anchor')
            elif button == 'toc-tab':
                pass
            elif button == 'tabledrawer-button':
                return_buttons.append('tablecontrols')
            elif button == 'bg-remove':
                pass
            elif button == 'removeimage-button':
                pass
            elif button == 'removelink-button':
                return_buttons.append('unlink')
            elif button == 'bg-undo':
                pass
            elif button == 'undo-button':
                return_buttons.append('undo')
            elif button == 'redo-button':
                return_buttons.append('redo')
            elif button == 'spellchecker':
                return_buttons.append('iespell')
            elif button == 'source':
                return_buttons.append('code')
            elif button == 'styles' or button == 'ulstyles' or 'olstyles':
                if 'style' not in return_buttons:
                    return_buttons.append('style')
            elif button == 'zoom':
                return_buttons.append('fullscreen')
            else:
                if button not in return_buttons:
                    return_buttons.append(button)
        return return_buttons

    security.declareProtected('View', 'isTinyMCEEnabled')
    def getConfiguration(self, context=None, field=None):
        results = {}

        widget = getattr(field, 'widget', None)
        filter_buttons = getattr(widget, 'filter_buttons', None)
        allow_buttons = getattr(widget, 'allow_buttons', None)
        redefine_parastyles = getattr (widget, 'redefine_parastyles', None)
        parastyles = getattr (widget, 'parastyles', None)

        results['styles'] = []
        if redefine_parastyles is None or not redefine_parastyles:
            for tablestyle in self.tablestyles.split('\n'):
                tablestylefields = tablestyle.split('|');
                results['styles'].append(tablestylefields[0] + '|table|' + tablestylefields[0]);
            results['styles'].extend(self.styles.split('\n'))

        if parastyles is not None:
            results['styles'].extend(parastyles)

        # Get buttons from control panel
        results['buttons'] = self.getEnabledButtons()

        if allow_buttons is not None:
            allow_buttons = self.translateButtonsFromKupu(buttons=allow_buttons)
            results['buttons'] = filter(lambda x:x in results['buttons'],allow_buttons)
        if filter_buttons is not None:
            filter_buttons = self.translateButtonsFromKupu(buttons=filter_buttons)
            results['buttons'] = filter(lambda x:x not in filter_buttons, results['buttons'])

        return json.write(results)
