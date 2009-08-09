from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility
from zope.interface import classProvides
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces._content import IContentish, IFolderish
from z3c.json import interfaces
from z3c.json import testing
from types import StringTypes

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
    autoresize_bottom_margin = FieldProperty(ITinyMCELayout['autoresize_bottom_margin'])
    editor_width = FieldProperty(ITinyMCELayout['editor_width'])
    editor_height = FieldProperty(ITinyMCELayout['editor_height'])
    directionality = FieldProperty(ITinyMCELayout['directionality'])
    contextmenu = FieldProperty(ITinyMCELayout['contextmenu'])
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
    toolbar_attribs = FieldProperty(ITinyMCEToolbar['toolbar_attribs'])
    toolbar_code = FieldProperty(ITinyMCEToolbar['toolbar_code'])
    toolbar_fullscreen = FieldProperty(ITinyMCEToolbar['toolbar_fullscreen'])
    customtoolbarbuttons = FieldProperty(ITinyMCEToolbar['customtoolbarbuttons'])

    link_using_uids = FieldProperty(ITinyMCEResourceTypes['link_using_uids'])
    allow_captioned_images = FieldProperty(ITinyMCEResourceTypes['allow_captioned_images'])
    rooted = FieldProperty(ITinyMCEResourceTypes['rooted'])
    containsobjects = FieldProperty(ITinyMCEResourceTypes['containsobjects'])
    containsanchors = FieldProperty(ITinyMCEResourceTypes['containsanchors'])
    linkable = FieldProperty(ITinyMCEResourceTypes['linkable'])
    imageobjects = FieldProperty(ITinyMCEResourceTypes['imageobjects'])
    customplugins = FieldProperty(ITinyMCEResourceTypes['customplugins'])

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

    def getImageScales(self, primary_field=None):
        """Return the image sizes for the drawer"""
        if primary_field is None:
            from Products.ATContentTypes.content.image import ATImage
            primary_field = ATImage.schema['image']
        sizes = primary_field.getAvailableSizes(primary_field)
        field_name = primary_field.getName()
        scales = [{'value':'', 'title':'Original', 'size':[0,0]}]
        for key, value in sizes.items():
            scales.append({'value': '%s_%s' % (field_name, key), 
                           'size': [value[0], value[1]],
                           'title':key.capitalize() })
        scales.sort(lambda x,y: cmp(x['size'][0], y['size'][0]))
        return scales

    security.declarePrivate('getEnabledButtons')
    def getEnabledButtons(self, context):
        buttons = []

        # Get enabled buttons from control panel
        if self.toolbar_save:
            try:
                if not context.checkCreationFlag():
                    buttons.append('save')
            except:
                pass

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
        if self.toolbar_attribs:
            buttons.append('attribs')
        if self.toolbar_code:
            buttons.append('code')
        if self.toolbar_fullscreen:
            buttons.append('fullscreen')

        if self.customtoolbarbuttons is not None:
            buttons.extend(self.customtoolbarbuttons.split('\n'))

        # Return the buttons
        return buttons

    security.declarePrivate ('translateButtonsFromKupu')
    def translateButtonsFromKupu(self, context, buttons):

        return_buttons = []
        
        for button in buttons:
            if button == 'save-button':
                try:
                    if not context.checkCreationFlag():
                        return_buttons.append('save')
                except:
                    pass
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
            elif button == 'styles' or button == 'ulstyles' or button == 'olstyles':
                if 'style' not in return_buttons:
                    return_buttons.append('style')
            elif button == 'zoom':
                return_buttons.append('fullscreen')
            else:
                if button not in return_buttons:
                    return_buttons.append(button)
        return return_buttons

    security.declarePrivate ('getValidElements')
    def getValidElements(self):

        XHTML_TAGS = set(
            'a abbr acronym address area b base bdo big blockquote body br '
            'button caption cite code col colgroup dd del div dfn dl dt em '
            'fieldset form h1 h2 h3 h4 h5 h6 head hr html i img input ins kbd '
            'label legend li link map meta noscript object ol optgroup option '
            'p param pre q samp script select small span strong style sub sup '
            'table tbody td textarea tfoot th thead title tr tt ul var'.split())

        CORE_ATTRS = set(
            'id title style class'.split())

        I18N_ATTRS = set(
            'lang dir'.split())

        FOCUS_ATTRS = set(
            'accesskey tabindex'.split())

        COMMON_ATTRS = CORE_ATTRS | I18N_ATTRS

        valid_elements = {
            'a': COMMON_ATTRS | FOCUS_ATTRS | set('charset type name href hreflang rel rev shape coords target'.split()),
            'abbr': COMMON_ATTRS.copy(),
            'acronym': COMMON_ATTRS.copy(),
            'address': COMMON_ATTRS.copy(),
            'applet': CORE_ATTRS | set('codebase archive code object alt name width height align hspace vspace'.split()),
            'area': COMMON_ATTRS | FOCUS_ATTRS | set('shape coords href nohref alt target'.split()),
            'b': COMMON_ATTRS.copy(),
            'base': set('id href target'.split()),
            'bdo': CORE_ATTRS | set('lang dir'.split()),
            'big': COMMON_ATTRS.copy(),
            'blockquote': COMMON_ATTRS | set('cite'.split()),
            'body': COMMON_ATTRS | set('background bgcolor text link vlink alink'.split()),
            'br': CORE_ATTRS | set('clear'.split()),
            'button': COMMON_ATTRS | FOCUS_ATTRS | set('name value type disabled'.split()),
            'caption': COMMON_ATTRS | set('align'.split()),
            'center': COMMON_ATTRS.copy(),
            'cite': COMMON_ATTRS.copy(),
            'code': COMMON_ATTRS.copy(),
            'col': COMMON_ATTRS | set('span width align char charoff valign'.split()),
            'colgroup': COMMON_ATTRS | set('span width align char charoff valign'.split()),
            'dd': COMMON_ATTRS.copy(),
            'del': COMMON_ATTRS | set('cite datetime'.split()),
            'dfn': COMMON_ATTRS.copy(),
            'div': COMMON_ATTRS | set('align'.split()),
            'dl': COMMON_ATTRS | set('compact'.split()),
            'dt': COMMON_ATTRS.copy(),
            'em': COMMON_ATTRS.copy(),
            'embed': '*',
            'fieldset': COMMON_ATTRS.copy(),
            'form': COMMON_ATTRS | set('action method name enctype accept accept-charset target'.split()),
            'h1': COMMON_ATTRS | set('align'.split()),
            'h2': COMMON_ATTRS | set('align'.split()),
            'h3': COMMON_ATTRS | set('align'.split()),
            'h4': COMMON_ATTRS | set('align'.split()),
            'h5': COMMON_ATTRS | set('align'.split()),
            'h6': COMMON_ATTRS | set('align'.split()),
            'head': I18N_ATTRS | set('id profile'.split()),
            'hr': COMMON_ATTRS | set('align noshade size width'.split()),
            'html': I18N_ATTRS | set('id xmlns'.split()),
            'i': COMMON_ATTRS.copy(),
            'img': COMMON_ATTRS | set('src alt name longdesc height width usemap ismap<ismap align border hspace vspace'.split()),
            'input': COMMON_ATTRS | FOCUS_ATTRS | set('type name value checked disabled readonly size maxlength src alt usemap accept align'.split()),
            'ins': COMMON_ATTRS | set('cite datetime'.split()),
            'kbd': COMMON_ATTRS.copy(),
            'label': COMMON_ATTRS | FOCUS_ATTRS | set('for'.split()),
            'legend': COMMON_ATTRS | set('accesskey align'.split()),
            'li': COMMON_ATTRS | set('type'.split()),
            'link': COMMON_ATTRS | set('charset href hreflang type rel rev media target'.split()),
            'map': I18N_ATTRS | set('id title name style class'.split()),
            'meta': I18N_ATTRS | set('id http-equiv name content scheme'.split()),
            'noscript': COMMON_ATTRS.copy(),
            'object': COMMON_ATTRS | set('declare classid codebase data type codetype archive standby height width usemap name tabindex align border hspace vspace'.split()),
            'ol': COMMON_ATTRS | set('compact type'.split()),
            'optgroup': COMMON_ATTRS | set('disabled label'.split()),
            'option': COMMON_ATTRS | set('selected disabled label value'.split()),
            'p': COMMON_ATTRS | set('align'.split()),
            'param': set('id name value valuetype type'.split()),
            'pre': COMMON_ATTRS | set('width'.split()),
            'q': COMMON_ATTRS | set('cite'.split()),
            'samp': COMMON_ATTRS.copy(),
            'script': set('id charset type language src defer'.split()),
            'select': COMMON_ATTRS | FOCUS_ATTRS | set('type name value checked disabled readonly size maxlength src alt usemap accept align multiple'.split()),
            'small': COMMON_ATTRS.copy(),
            'span': COMMON_ATTRS.copy(),
            'strong': COMMON_ATTRS.copy(),
            'style': I18N_ATTRS | set('id type media title'.split()),
            'sub': COMMON_ATTRS.copy(),
            'sup': COMMON_ATTRS.copy(),
            'table': COMMON_ATTRS | set('summary width border frame rules cellspacing cellpadding align bgcolor'.split()),
            'tbody': COMMON_ATTRS | set('align char charoff valign'.split()),
            'td': COMMON_ATTRS | set('align char charoff valign bgcolor abbr axis headers scope rowspan colspan nowrap width height'.split()),
            'textarea': COMMON_ATTRS | FOCUS_ATTRS | set('name rows cols disabled readonly'.split()),
            'tfoot': COMMON_ATTRS | set('align char charoff valign'.split()),
            'th': COMMON_ATTRS | set('align char charoff valign bgcolor abbr axis headers scope rowspan colspan nowrap width height'.split()),
            'thead': COMMON_ATTRS | set('align char charoff valign'.split()),
            'title': I18N_ATTRS | set('id'.split()),
            'tr': COMMON_ATTRS | set('align char charoff valign bgcolor'.split()),
            'tt': COMMON_ATTRS.copy(),
            'ul': COMMON_ATTRS | set('compact type'.split()),
            'var': COMMON_ATTRS.copy(),
            }

        # Get safe html transform
        safe_html = getattr(getToolByName(self, 'portal_transforms'), 'safe_html')

        # Get custom tags
        valid_tags = set(safe_html.get_parameter_value('valid_tags'))
        custom_tags = valid_tags - XHTML_TAGS

        # Add custom tags
        for custom_tag in custom_tags:
            if not valid_elements.has_key(custom_tag):
                valid_elements[custom_tag] = COMMON_ATTRS

        # Get kupu library tool
        kupu_library_tool = getToolByName(self, 'kupu_library_tool')

        # Get stripped combinations
        stripped_combinations = kupu_library_tool.get_stripped_combinations()

        # Strip combinations
        for (stripped_combination_tags, stripped_combination_attributes) in stripped_combinations:
            stripped_combination_attributes_set = set(stripped_combination_attributes)
            for stripped_combination_tag in stripped_combination_tags:
                if valid_elements.has_key(stripped_combination_tag):
                    valid_elements[stripped_combination_tag] -= stripped_combination_attributes_set

        # Remove to be stripped attributes
        stripped_attributes = set(kupu_library_tool.get_stripped_attributes())
        style_whitelist = kupu_library_tool.getStyleWhitelist()
        style_attribute = "style"
        if len(style_whitelist) > 0:
            style_attribute = 'style<' + '?'.join(style_whitelist)

        # Remove elements which are not in valid_tags
        for valid_element in valid_elements.keys():
            if valid_element not in valid_tags:
                del valid_elements[valid_element]
            else:
                if valid_elements[valid_element] != '*':
                    valid_elements[valid_element] -= stripped_attributes
                #if 'style' in valid_elements[valid_element]:
                #    valid_elements[valid_element].remove('style')
                #    valid_elements[valid_element].add(style_attribute)

        # Convert sets to lists
        for valid_element in valid_elements.keys():
            valid_elements[valid_element] = sorted(valid_elements[valid_element])

        return valid_elements

    security.declareProtected('View', 'getContentType')
    def getContentType(self, object=None, fieldname=None):
        if hasattr(object, 'getContentType'):
            return object.getContentType(fieldname)
        return 'text/html'

    security.declareProtected('View', 'getConfiguration')
    def getConfiguration(self, context=None, field=None):
        results = {}

        # Get widget attributes
        widget = getattr(field, 'widget', None)
        filter_buttons = getattr(widget, 'filter_buttons', None)
        allow_buttons = getattr(widget, 'allow_buttons', None)
        redefine_parastyles = getattr (widget, 'redefine_parastyles', None)
        parastyles = getattr (widget, 'parastyles', None)
        rooted = getattr (widget, 'rooted', False)

        # Add styles to results
        results['styles'] = []
        results['table_styles'] = []
        if not redefine_parastyles:
            if isinstance(self.tablestyles, StringTypes):
                for tablestyle in self.tablestyles.split('\n'):
                    tablestylefields = tablestyle.split('|');
                    results['styles'].append(tablestylefields[0] + '|table|' + tablestylefields[1]);
                    results['table_styles'].append(tablestylefields[0] + '=' + tablestylefields[1]);
            if isinstance(self.styles, StringTypes):
                results['styles'].extend(self.styles.split('\n'))

        if parastyles is not None:
            results['styles'].extend(parastyles)

        # Get buttons from control panel
        results['buttons'] = self.getEnabledButtons(context=context)

        # Filter buttons
        if allow_buttons is not None:
            allow_buttons = self.translateButtonsFromKupu(context=context, buttons=allow_buttons)
            results['buttons'] = filter(lambda x:x in results['buttons'],allow_buttons)
        if filter_buttons is not None:
            filter_buttons = self.translateButtonsFromKupu(context=context, buttons=filter_buttons)
            results['buttons'] = filter(lambda x:x not in filter_buttons, results['buttons'])

        # Get valid html elements
        results['valid_elements'] = self.getValidElements()

        # Set toolbar_location
        if self.toolbar_external:
            results['toolbar_location'] = 'external'
        else:
            results['toolbar_location'] = 'top'

        if self.autoresize:
            results['path_location'] = 'none'
            results['resizing_use_cookie'] = False
            results['resizing'] = False
            results['autoresize'] = True
        else:
            results['path_location'] = 'bottom'
            results['resizing_use_cookie'] = True
            if self.resizing:
                results['resizing'] = True
            else:
                results['resizing'] = False
            results['autoresize'] = False

        try:
            results['autoresize_bottom_margin'] = int(self.autoresize_bottom_margin)
        except:
            results['autoresize_bottom_margin'] = 40

        if '%' in self.editor_width:
            results['resize_horizontal'] = False
        else:
            results['resize_horizontal'] = True

        try:
            results['editor_width'] = int(self.editor_width)
        except:
            results['editor_width'] = 600

        try:
            results['editor_height'] = int(self.editor_height)
        except:
            results['editor_height'] = 400

        try:
            results['toolbar_width'] = int(self.toolbar_width)
        except:
            results['toolbar_width'] = 440

        results['directionality'] = self.directionality
        if self.contextmenu:
            results['contextmenu'] = True
        else:
            results['contextmenu'] = False

        if self.content_css and self.content_css.strip() != "":
            results['content_css'] = self.content_css
        else:
            results['content_css'] = self.absolute_url() + """/@@tinymce-getstyle"""

        if self.link_using_uids:
            results['link_using_uids'] = True
        else:
            results['link_using_uids'] = False

        if self.allow_captioned_images:
            results['allow_captioned_images'] = True
        else:
            results['allow_captioned_images'] = False

        if self.rooted or rooted:
            results['rooted'] = True
        else:
            results['rooted'] = False

        results['customplugins'] = []
        if self.customplugins is not None:
            results['customplugins'].extend(self.customplugins.split('\n'))

        results['entity_encoding'] = self.entity_encoding

        portal_url = getToolByName(self, 'portal_url')
        results['portal_url'] = portal_url()

        props = getToolByName(self, 'portal_properties')
        livesearch = props.site_properties.getProperty('enable_livesearch', False)
        if livesearch:
            results['livesearch'] = True
        else:
            results['livesearch'] = False

        AVAILABLE_LANGUAGES = set(
           'ar bs ch da el es fa fr he hu ii it ko lv ms nl pl ro sc si sl sr '
           'tr tw vi bg ca cs de en et fi gl hr ia is ja lt mk nb nn pt ru se '
           'sk sq sv tt uk zh'.split())

        if context.REQUEST.has_key('LANGUAGE'):
            results['language'] = context.REQUEST.LANGUAGE[:2]
            if results['language'] not in AVAILABLE_LANGUAGES:
                results['language'] = "en"
        else:
            results['language'] = "en"

        try:
            results['document_url'] = context.absolute_url()
            if context.checkCreationFlag():
                parent = getattr(context.aq_inner, 'aq_parent', None)
                parent = getattr(parent, 'aq_parent', None)
                parent = getattr(parent, 'aq_parent', None)
                results['parent'] = parent.absolute_url() + "/"
            else:
                if IFolderish.providedBy(context):
                    results['parent'] = context.absolute_url() + "/"
                else:
                    results['parent'] = getattr(context.aq_inner, 'aq_parent', None).absolute_url() + "/"
        except:
            results['parent'] = portal_url() + "/"
            results['document_url'] = portal_url()

        testing.setUpJSONConverter()
        jsonWriter = getUtility(interfaces.IJSONWriter)
        return jsonWriter.write(results)
