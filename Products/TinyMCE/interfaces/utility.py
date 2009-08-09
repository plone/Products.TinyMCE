from zope.interface import Interface
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

_ = MessageFactory('plone.tinymce')

class ITinyMCELayout(Interface):
    """This interface defines the layout properties."""

    resizing = schema.Bool(
        title=_(u"Enable resizing the editor window."),
        description=_(u"This option gives you the ability to enable/disable resizing the editor window. If the editor width is set to a percentage only vertical resizing is enabled."),
        default=True,
        required=False)

    autoresize = schema.Bool(
        title=_(u"Enable auto resizing of the editor window."),
        description=_(u"This option gives you the ability to enable/disable auto resizing the editor window depending on the content."),
        default=False,
        required=False)

    autoresize_bottom_margin = schema.TextLine(
        title=_(u"Bottom margin of the textfield when auto resizing is enabled."),
        description=_(u"This option gives you the ability to specify the bottom margin (in pixels) of the textfield when auto resizing of the editor window is enabled."),
        default=u'40',
        required=False)

    editor_width = schema.TextLine(
        title=_(u"Editor width"),
        description=_(u"This option gives you the ability to specify the width of the editor in pixels or percent."),
        default=u'100%',
        required=False) 

    editor_height = schema.TextLine(
        title=_(u"Editor height"),
        description=_(u"This option gives you the ability to specify the height of the editor in pixels. If auto resize is enabled this value is used as minimum height."),
        default=u'400',
        required=False) 

    directionality = schema.Choice(
        title=_(u"Writing direction"),
        description=_(u"This option specifies the default writing direction, some languages (Like Hebrew, Arabic, Urdu...) write from right to left instead of left to right."),
        default=u'ltr',
        missing_value=set(),
        vocabulary=SimpleVocabulary([SimpleTerm('ltr', 'Left to right'), SimpleTerm('rtl', 'Right to left')]),
        required=False)

    contextmenu = schema.Bool(
        title=_(u"Enable contextmenu."),
        description=_(u"This option gives you the ability to enable/disable the use of the contextmenu."),
        default=True,
        required=False)

    content_css = schema.TextLine(
        title=_(u"Choose the Css used in Wysiwyg Editor Area"),
        description=_(u"This option enables you to specify a custom CSS file that extends the theme content CSS. This CSS file is the one used within the editor (the editable area)."),
        default=u'',
        required=False)

    styles = schema.Text(
        title=_(u"Styles"),
        description=_(u"Enter a list of styles to appear in the style pulldown. Format is title|tag or title|tag|className, one per line."),
        default=u'Heading|h2\nSubheading|h3\nLiteral|pre\nDiscreet|p|discreet\nPull-quote|div|pullquote\nCall-out|p|callout\nHighlight|span|visualHighlight\nOdd row|tr|odd\nEven row|tr|even\nHeading cell|th|\nPage break (print only)|div|pageBreak\nClear floats|div|visualClear',
        required=False) 

    tablestyles = schema.Text(
        title=_(u"Table styles"),
        description=_(u"Enter a list of styles to appear in the table style pulldown. Format is title|class, one per line."),
        default=u'Subdued grid|plain\nInvisible grid|invisible\nFancy listing|listing\nFancy grid listing|grid listing\nFancy vertical listing|vertical listing',
        required=False) 

    imagesizes = schema.Tuple(
        title=_(u'label_imagesizes', default=u'Image Sizes'),
        description=_(u'help_imagesizes', default=u"Select the image sizes to show in the browser"),
        value_type = schema.Choice(vocabulary = 'tinymce.imagescales'),
        required=False) 

