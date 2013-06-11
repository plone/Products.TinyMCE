# -*- coding: utf-8 -*-

try:
    import simplejson as json
    json  # Pyflakes
except ImportError:
    import json

from zope import schema
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from Products.TinyMCE.vocabularies import (
        shortcuts_vocabulary, thumbnail_sizes_vocabulary, plugins_vocabulary)

_ = MessageFactory('plone.tinymce')

DEFAULT_PLUGINS = ['advhr', 'definitionlist', 'directionality', 'emotions',
 'fullscreen', 'inlinepopups', 'insertdatetime', 'media', 'nonbreaking',
 'noneditable', 'pagebreak', 'paste', 'plonebrowser',
 'ploneinlinestyles', 'plonestyle', 'preview', 'print', 'save',
 'searchreplace', 'tabfocus', 'table', 'visualchars', 'xhtmlxtras']


def validate_json(value):
    try:
        json.loads(value)
    except ValueError, exc:
        class JSONError(schema.ValidationError):
            __doc__ = _(u"Must be empty or a valid JSON-formatted "
                        u"configuration – ${message}.", mapping={
                            'message': unicode(exc)})

        raise JSONError(value)

    return True


class ITinyMCELayout(Interface):
    """This interface defines the layout properties."""

    resizing = schema.Bool(
        title=_(u"Enable resizing the editor window."),
        description=_(u"This option gives you the ability to enable/disable resizing the editor window. If the editor width is set to a percentage only vertical resizing is enabled."),
        required=False)

    autoresize = schema.Bool(
        title=_(u"Enable auto resizing of the editor window."),
        description=_(u"This option gives you the ability to enable/disable auto resizing the editor window depending on the content."),
        required=False)

    # TODO: add validation to assert % and px in the value
    editor_width = schema.TextLine(
        title=_(u"Editor width"),
        description=_(u"This option gives you the ability to specify the width of the editor (like 100% or 400px)."),
        required=False)

    # TODO: add validation to assert % and px in the value
    editor_height = schema.TextLine(
        title=_(u"Editor height"),
        description=_(u"This option gives you the ability to specify the height of the editor in pixels. If auto resize is enabled this value is used as minimum height."),
        required=False)

    contextmenu = schema.Bool(
        title=_(u"Enable contextmenu"),
        description=_(u"This option gives you the ability to enable/disable the use of the contextmenu."),
        required=False)

    content_css = schema.TextLine(
        title=_(u"Choose the CSS used in WYSIWYG Editor Area"),
        description=_(u"This option enables you to specify a custom CSS file that replaces the theme content CSS. This CSS file is the one used within the editor (the editable area)."),
        required=False)

    styles = schema.Text(
        title=_(u"Styles"),
        description=_(u"Enter a list of styles to appear in the style pulldown. Format is title|tag or title|tag|className, one per line."),
        required=False)

    formats = schema.Text(
        title=_(u"Formats"),
        description=_(u"Enter a JSON-formatted style format configuration. "
                      u"A format is for example the style that get applied when "
                      u"you press the bold button inside the editor. "
                      u"See http://www.tinymce.com/wiki.php/Configuration:formats"),
        constraint=validate_json,
        required=False,
    )

    tablestyles = schema.Text(
        title=_(u"Table styles"),
        description=_(u"Enter a list of styles to appear in the table style pulldown. Format is title|class, one per line."),
        required=False)


