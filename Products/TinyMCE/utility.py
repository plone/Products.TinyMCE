try:
    import simplejson as json
    json  # Pyflakes
except ImportError:
    import json
from types import StringTypes
from zope.component import getUtilitiesFor, queryUtility
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.interface import classProvides, implements
from zope.schema.fieldproperty import FieldProperty
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base, aq_inner, aq_parent
from OFS.SimpleItem import SimpleItem
from Products.Archetypes.Field import ImageField
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.interfaces.field import IImageField
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFCore.utils import getToolByName
try:
    from plone.app.layout.globals.portal import RIGHT_TO_LEFT
    RIGHT_TO_LEFT    # pyflakes
except ImportError:
    RIGHT_TO_LEFT = ['ar', 'fa', 'he', 'ps']  # not available in plone 3
from plone.outputfilters.filters.resolveuid_and_caption import IImageCaptioningEnabler, IResolveUidsEnabler

from Products.TinyMCE.bbb import implementedOrProvidedBy
from Products.TinyMCE.interfaces.shortcut import ITinyMCEShortcut
from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.interfaces.utility import ITinyMCELayout
from Products.TinyMCE.interfaces.utility import ITinyMCEToolbar
from Products.TinyMCE.interfaces.utility import ITinyMCELibraries
from Products.TinyMCE.interfaces.utility import ITinyMCEResourceTypes
from Products.TinyMCE.interfaces.utility import ITinyMCEContentBrowser


_ = MessageFactory('plone.tinymce')
PMF = MessageFactory('plone')
BUTTON_WIDTHS = {'style': 150, 'forecolor': 32, 'backcolor': 32, 'tablecontrols': 285}


try:
    from plone.app.textfield.interfaces import IRichText
    IRichText    # pyflakes
except ImportError:
    from zope.interface import Interface
    class IRichText(Interface):
        pass