class ITinyMCEToolbar(Interface):
    """This interface defines the toolbar properties."""

    toolbar_width = schema.TextLine(
        title=_(u"Toolbar width"),
        description=_(u"This option gives you the ability to specify the width of the toolbar in pixels."),
        default=u'440',
        required=False)

    toolbar_external = schema.Bool(
        title=_(u"External"),
        description=_(u"This option enables the external toolbar which will be placed at the top of the page."),
        default=False,
        required=False)

    toolbar_save = schema.Bool(
        title=_(u"Save"),
        default=True,
        required=False)

    toolbar_cut = schema.Bool(
        title=_(u"Cut"),
        default=False,
        required=False)

    toolbar_copy = schema.Bool(
        title=_(u"Copy"),
        default=False,
        required=False)

    toolbar_paste = schema.Bool(
        title=_(u"Paste"),
        default=False,
        required=False)

    toolbar_pastetext = schema.Bool(
        title=_(u"Paste as Plain Text"),
        default=False,
        required=False)

    toolbar_pasteword = schema.Bool(
        title=_(u"Paste from Word"),
        default=False,
        required=False)

    toolbar_undo = schema.Bool(
        title=_(u"Undo"),
        default=False,
        required=False)

    toolbar_redo = schema.Bool(
        title=_(u"Redo"),
        default=False,
        required=False)

    toolbar_search = schema.Bool(
        title=_(u"Find"),
        default=False,
        required=False)

    toolbar_replace = schema.Bool(
        title=_(u"Find/Replace"),
        default=False,
        required=False)

    toolbar_style = schema.Bool(
        title=_(u"Select Style"),
        default=True,
        required=False)

    toolbar_bold = schema.Bool(
        title=_(u"Bold"),
        default=True,
        required=False)

    toolbar_italic = schema.Bool(
        title=_(u"Italic"),
        default=True,
        required=False)

    toolbar_underline = schema.Bool(
        title=_(u"Underline"),
        default=False,
        required=False)

    toolbar_strikethrough = schema.Bool(
        title=_(u"Strikethrough"),
        default=False,
        required=False)

    toolbar_sub = schema.Bool(
        title=_(u"Subscript"),
        default=False,
        required=False)

    toolbar_sup = schema.Bool(
        title=_(u"Superscript"),
        default=False,
        required=False)

    toolbar_forecolor = schema.Bool(
        title=_(u"Forecolor"),
        default=False,
        required=False)

    toolbar_backcolor = schema.Bool(
        title=_(u"Backcolor"),
        default=False,
        required=False)

    toolbar_justifyleft = schema.Bool(
        title=_(u"Align left"),
        default=True,
        required=False)

    toolbar_justifycenter = schema.Bool(
        title=_(u"Align center"),
        default=True,
        required=False)

    toolbar_justifyright = schema.Bool(
        title=_(u"Align right"),
        default=True,
        required=False)

    toolbar_justifyfull = schema.Bool(
        title=_(u"Align full"),
        default=True,
        required=False)

    toolbar_bullist = schema.Bool(
        title=_(u"Unordered list"),
        default=True,
        required=False)

    toolbar_numlist = schema.Bool(
        title=_(u"Ordered list"),
        default=True,
        required=False)

    toolbar_outdent = schema.Bool(
        title=_(u"Outdent"),
        default=True,
        required=False)

    toolbar_indent = schema.Bool(
        title=_(u"Indent"),
        default=True,
        required=False)

    toolbar_tablecontrols = schema.Bool(
        title=_(u"Table controls"),
        default=True,
        required=False)

    toolbar_link = schema.Bool(
        title=_(u"Insert/edit link"),
        default=True,
        required=False)

    toolbar_unlink = schema.Bool(
        title=_(u"Unlink"),
        default=True,
        required=False)

    toolbar_anchor = schema.Bool(
        title=_(u"Insert/edit anchor"),
        default=True,
        required=False)

    toolbar_image = schema.Bool(
        title=_(u"Insert/edit image"),
        default=True,
        required=False)

    toolbar_media = schema.Bool(
        title=_(u"Insert/edit media"),
        default=False,
        required=False)

    toolbar_charmap = schema.Bool(
        title=_(u"Insert custom character"),
        default=False,
        required=False)

    toolbar_hr = schema.Bool(
        title=_(u"Insert horizontal ruler"),
        default=False,
        required=False)

    toolbar_advhr = schema.Bool(
        title=_(u"Insert advanced horizontal ruler"),
        default=False,
        required=False)

    toolbar_insertdate = schema.Bool(
        title=_(u"Insert date"),
        default=False,
        required=False)

    toolbar_inserttime = schema.Bool(
        title=_(u"Insert time"),
        default=False,
        required=False)

    toolbar_emotions = schema.Bool(
        title=_(u"Emotions"),
        default=False,
        required=False)

    toolbar_nonbreaking = schema.Bool(
        title=_(u"Insert non-breaking space character"),
        default=False,
        required=False)

    toolbar_pagebreak = schema.Bool(
        title=_(u"Insert page break"),
        default=False,
        required=False)

    toolbar_print = schema.Bool(
        title=_(u"Print"),
        default=False,
        required=False)

    toolbar_preview = schema.Bool(
        title=_(u"Preview"),
        default=False,
        required=False)

    toolbar_iespell = schema.Bool(
        title=_(u"Spellchecker"),
        default=False,
        required=False)

    toolbar_removeformat = schema.Bool(
        title=_(u"Remove formatting"),
        default=False,
        required=False)

    toolbar_cleanup = schema.Bool(
        title=_(u"Cleanup messy code"),
        default=False,
        required=False)

    toolbar_visualaid = schema.Bool(
        title=_(u"Toggle guidelines/invisible objects"),
        default=False,
        required=False)

    toolbar_visualchars = schema.Bool(
        title=_(u"Visual control characters on/off"),
        default=False,
        required=False)

    toolbar_attribs = schema.Bool(
        title=_(u"Insert/edit attributes"),
        default=False,
        required=False)

    toolbar_code = schema.Bool(
        title=_(u"Edit HTML Source"),
        default=True,
        required=False)

    toolbar_fullscreen = schema.Bool(
        title=_(u"Toggle fullscreen mode"),
        default=True,
        required=False)

    customtoolbarbuttons = schema.Text(
        title=_(u"Custom Toolbar Buttons"),
        description=_(u"Enter a list of custom toolbar buttons which will be loaded in the editor, one per line."),
        default=u'',
        required=False) 

