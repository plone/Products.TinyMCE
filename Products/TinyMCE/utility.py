try:
    import json
    json = json # Pyflakes
except ImportError:
    import simplejson as json
from types import StringTypes
from zope.component import getUtility, queryUtility
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.interface import classProvides
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from OFS.SimpleItem import SimpleItem
from Products.Archetypes.Field import ImageField
from Products.Archetypes.interfaces.field import IImageField
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
try:
    from plone.app.layout.globals.portal import RIGHT_TO_LEFT
    RIGHT_TO_LEFT = RIGHT_TO_LEFT # Pyflakes
except ImportError:
    # Plone 3
    RIGHT_TO_LEFT = ['ar', 'fa', 'he', 'ps']
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.outputfilters.filters.resolveuid_and_caption import IImageCaptioningEnabler
from plone.outputfilters.filters.resolveuid_and_caption import IResolveUidsEnabler

from Products.TinyMCE.bbb import implementedOrProvidedBy
from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.interfaces.utility import ITinyMCELayout
from Products.TinyMCE.interfaces.utility import ITinyMCEToolbar
from Products.TinyMCE.interfaces.utility import ITinyMCELibraries
from Products.TinyMCE.interfaces.utility import ITinyMCEResourceTypes

_ = MessageFactory('plone.tinymce')

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
    toolbar_spellchecker = FieldProperty(ITinyMCEToolbar['toolbar_spellchecker'])
    toolbar_removeformat = FieldProperty(ITinyMCEToolbar['toolbar_removeformat'])
    toolbar_cleanup = FieldProperty(ITinyMCEToolbar['toolbar_cleanup'])
    toolbar_visualaid = FieldProperty(ITinyMCEToolbar['toolbar_visualaid'])
    toolbar_visualchars = FieldProperty(ITinyMCEToolbar['toolbar_visualchars'])
    toolbar_attribs = FieldProperty(ITinyMCEToolbar['toolbar_attribs'])
    toolbar_code = FieldProperty(ITinyMCEToolbar['toolbar_code'])
    toolbar_fullscreen = FieldProperty(ITinyMCEToolbar['toolbar_fullscreen'])
    customtoolbarbuttons = FieldProperty(ITinyMCEToolbar['customtoolbarbuttons'])
    
    libraries_spellchecker_choice = FieldProperty(ITinyMCELibraries['libraries_spellchecker_choice'])
    libraries_atd_show_types = FieldProperty(ITinyMCELibraries['libraries_atd_show_types'])
    libraries_atd_ignore_strings = FieldProperty(ITinyMCELibraries['libraries_atd_ignore_strings'])

    link_using_uids = FieldProperty(ITinyMCEResourceTypes['link_using_uids'])
    allow_captioned_images = FieldProperty(ITinyMCEResourceTypes['allow_captioned_images'])
    rooted = FieldProperty(ITinyMCEResourceTypes['rooted'])
    containsobjects = FieldProperty(ITinyMCEResourceTypes['containsobjects'])
    containsanchors = FieldProperty(ITinyMCEResourceTypes['containsanchors'])
    linkable = FieldProperty(ITinyMCEResourceTypes['linkable'])
    imageobjects = FieldProperty(ITinyMCEResourceTypes['imageobjects'])
    customplugins = FieldProperty(ITinyMCEResourceTypes['customplugins'])

    def getImageScales(self, field=None, context=None):
        """Return the image sizes for the drawer"""
        if field is None:
            from Products.ATContentTypes.content.image import ATImage
            field = ATImage.schema['image']

        # in Archetypes 1.5.x ImageField doesn't actually provide IImageField o.O
        if not isinstance(field, ImageField) and not implementedOrProvidedBy(IImageField, field):
            raise TypeError("Can't retrieve image scale info for non-image field.")

        field_name = field.getName()
        sizes = field.getAvailableSizes(field)

        # Extract image dimensions from context.
        if context is not None:
            width, height = context.getField(field_name).getSize(context)
        else:
            width, height = 0, 0

        scales = [{'value': '%s_%s' % (field_name, key),
                   'size': [value[0], value[1]],
                   'title':key.capitalize() } for key, value in sizes.items()]
        scales.sort(lambda x,y: cmp(x['size'][0], y['size'][0]))
        scales.insert(0, {'value':'',
                          'title':'Original',
                          'size':[width, height]})
        return scales

    security.declarePrivate('getEnabledButtons')
    def getEnabledButtons(self, context):
        buttons = []

        # Get enabled buttons from control panel
        if self.toolbar_save:
            if getattr(aq_base(context), 'checkCreationFlag', None):
                if not context.checkCreationFlag():
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
        if self.toolbar_definitionlist:
            buttons.append('definitionlist')
        if self.toolbar_outdent:
            buttons.append('outdent')
        if self.toolbar_indent:
            buttons.append('indent')

        if self.toolbar_image:
            buttons.append('image')
        if self.toolbar_media:
            buttons.append('media')

        if self.toolbar_link:
            buttons.append('link')
        if self.toolbar_unlink:
            buttons.append('unlink')
        if self.toolbar_anchor:
            buttons.append('anchor')

        if self.toolbar_tablecontrols:
            buttons.append('tablecontrols')

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

        if self.toolbar_spellchecker:
            buttons.append(self.libraries_spellchecker_choice)

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
            'id style title class'.split())

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
            'map': I18N_ATTRS | set('id title name class'.split()),
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
            'iframe': COMMON_ATTRS | set('src name scrolling frameborder longdesc align height width marginheight marginwidth'.split())
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

        # Get kupu library tool filter
        # Settings are stored on safe_html transform in Plone 4 and
        # on kupu tool in Plone 3.
        kupu_library_tool = getToolByName(self, 'kupu_library_tool', None)

        stripped_combinations = []
        # Get stripped combinations try
        try:
            sc = safe_html.get_parameter_value('stripped_combinations')
            for ta in sc.keys():
                tags = ta.replace(',', ' ').split()
                attributes = sc[ta].replace(',', ' ').split()
                stripped_combinations.append((tags,attributes))
        except:
            if kupu_library_tool is not None:
                stripped_combinations = kupu_library_tool.get_stripped_combinations()

        # Strip combinations
        for (stripped_combination_tags, stripped_combination_attributes) in stripped_combinations:
            stripped_combination_attributes_set = set(stripped_combination_attributes)
            for stripped_combination_tag in stripped_combination_tags:
                if valid_elements.has_key(stripped_combination_tag):
                    valid_elements[stripped_combination_tag] -= stripped_combination_attributes_set

        # Remove to be stripped attributes
        try:
            stripped_attributes = set(safe_html.get_parameter_value('stripped_attributes'))
            style_whitelist = safe_html.get_parameter_value('style_whitelist')
        except:
            if kupu_library_tool is not None:
                stripped_attributes = set(kupu_library_tool.get_stripped_attributes())
                style_whitelist = kupu_library_tool.getStyleWhitelist()
            else:
                stripped_attributes = set()
                style_whitelist = ()
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
    def getConfiguration(self, context=None, field=None, request=None):
        results = {}

        # Get widget attributes
        widget = getattr(field, 'widget', None)
        filter_buttons = getattr(widget, 'filter_buttons', None)
        allow_buttons = getattr(widget, 'allow_buttons', None)
        redefine_parastyles = getattr (widget, 'redefine_parastyles', None)
        parastyles = getattr (widget, 'parastyles', None)
        rooted = getattr (widget, 'rooted', False)
        toolbar_width = getattr(widget, 'toolbar_width', self.toolbar_width)

        # Get safe html transform
        safe_html = getattr(getToolByName(self, 'portal_transforms'), 'safe_html')

        # Get kupu library tool filter
        # Settings are stored on safe_html transform in Plone 4 and
        # on kupu tool in Plone 3.
        kupu_library_tool = getToolByName(self, 'kupu_library_tool', None)

        # Remove to be stripped attributes
        try:
            style_whitelist = safe_html.get_parameter_value('style_whitelist')
        except:
            if kupu_library_tool is not None:
                style_whitelist = kupu_library_tool.getStyleWhitelist()
            else:
                style_whitelist = []
        results['valid_inline_styles'] = style_whitelist

        # Replacing some hardcoded translations
        labels = {}
        labels['label_styles'] = translate(_('(remove style)'), context=request)
        labels['label_paragraph'] = translate(_('Normal paragraph'), context=request)
        labels['label_plain_cell'] = translate(_('Plain cell'), context=request)
        labels['label_style_ldots'] = translate(_('Style...'), context=request)
        labels['label_text'] = translate(_('Text'), context=request)
        labels['label_tables'] = translate(_('Tables'), context=request)
        labels['label_selection'] = translate(_('Selection'), context=request)
        labels['label_lists'] = translate(_('Lists'), context=request)
        labels['label_print'] = translate(_('Print'), context=request)
        labels['label_no_items'] = translate(_('No items in this folder'), context=request)
        labels['label_no_anchors'] = translate(_('No anchors in this page'), context=request)
        results['labels']= labels

        # Add styles to results
        results['styles'] = []
        results['table_styles'] = []
        if not redefine_parastyles:
            if isinstance(self.tablestyles, StringTypes):
                for tablestyle in self.tablestyles.split('\n'):
                    if not tablestyle:
                        # empty line
                        continue
                    tablestylefields = tablestyle.split('|')
                    tablestyletitle = tablestylefields[0]
                    tablestyleid = tablestylefields[1]
                    if tablestyleid == 'plain':
                        # Do not duplicate the default style hardcoded in the
                        # table.htm.pt
                        continue
                    if request is not None:
                        tablestyletitle = translate(_(tablestylefields[0]), context=request)
                    results['styles'].append(tablestyletitle + '|table|' + tablestyleid)
                    results['table_styles'].append(tablestyletitle + '=' + tablestyleid)
            if isinstance(self.styles, StringTypes):
                styles = []
                for style in self.styles.split('\n'):
                    if not style:
                        # empty line
                        continue
                    stylefields = style.split('|')
                    styletitle = stylefields[0]
                    if request is not None:
                        styletitle = translate(_(stylefields[0]), context=request)
                    merge = styletitle + '|' + '|'.join(stylefields[1:])
                    styles.append(merge)
                results['styles'].extend(styles)

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
            results['toolbar_width'] = int(toolbar_width)
        except:
            results['toolbar_width'] = 440

        if self.directionality == 'auto':
            language = context.Language()
            if not language:
                portal_properties = getToolByName(context, "portal_properties")
                site_properties = portal_properties.site_properties
                language = site_properties.getProperty('default_language',
                                                       None)
            directionality = (language[:2] in RIGHT_TO_LEFT) and 'rtl' or 'ltr'
        else:
            directionality = self.directionality
        results['directionality'] = directionality

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

        portal = getUtility(ISiteRoot)
        results['portal_url'] =  aq_inner(portal).absolute_url()
        nav_root = getNavigationRootObject(context, portal)
        results['navigation_root_url'] = nav_root.absolute_url()

        props = getToolByName(self, 'portal_properties')
        livesearch = props.site_properties.getProperty('enable_livesearch', False)
        if livesearch:
            results['livesearch'] = True
        else:
            results['livesearch'] = False

        AVAILABLE_LANGUAGES = set(
        'sq ar hy az eu be bn nb bs br bg ca ch zh hr cs da dv nl en et fi fr gl '
        'ka de el gu he hi hu is id ia it ja ko lv lt lb mk ms ml mn se no nn fa '
        'pl pt ps ro ru sc sr ii si sk sl es sv ta tt te th tr tw uk ur cy vi zu'.split())

        if context.REQUEST.has_key('LANGUAGE'):
            results['language'] = context.REQUEST.LANGUAGE[:2]
            if results['language'] not in AVAILABLE_LANGUAGES:
                results['language'] = "en"
        else:
            results['language'] = "en"

        try:
            results['document_url'] = context.absolute_url()
            if getattr(aq_base(context), 'checkCreationFlag', None):
                parent = aq_parent(aq_inner(context))
                if context.checkCreationFlag():
                    parent = aq_parent(aq_parent(parent))
                    results['parent'] = parent.absolute_url() + "/"
                else:
                    if IFolderish.providedBy(context):
                        results['parent'] = context.absolute_url() + "/"
                    else:
                        results['parent'] = parent.absolute_url() + "/"
        except AttributeError:
            results['parent'] = results['portal_url'] + "/"
            results['document_url'] = results['portal_url']

        # Get Library options
        results['libraries_spellchecker_choice'] = \
                                        self.libraries_spellchecker_choice

        # init vars specific for "After the Deadline" spellchecker
        mtool = getToolByName(portal, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        results['atd_rpc_id'] = 'Products.TinyMCE-' + member.getId()
        results['atd_rpc_url'] = "%s/@@atdproxy" % portal.absolute_url()
        results['atd_show_types'] = self.libraries_atd_show_types.strip().replace('\n', ',')
        results['atd_ignore_strings'] = self.libraries_atd_ignore_strings.strip().replace('\n', ',')

        return json.dumps(results)


class ImageCaptioningEnabler(object):
    implements(IImageCaptioningEnabler)
    
    @property
    def available(self):
        tinymce = queryUtility(ITinyMCE)
        if tinymce is not None:
            return tinymce.allow_captioned_images
        return False


class ResolveUidsEnabler(object):
    implements(IResolveUidsEnabler)

    @property
    def available(self):
        tinymce = queryUtility(ITinyMCE)
        if tinymce is not None:
            return tinymce.link_using_uids
        return False