class ITinyMCEToolbar(Interface):
    """This interface defines the toolbar properties."""

    toolbar_width = schema.TextLine(
        title=_(u"Toolbar width"),
        description=_(u"This option gives you the ability to specify the width of the toolbar in pixels."),
        required=False)

    toolbar_external = schema.Bool(
        title=_(u"Place toolbar on top of the page"),
        description=_(u"This option enables the external toolbar which will be placed at the top of the page."),
        required=False)

    toolbar_save = schema.Bool(
        title=_(u"Save"),
        required=False)

    toolbar_cut = schema.Bool(
        title=_(u"Cut"),
        required=False)

    toolbar_copy = schema.Bool(
        title=_(u"Copy"),
        required=False)

    toolbar_paste = schema.Bool(
        title=_(u"Paste"),
        required=False)

    toolbar_pastetext = schema.Bool(
        title=_(u"Paste as Plain Text"),
        required=False)

    toolbar_pasteword = schema.Bool(
        title=_(u"Paste from Word"),
        required=False)

    toolbar_undo = schema.Bool(
        title=_(u"Undo"),
        required=False)

    toolbar_redo = schema.Bool(
        title=_(u"Redo"),
        required=False)

    toolbar_search = schema.Bool(
        title=_(u"Find"),
        required=False)

    toolbar_replace = schema.Bool(
        title=_(u"Find/Replace"),
        required=False)

    toolbar_style = schema.Bool(
        title=_(u"Select Style"),
        required=False)

    toolbar_bold = schema.Bool(
        title=_(u"Bold"),
        required=False)

    toolbar_italic = schema.Bool(
        title=_(u"Italic"),
        required=False)

    toolbar_underline = schema.Bool(
        title=_(u"Underline"),
        required=False)

    toolbar_strikethrough = schema.Bool(
        title=_(u"Strikethrough"),
        required=False)

    toolbar_sub = schema.Bool(
        title=_(u"Subscript"),
        required=False)

    toolbar_sup = schema.Bool(
        title=_(u"Superscript"),
        required=False)

    toolbar_forecolor = schema.Bool(
        title=_(u"Forecolor"),
        required=False)

    toolbar_backcolor = schema.Bool(
        title=_(u"Backcolor"),
        required=False)

    toolbar_justifyleft = schema.Bool(
        title=_(u"Align left"),
        required=False)

    toolbar_justifycenter = schema.Bool(
        title=_(u"Align center"),
        required=False)

    toolbar_justifyright = schema.Bool(
        title=_(u"Align right"),
        required=False)

    toolbar_justifyfull = schema.Bool(
        title=_(u"Align full"),
        required=False)

    toolbar_bullist = schema.Bool(
        title=_(u"Unordered list"),
        required=False)

    toolbar_numlist = schema.Bool(
        title=_(u"Ordered list"),
        required=False)

    toolbar_definitionlist = schema.Bool(
        title=_(u"Definition list"),
        required=False)

    toolbar_outdent = schema.Bool(
        title=_(u"Outdent"),
        required=False)

    toolbar_indent = schema.Bool(
        title=_(u"Indent"),
        required=False)

    toolbar_tablecontrols = schema.Bool(
        title=_(u"Table controls"),
        required=False)

    toolbar_link = schema.Bool(
        title=_(u"Insert/edit link"),
        required=False)

    toolbar_unlink = schema.Bool(
        title=_(u"Unlink"),
        required=False)

    toolbar_anchor = schema.Bool(
        title=_(u"Insert/edit anchor"),
        required=False)

    toolbar_image = schema.Bool(
        title=_(u"Insert/edit image"),
        required=False)

    toolbar_media = schema.Bool(
        title=_(u"Insert/edit media"),
        required=False)

    toolbar_charmap = schema.Bool(
        title=_(u"Insert custom character"),
        required=False)

    toolbar_hr = schema.Bool(
        title=_(u"Insert horizontal ruler"),
        required=False)

    toolbar_advhr = schema.Bool(
        title=_(u"Insert advanced horizontal ruler"),
        required=False)

    toolbar_insertdate = schema.Bool(
        title=_(u"Insert date"),
        required=False)

    toolbar_inserttime = schema.Bool(
        title=_(u"Insert time"),
        required=False)

    toolbar_emotions = schema.Bool(
        title=_(u"Emotions"),
        required=False)

    toolbar_nonbreaking = schema.Bool(
        title=_(u"Insert non-breaking space character"),
        required=False)

    toolbar_pagebreak = schema.Bool(
        title=_(u"Insert page break"),
        required=False)

    toolbar_print = schema.Bool(
        title=_(u"Print"),
        required=False)

    toolbar_preview = schema.Bool(
        title=_(u"Preview"),
        required=False)

    toolbar_spellchecker = schema.Bool(
        title=_(u"Spellchecker"),
        required=False)

    toolbar_removeformat = schema.Bool(
        title=_(u"Remove formatting"),
        required=False)

    toolbar_cleanup = schema.Bool(
        title=_(u"Cleanup messy code"),
        required=False)

    toolbar_visualaid = schema.Bool(
        title=_(u"Toggle guidelines/invisible objects"),
        required=False)

    toolbar_visualchars = schema.Bool(
        title=_(u"Visual control characters on/off"),
        required=False)

    toolbar_attribs = schema.Bool(
        title=_(u"Insert/edit attributes"),
        required=False)

    toolbar_code = schema.Bool(
        title=_(u"Edit HTML Source"),
        required=False)

    toolbar_fullscreen = schema.Bool(
        title=_(u"Toggle fullscreen mode"),
        required=False)

    customtoolbarbuttons = schema.Text(
        title=_(u"Custom Toolbar Buttons"),
        description=_(u"Enter a list of custom toolbar buttons which will be loaded in the editor, one per line."),
        required=False)