class ITinyMCELibraries(Interface):
    """This interface defines the libraries properties."""

class ITinyMCEResourceTypes(Interface):
    """This interface defines the resource types properties."""

    link_using_uids = schema.Bool(
        title=_(u"Link using UIDs"),
        description=_(u"Links to objects on this site can use unique object ids so that the links remain valid even if the target object is renamed or moved elsewhere on the site."),
        default=False,
        required=False)

    allow_captioned_images = schema.Bool(
        title=_(u"Allow captioned images"),
        description=_(u"Images will be automatically captioned."),
        default=False,
        required=False)

    rooted = schema.Bool(
        title=_(u'label_rooted', default=u"Rooted to current object"),
        description=_(u"help_rooted", default=u"When enabled the user will be rooted to the current object and can't add links and images from other parts of the site."),
        default=False,
        required=False)

    containsobjects = schema.Text(
        title=_(u"Contains Objects"),
        description=_(u"Enter a list of content types which can contain other objects. Format is one contenttype per line."),
        default=u'',
        required=False) 

    containsanchors = schema.Text(
        title=_(u"Contains Anchors"),
        description=_(u"Enter a list of content types which can contain anchors. Format is one contenttype per line."),
        default=u'',
        required=False) 

    linkable = schema.Text(
        title=_(u"Linkable Objects"),
        description=_(u"Enter a list of content types which can be linked. Format is one contenttype per line."),
        default=u'',
        required=False) 

    imageobjects = schema.Text(
        title=_(u"Image Objects"),
        description=_(u"Enter a list of content types which can be used as images. Format is one contenttype per line."),
        default=u'',
        required=False) 

    customplugins = schema.Text(
        title=_(u"Custom Plugins"),
        description=_(u"Enter a list of custom plugins which will be loaded in the editor. Format is pluginname or pluginname|location, one per line."),
        default=u'',
        required=False) 

    entity_encoding = schema.Choice(
        title=_(u"Entity encoding"),
        description=_(u"This option controls how entities/characters get processed. Named: Characters will be converted into named entities based on the entities option. Numeric: Characters will be converted into numeric entities. Raw: All characters will be stored in non-entity form except these XML default entities: amp lt gt quot"),
        default=u'raw',
        missing_value=set(),
        vocabulary=SimpleVocabulary([SimpleTerm('named', 'Named'), SimpleTerm('numeric', 'Numeric'), SimpleTerm('raw', 'Raw')]),
        required=False)

class ITinyMCE(
    ITinyMCELayout,
    ITinyMCEToolbar,
    ITinyMCELibraries,
    ITinyMCEResourceTypes
    ):
    """This interface defines the Utility."""

    def isTinyMCEEnabled(useragent='', allowAnonymous=False, REQUEST=None, context=None, fieldName=None):
        """Is TinyMCE enabled for this combination of client browser, permissions, and field."""

    def getContentType(self, object=None, fieldname=None):
        """Get the content type of the field."""

    def getConfiguration(self, context=None, field=None):
        """Get the configuration based on the control panel settings and the field settings."""