def form_adapter(context):
    """Form Adapter"""
    return getToolByName(context, 'portal_tinymce')


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
    contextmenu = FieldProperty(ITinyMCELayout['contextmenu'])
    content_css = FieldProperty(ITinyMCELayout['content_css'])
    styles = FieldProperty(ITinyMCELayout['styles'])
    formats = FieldProperty(ITinyMCELayout['formats'])
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
    libraries_atd_service_url = FieldProperty(ITinyMCELibraries['libraries_atd_service_url'])

    link_using_uids = FieldProperty(ITinyMCEResourceTypes['link_using_uids'])
    allow_captioned_images = FieldProperty(ITinyMCEResourceTypes['allow_captioned_images'])
    rooted = FieldProperty(ITinyMCEResourceTypes['rooted'])
    containsobjects = FieldProperty(ITinyMCEResourceTypes['containsobjects'])
    containsanchors = FieldProperty(ITinyMCEResourceTypes['containsanchors'])
    linkable = FieldProperty(ITinyMCEResourceTypes['linkable'])
    imageobjects = FieldProperty(ITinyMCEResourceTypes['imageobjects'])
    plugins = FieldProperty(ITinyMCEResourceTypes['plugins'])
    customplugins = FieldProperty(ITinyMCEResourceTypes['customplugins'])

    link_shortcuts = FieldProperty(ITinyMCEContentBrowser['link_shortcuts'])
    image_shortcuts = FieldProperty(ITinyMCEContentBrowser['image_shortcuts'])
    num_of_thumb_columns = FieldProperty(ITinyMCEContentBrowser['num_of_thumb_columns'])
    thumbnail_size = FieldProperty(ITinyMCEContentBrowser['thumbnail_size'])

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

        scales = [{'value': '@@images/%s/%s' % (field_name, key),
                   'size': [value[0], value[1]],
                   'title': key.capitalize()} for key, value in sizes.items()]
        scales.sort(key=lambda x: x['size'][0])
        scales.insert(0, {'value': '',
                          'title': _(u'Original'),
                          'size': [width, height]})
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

    security.declarePrivate('translateButtonsFromKupu')
    def translateButtonsFromKupu(self, context, buttons):
        """Given a set of buttons in Kupu, translate them to
        a set for TinyMCE toolbar
        """
        return_buttons = []

        for button in buttons:
            if button == 'save-button':
                try:
                    if not context.checkCreationFlag():
                        return_buttons.append('save')
                except AttributeError:
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

    security.declarePrivate('getValidElements')
    def getValidElements(self):
        """Return valid (X)HTML elements and their attributes
        that can be used within TinyMCE
        """
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
            if custom_tag not in valid_elements:
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
                stripped_combinations.append((tags, attributes))
        except(KeyError, AttributeError):
            if kupu_library_tool is not None:
                stripped_combinations = kupu_library_tool.get_stripped_combinations()

        # Strip combinations
        for (stripped_combination_tags, stripped_combination_attributes) in stripped_combinations:
            stripped_combination_attributes_set = set(stripped_combination_attributes)
            for stripped_combination_tag in stripped_combination_tags:
                if stripped_combination_tag in valid_elements:
                    valid_elements[stripped_combination_tag] -= stripped_combination_attributes_set

        # Remove to be stripped attributes
        try:
            stripped_attributes = set(safe_html.get_parameter_value('stripped_attributes'))
            #style_whitelist = safe_html.get_parameter_value('style_whitelist')
        except (KeyError, AttributeError):
            if kupu_library_tool is not None:
                stripped_attributes = set(kupu_library_tool.get_stripped_attributes())
                #style_whitelist = kupu_library_tool.getStyleWhitelist()
            else:
                stripped_attributes = set()
                #style_whitelist = ()

        #style_attribute = "style"
        #if len(style_whitelist) > 0:
            #style_attribute = 'style<' + '?'.join(style_whitelist)

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

        # p needs to be prepended with # to allow empty p tags http://www.tinymce.com/wiki.php/Configuration:valid_elements
        valid_elements['#p'] = valid_elements.pop('p')
        return valid_elements

    security.declarePrivate('getPlugins')
    def getPlugins(self):
        """ See ITinyMCE interface
        """
        plugins = self.plugins[:]
        sp = self.libraries_spellchecker_choice
        if sp and sp != "browser":
            plugins.append(sp)

        if self.customplugins is not None:
            for plugin in self.customplugins.splitlines():
                if '|' in plugin:
                    plugin = plugin.split('|', 1)[0]
                if plugin not in plugins:
                    plugins.append(plugin)

        if self.contextmenu:
            plugins.append('contextmenu')

        if self.autoresize:
            plugins.append('autoresize')
        return ','.join(plugins)

    security.declarePrivate('getStyles')
    def getStyles(self, styles, labels):
        """ See ITinyMCE interface
        """
        h = {'Text': [], 'Selection': [], 'Tables': [], 'Lists': [], 'Print': []}
        styletype = ""

        # Push title
        h['Text'].append('{ title: "Text", tag: "", className: "-", type: "Text" }')
        h['Selection'].append('{ title: "Selection", tag: "", className: "-", type: "Selection" }')
        h['Tables'].append('{ title: "Tables", tag: "table", className: "-", type: "Tables" }')
        h['Lists'].append('{ title: "Lists", tag: "ul", className: "-", type: "Lists" }')
        h['Lists'].append('{ title: "Lists", tag: "ol", className: "-", type: "Lists" }')
        h['Lists'].append('{ title: "Lists", tag: "dl", className: "-", type: "Lists" }')
        h['Print'].append('{ title: "Print", tag: "", className: "-", type: "Print" }')

        # Add defaults
        h['Text'].append('{ title: "' + labels['label_paragraph'] + '", tag: "p", className: " ", type: "Text" }')
        h['Selection'].append('{ title: "' + labels['label_styles'] + '", tag: "", className: "", type: "Selection" }')
        h['Tables'].append('{ title: "' + labels['label_plain_cell'] + '", tag: "td", className: " ", type: "Tables" }')
        h['Lists'].append('{ title: "' + labels['label_lists'] + '", tag: "dl", className: " ", type: "Lists" }')

        for i in styles:
            e = i.split('|')
            while len(e) <= 2:
                e.append("")
            if e[1].lower() in ('del', 'ins', 'span'):
                    styletype = "Selection"
            elif e[1].lower() in ('table', 'tr', 'td', 'th'):
                    styletype = "Tables"
            elif e[1].lower() in ('ul', 'ol', 'li', 'dt', 'dd', 'dl'):
                    styletype = "Lists"
            else:
                    styletype = "Text"

            if e[2] == "pageBreak":
                    styletype = "Print"
            h[styletype].append('{ title: "' + e[0] + '", tag: "' + e[1] + '", className: "' + e[2] + '", type: "' + styletype + '" }')

            # Add items to list
            a = []
            if len(h['Text']) > 1:
                a.extend(h['Text'])
            if len(h['Selection']) > 1:
                a.extend(h['Selection'])
            if len(h['Tables']) > 1:
                a.extend(h['Tables'])
            if len(h['Lists']) > 1:
                a.extend(h['Lists'])
            if len(h['Print']) > 1:
                a.extend(h['Print'])

        return '[' + ','.join(a) + ']'

    security.declarePrivate('getToolbars')
    def getToolbars(self, config):
        """Calculate number of toolbar rows from length of buttons"""
        t = [[], [], [], []]
        cur_toolbar = 0
        cur_x = 0

        for i in config['buttons']:
            button_width = BUTTON_WIDTHS.get(i, 23)
            if cur_x + button_width > int(config['toolbar_width']):
                cur_x = button_width
                cur_toolbar += 1
            else:
                cur_x += button_width
            if cur_toolbar <= 3:
                t[cur_toolbar].append(i)

        return [','.join(toolbar) for toolbar in t]

    security.declareProtected('View', 'getContentType')
    def getContentType(self, object=None, field=None, fieldname=None):
        context = aq_base(object)
        if context is not None and IBaseObject.providedBy(context):
            # support Archetypes fields
            if field is not None:
                pass
            elif fieldname is not None:
                field = context.getField(fieldname) or getattr(context, fieldname, None)
            else:
                field = context.getPrimaryField()
            if field and hasattr(aq_base(field), 'getContentType'):
                return field.getContentType(context)
        elif IRichText.providedBy(field):
            # support plone.app.textfield RichTextValues

            # First try to get a stored value and check its mimetype.
            mimetype = None
            if context is not None:
                value = getattr(context, fieldname, None)
                mimetype = getattr(value, 'mimeType', None)

            # Fall back to the field's default mimetype
            if mimetype is None:
                mimetype = field.default_mime_type
            return mimetype
        elif context is not None and fieldname is not None and '.widgets.' in fieldname:
            # We don't have the field object but we can at least try
            # to get the mimetype from an attribute on the object
            fieldname = fieldname.split('.widgets.')[-1]
            field = getattr(context, fieldname, None)
            mimetype = getattr(field, 'mimeType', None)
            if mimetype is not None:
                return mimetype
        return 'text/html'

    security.declareProtected('View', 'getConfiguration')
    def getConfiguration(self, context=None, field=None, request=None, script_url=None):
        """Return JSON configuration that is passed to javascript tinymce constructor.

        :param field: Dexterity or Archetypes Field instance

        :param context: The TinyMCE editor content items

        :param script_url: tinymce.jquery.js plug-in TinyMCE script parameter.
                           For more details see
                           http://www.tinymce.com/wiki.php/jQuery_Plugin

        :return: JSON string of the TinyMCE configuration for this field
        """
        results = {}

        # Get widget attributes
        widget = getattr(field, 'widget', None)
        filter_buttons = getattr(widget, 'filter_buttons', None)
        allow_buttons = getattr(widget, 'allow_buttons', None)
        redefine_parastyles = getattr(widget, 'redefine_parastyles', None)
        parastyles = getattr(widget, 'parastyles', None)
        rooted = getattr(widget, 'rooted', False)
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
        except (KeyError, AttributeError):
            if kupu_library_tool is not None:
                style_whitelist = kupu_library_tool.getStyleWhitelist()
            else:
                style_whitelist = []
        results['valid_inline_styles'] = ','.join(style_whitelist)  # tinymce format

        # Replacing some hardcoded translations
        labels = {}
        labels['label_browseimage'] = translate(_('Image Browser'), context=request)
        labels['label_browselink'] = translate(_('Link Browser'), context=request)
        labels['label_addnewimage'] = translate(_('Add new Image'), context=request)
        labels['label_addnewfile'] = translate(_('Add new File'), context=request)
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
        labels['label_browser'] = translate(_('Browser'), context=request)
        labels['label_shortcuts'] = translate(_('Shortcuts'), context=request)
        labels['label_search_results'] = translate(_('Search results:'), context=request)
        labels['label_internal_path'] = translate(PMF("you_are_here"), context=request)
        results['labels'] = labels

        # Add styles to results
        results['styles'] = []
        table_styles = []
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
                    table_styles.append(tablestyletitle + '=' + tablestyleid)
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
        results['table_styles'] = ';'.join(table_styles)  # tinymce config

        if parastyles is not None:
            results['styles'].extend(parastyles)

        styles = results.pop('styles')

        # Get buttons from control panel
        results['buttons'] = self.getEnabledButtons(context=context)

        # Filter buttons
        if allow_buttons is not None:
            allow_buttons = self.translateButtonsFromKupu(context=context, buttons=allow_buttons)
            results['buttons'] = filter(lambda x: x in results['buttons'], allow_buttons)
        if filter_buttons is not None:
            filter_buttons = self.translateButtonsFromKupu(context=context, buttons=filter_buttons)
            results['buttons'] = filter(lambda x: x not in filter_buttons, results['buttons'])

        # Get valid html elements
        valid_elements = self.getValidElements()
        results['valid_elements'] = ','.join(["%s[%s]" % (key, '|'.join(value)) for key, value in valid_elements.iteritems()])

        # self.customplugins can be None on old migrated sites
        results['customplugins'] = (self.customplugins or "").splitlines()

        # Set toolbar_location
        if self.toolbar_external:
            results['theme_advanced_toolbar_location'] = 'external'
        else:
            results['theme_advanced_toolbar_location'] = 'top'

        if self.autoresize:
            results['theme_advanced_path_location'] = 'none'
            results['theme_advanced_resizing_use_cookie'] = False
            results['theme_advanced_resizing'] = False
            results['autoresize'] = True
        else:
            results['theme_advanced_path_location'] = 'bottom'
            results['theme_advanced_resizing_use_cookie'] = True
            results['theme_advanced_resizing'] = self.resizing
            results['autoresize'] = False

        if '%' in self.editor_width:
            results['theme_advanced_resize_horizontal'] = False
        else:
            results['theme_advanced_resize_horizontal'] = True

        try:
            results['theme_advanced_source_editor_width'] = int(self.editor_width)
        except (TypeError, ValueError):
            results['theme_advanced_source_editor_width'] = 600

        try:
            results['theme_advanced_source_editor_height'] = int(self.editor_height)
        except (TypeError, ValueError):
            results['theme_advanced_source_editor_height'] = 400

        try:
            results['toolbar_width'] = int(toolbar_width)
        except (TypeError, ValueError):
            results['toolbar_width'] = 440

        portal_state = context.restrictedTraverse('@@plone_portal_state')
        # is_rtl handles every possible setting as far as RTL/LTR is concerned
        # pass that to tinmyce
        results['directionality'] = portal_state.is_rtl() and 'rtl' or 'ltr'

        portal = portal_state.portal()
        request = context.REQUEST
        portal_path = portal.getPhysicalPath()
        results['portal_url'] = request.physicalPathToURL(portal_path)
        results['navigation_root_url'] = portal_state.navigation_root_url()

        if self.content_css and self.content_css.strip() != "":
            results['content_css'] = self.content_css
        else:
            results['content_css'] = '/'.join([
                results['portal_url'],
                self.getId(),
                "@@tinymce-getstyle"])

        results['link_using_uids'] = self.link_using_uids
        results['contextmenu'] = self.contextmenu
        results['entity_encoding'] = self.entity_encoding
        if script_url:
            results['script_url'] = script_url

        if self.allow_captioned_images:
            results['allow_captioned_images'] = True
        else:
            results['allow_captioned_images'] = False

        if self.rooted or rooted:
            results['rooted'] = True
        else:
            results['rooted'] = False

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

        if 'LANGUAGE' in context.REQUEST:
            results['language'] = context.REQUEST.LANGUAGE[:2]
            if results['language'] not in AVAILABLE_LANGUAGES:
                results['language'] = "en"
        else:
            results['language'] = "en"

        try:
            results['document_url'] = context.absolute_url()
            parent = aq_parent(aq_inner(context))
            if getattr(aq_base(context), 'checkCreationFlag', lambda: None)():
                # An archetypes add form, navigate outside the portal_factory
                parent = aq_parent(aq_parent(parent))
                results['document_base_url'] = parent.absolute_url() + "/"
            else:
                if IFolderish.providedBy(context):
                    # Current item is folderish (or parent, if a dexterity add form)
                    results['document_base_url'] = context.absolute_url() + "/"
                else:
                    # Parent must be folderish, since it contains context
                    results['document_base_url'] = parent.absolute_url() + "/"
        except AttributeError:
            results['document_base_url'] = results['portal_url'] + "/"
            results['document_url'] = results['portal_url']

        # Get Library options
        results['gecko_spellcheck'] = self.libraries_spellchecker_choice == 'browser'

        # Content Browser
        shortcuts_dict = dict(getUtilitiesFor(ITinyMCEShortcut))
        results['link_shortcuts_html'] = []
        results['image_shortcuts_html'] = []
        results['num_of_thumb_columns'] = self.num_of_thumb_columns
        results['thumbnail_size'] = self.thumbnail_size

        for name in self.link_shortcuts:
            results['link_shortcuts_html'].extend(shortcuts_dict.get(name).render(context))
        for name in self.image_shortcuts:
            results['image_shortcuts_html'].extend(shortcuts_dict.get(name).render(context))

        # init vars specific for "After the Deadline" spellchecker
        mtool = getToolByName(portal, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        results['atd_rpc_id'] = 'Products.TinyMCE-' + (member.getId() or '')  # None when Anonymous User
        results['atd_rpc_url'] = "%s/@@" % portal.absolute_url()
        results['atd_show_types'] = self.libraries_atd_show_types.strip().replace('\n', ',')
        results['atd_ignore_strings'] = self.libraries_atd_ignore_strings.strip().replace('\n', ',')

        # generic configuration
        results['mode'] = "exact"
        results['theme'] = "advanced"
        results['skin'] = "plone"
        results['inlinepopups_skin'] = "plonepopup"
        results['body_class'] = "documentContent"
        results['body_id'] = "content"
        results['table_firstline_th'] = True
        results['fix_list_elements'] = False
        # allow embed tag if user removes it from
        # list of nasty tags - see #10681
        results['media_strict'] = False
        results['theme_advanced_path'] = False
        results['theme_advanced_toolbar_align'] = "left"

        results['plugins'] = self.getPlugins()
        results['theme_advanced_styles'] = self.getStyles(styles, labels)
        results['theme_advanced_buttons1'], results['theme_advanced_buttons2'], \
            results['theme_advanced_buttons3'], results['theme_advanced_buttons4'] = self.getToolbars(results)

        if self.formats and self.formats.strip():
            results['formats'] = json.loads(self.formats)

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