class ITinyMCELibraries(Interface):
    """This interface defines the libraries properties."""

    libraries_spellchecker_choice = schema.Choice(
        title=_(u"Spellchecker plugin to use"),
        description=_(u"This option allows you to choose the spellchecker for "
                      u"TinyMCE. If you want the spellchecker button to be "
                      u"visible, make sure it is enabled in the toolbar "
                      u"settings."),
        missing_value=set(),
        vocabulary=SimpleVocabulary([
                            SimpleTerm('browser', 'browser',
                                    _(u"Default browser spellchecker")),
                            SimpleTerm('iespell', 'iespell',
                                    _(u"ieSpell (free for personal use)")),
                            SimpleTerm('AtD', 'AtD',
                                    _(u"After the deadline (FLOSS)")),
                            ]),
        default='browser',
        required=False)

    libraries_atd_ignore_strings = schema.Text(
        title=_(u"AtD Ignore strings"),
        description=_(
            'label_atd_ignore_strings',
            default=u"A list of strings which the \"After the Deadline\"" \
                    u"spellchecker should ignore. " \
                    u"Note: This option is only applicable when the appropriate " \
                "spellchecker has been chosen above."),
        default=u"Zope\nPlone\nTinyMCE",
        required=False)

    libraries_atd_show_types = schema.Text(
        title=_(u"AtD Error types to show"),
        description=_(
            'help_atderrortypes_to_show',
            default=u"A list of error types which the " \
                    u"\"After the Deadline\" spellchecker should check for. " \
                    u"By default, all the available error type will be listed here."),
        default=u"Bias Language\nCliches\nComplex Expression\n" \
                u"Diacritical Marks\nDouble Negatives\n" \
                u"Hidden Verbs\nJargon Language\nPassive voice\n" \
                u"Phrases to Avoid\nRedundant Expression",
        required=False)

    libraries_atd_service_url = schema.TextLine(
        title=_(u"AtD Service URL"),
        description=_(
            'help_atd_service_url',
            default=u"The URL of the \"After the Deadline\" grammar and spell " \
                    u"checking server. The default value is the public server, " \
                    u"but ideally you should download and install your own and " \
                    u"specify its address here."),
        required=True,
        default=u"service.afterthedeadline.com",)


class ITinyMCEResourceTypes(Interface):
    """This interface defines the resource types properties."""

    link_using_uids = schema.Bool(
        title=_(u"Link using UIDs"),
        description=_(u"Links to objects on this site can use unique object ids so that the links remain valid even if the target object is renamed or moved elsewhere on the site."),
        required=False)

    allow_captioned_images = schema.Bool(
        title=_(u"Allow captioned images"),
        description=_(u"Images will be automatically captioned."),
        required=False)

    rooted = schema.Bool(
        title=_(u"Rooted to current object"),
        description=_(u"When enabled the user will be rooted to the current object and can't add links and images from other parts of the site."),
        required=False)

    containsobjects = schema.Text(
        title=_(u"Contains Objects"),
        description=_(u"Enter a list of content types which can contain other objects. Format is one contenttype per line."),
        required=False)

    containsanchors = schema.Text(
        title=_(u"Contains Anchors"),
        description=_(u"Enter a list of content types which can contain anchors. Format is one contenttype per line."),
        required=False)

    linkable = schema.Text(
        title=_(u"Linkable Objects"),
        description=_(u"Enter a list of content types which can be linked. Format is one contenttype per line."),
        required=False)

    imageobjects = schema.Text(
        title=_(u"Image Objects"),
        description=_(u"Enter a list of content types which can be used as images. Format is one contenttype per line."),
        required=False)

    plugins = schema.List(
        title=_("label_tinymce_plugins", default=u"Editor Plugins"),
        description=_("help_tinymce_plugins", default=(
            u"Enter a list of custom plugins which will be loaded in the "
            u"editor. Format is pluginname or pluginname|location, one per "
            u"line.")),
        value_type=schema.Choice(source=plugins_vocabulary,),
        default=DEFAULT_PLUGINS,
        required=False)

    customplugins = schema.Text(
        title=_(u"Custom Plugins"),
        description=_(u"Enter a list of custom plugins which will be loaded in the editor. Format is pluginname or pluginname|location, one per line."),
        required=False)

    entity_encoding = schema.Choice(
        title=_(u"Entity encoding"),
        description=_(u"This option controls how entities/characters get processed. Named: Characters will be converted into named entities based on the entities option. Numeric: Characters will be converted into numeric entities. Raw: All characters will be stored in non-entity form except these XML default entities: amp lt gt quot"),
        missing_value=set(),
        vocabulary=SimpleVocabulary([SimpleTerm('named', 'named', _(u"Named")), SimpleTerm('numeric', 'numeric', _(u"Numeric")), SimpleTerm('raw', 'raw', _(u"Raw"))]),
        required=False)


class ITinyMCEContentBrowser(Interface):
    """This interface defines the content browser properties."""

    link_shortcuts = schema.List(
        title=_("Link Shortcuts"),
        description=_(u"List of shortcuts to appear in link browser for quick navigation."),
        value_type=schema.Choice(source=shortcuts_vocabulary,),
        default=[_('Home'), _('Current Folder')],
        required=False,
    )

    image_shortcuts = schema.List(
        title=_("Image Shortcuts"),
        description=_(u"List of shortcuts to appear in image browser for quick navigation."),
        value_type=schema.Choice(source=shortcuts_vocabulary,),
        default=['Home', 'Current Folder'],
        required=False,
    )

    thumbnail_size = schema.Choice(
        title=_(u'Thumbnail size in thumbnails mode'),
        #description=_(u""),
        source=thumbnail_sizes_vocabulary,
        default=('tile', 64, 64),
    )

    num_of_thumb_columns = schema.Choice(
        title=_(u'Number of columns in thumbnails mode'),
        #description=_(u""),
        values=[2, 4, 8, 16],
        default=4,
    )

    anchor_selector = schema.TextLine(
        title=_(u"Anchor selector expression"),
        description=_(
            'help_anchor_selector',
            default=u"A CSS level 3 pattern used to match elements "
                    u"that can serve as anchors. The default value "
                    u"is to match headings."),
        required=True,
        default=u"h2,h3",
    )


class ITinyMCE(
    ITinyMCELayout,
    ITinyMCEToolbar,
    ITinyMCELibraries,
    ITinyMCEResourceTypes,
    ITinyMCEContentBrowser,
    ):
    """This interface defines the Utility."""

    def getContentType(object=None, field=None, fieldname=None):
        """ Get the content type of the field.
        """

    def getConfiguration(context=None, field=None, request=None):
        """ Get the configuration based on the control panel and field settings.

            The request can be provided for translation purpose.
        """

    def getImageScales(field=None, context=None):
        """
        """

    def getEnabledButtons(context):
        """
        """

    def translateButtonsFromKupu(context, buttons):
        """
        """

    def getValidElements():
        """ Return valid (X)HTML elements and their attributes.
        """

    def getPlugins():
        """ Return a comma seperated list of TinyMCE plugins
        """

    def getStyles(styles, labels):
        """ Return a list of styles for the use with TinyMCE
        """

    def getToolbars(config):
        """ Get toolbar buttons for the editor

            Calculate the number of toolbar rows from the length
            of the buttons.
        """
