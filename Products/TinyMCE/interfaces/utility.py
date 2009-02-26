from zope.interface import Interface
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

_ = MessageFactory('tinymce')

class ITinyMCELayout(Interface):
	"""This interface defines the layout properties."""

	resizing = schema.Bool(
		title=_(u'label_resizing', default=u"Enable resizing the editor window."),
		description=_(u"help_resizing", default=u"This option gives you the ability to enable/disable resizing the editor window. If the editor width is set to a percentage only vertical resizing is enabled."),
		default=True,
		required=False)

	autoresize = schema.Bool(
		title=_(u'label_autoresize', default=u"Enable auto resizing of the editor window."),
		description=_(u"help_autoresize", default=u"This option gives you the ability to enable/disable auto resizing the editor window depending on the content."),
		default=False,
		required=False)

	autoresize_bottom_margin = schema.TextLine(
		title=_(u'label_autoresize_bottom_margin', default=u"Bottom margin of the textfield when auto resizing is enabled."),
		description=_(u"help_autoresize_bottom_margin", default=u"This option gives you the ability to specify the bottom margin (in pixels) of the textfield when auto resizing of the editor window is enabled."),
		default=u'40',
		required=False)

	editor_width = schema.TextLine(
		title=_(u'label_editor_width', default=u'Editor width'),
		description=_(u'help_editor_width', default=u"This option gives you the ability to specify the width of the editor in pixels or percent."),
		default=u'100%',
		required=False) 

	editor_height = schema.TextLine(
		title=_(u'label_editor_height', default=u'Editor height'),
		description=_(u'help_editor_height', default=u"This option gives you the ability to specify the height of the editor in pixels. If auto resize is enabled this value is used as minimum height."),
		default=u'400',
		required=False) 

	directionality = schema.Choice(
		title=_(u'label_directionality', default=u'Writing direction'),
		description=_(u'help_directionality', default=u"This option specifies the default writing direction, some languages (Like Hebrew, Arabic, Urdu...) write from right to left instead of left to right."),
		default=u'ltr',
		missing_value=set(),
		vocabulary=SimpleVocabulary([SimpleTerm('ltr', 'Left to right'), SimpleTerm('rtl', 'Right to left')]),
		required=False)

	contextmenu = schema.Bool(
		title=_(u'label_contextmenu', default=u"Enable contextmenu."),
		description=_(u"help_contextmenu", default=u"This option gives you the ability to enable/disable the use of the contextmenu."),
		default=True,
		required=False)

	content_css = schema.TextLine(
		title=_(u'label_content_css', default=u'Choose the Css used in Wysiwyg Editor Area'),
		description=_(u'help_content_css', default=u"This option enables you to specify a custom CSS file that extends the theme content CSS. This CSS file is the one used within the editor (the editable area)."),
		default=u'',
		required=False)

	styles = schema.Text(
		title=_(u'label_styles', default=u'Styles'),
		description=_(u'help_styles', default=u"Enter a list of styles to appear in the style pulldown. Format is title|tag or title|tag|className, one per line."),
		default=u'Heading|h2\nSubheading|h3\nLiteral|pre\nDiscreet|p|discreet\nPull-quote|div|pullquote\nCall-out|p|callout\nHighlight|span|visualHighlight\nOdd row|tr|odd\nEven row|tr|even\nHeading cell|th|\nPage break (print only)|div|pageBreak\nClear floats|div|visualClear',
		required=False) 

	tablestyles = schema.Text(
		title=_(u'label_tablestyles', default=u'Table styles'),
		description=_(u'help_tablestyles', default=u"Enter a list of styles to appear in the table style pulldown. Format is title|class, one per line."),
		default=u'Subdued grid|plain\nInvisible grid|invisible\nFancy listing|listing\nFancy grid listing|grid listing\nFancy vertical listing|vertical listing',
		required=False) 

class ITinyMCEToolbar(Interface):
	"""This interface defines the toolbar properties."""

	toolbar_width = schema.TextLine(
		title=_(u'label_toolbar_width', default=u'Toolbar width'),
		description=_(u'help_toolbar_width', default=u"This option gives you the ability to specify the width of the toolbar in pixels."),
		default=u'440',
		required=False)

	toolbar_external = schema.Bool(
		title=_(u'label_toolbar_external', default=u"External"),
		description=_(u"help_toolbar_external", default=u"This option enables the external toolbar which will be placed at the top of the page."),
		default=False,
		required=False)

	toolbar_save = schema.Bool(
		title=_(u'label_toolbar_save', default=u"Save"),
		description=_(u"help_toolbar_save", default=u""),
		default=True,
		required=False)

	toolbar_cut = schema.Bool(
		title=_(u'label_toolbar_cut', default=u"Cut"),
		description=_(u"help_toolbar_cut", default=u""),
		default=False,
		required=False)

	toolbar_copy = schema.Bool(
		title=_(u'label_toolbar_copy', default=u"Copy"),
		description=_(u"help_toolbar_copy", default=u""),
		default=False,
		required=False)

	toolbar_paste = schema.Bool(
		title=_(u'label_toolbar_paste', default=u"Paste"),
		description=_(u"help_toolbar_paste", default=u""),
		default=False,
		required=False)

	toolbar_pastetext = schema.Bool(
		title=_(u'label_toolbar_pastetext', default=u"Paste as Plain Text"),
		description=_(u"help_toolbar_pastetext", default=u""),
		default=False,
		required=False)

	toolbar_pasteword = schema.Bool(
		title=_(u'label_toolbar_pasteword', default=u"Paste from Word"),
		description=_(u"help_toolbar_pasteword", default=u""),
		default=False,
		required=False)

	toolbar_undo = schema.Bool(
		title=_(u'label_toolbar_undo', default=u"Undo"),
		description=_(u"help_toolbar_undo", default=u""),
		default=False,
		required=False)

	toolbar_redo = schema.Bool(
		title=_(u'label_toolbar_redo', default=u"Redo"),
		description=_(u"help_toolbar_redo", default=u""),
		default=False,
		required=False)

	toolbar_search = schema.Bool(
		title=_(u'label_toolbar_search', default=u"Find"),
		description=_(u"help_toolbar_search", default=u""),
		default=False,
		required=False)

	toolbar_replace = schema.Bool(
		title=_(u'label_toolbar_replace', default=u"Find/Replace"),
		description=_(u"help_toolbar_replace", default=u""),
		default=False,
		required=False)

	toolbar_style = schema.Bool(
		title=_(u'label_toolbar_style', default=u"Select Style"),
		description=_(u"help_toolbar_style", default=u""),
		default=True,
		required=False)

	toolbar_bold = schema.Bool(
		title=_(u'label_toolbar_bold', default=u"Bold"),
		description=_(u"help_toolbar_bold", default=u""),
		default=True,
		required=False)

	toolbar_italic = schema.Bool(
		title=_(u'label_toolbar_italic', default=u"Italic"),
		description=_(u"help_toolbar_italic", default=u""),
		default=True,
		required=False)

	toolbar_underline = schema.Bool(
		title=_(u'label_toolbar_underline', default=u"Underline"),
		description=_(u"help_toolbar_underline", default=u""),
		default=False,
		required=False)

	toolbar_strikethrough = schema.Bool(
		title=_(u'label_toolbar_strikethrough', default=u"Strikethrough"),
		description=_(u"help_toolbar_strikethrough", default=u""),
		default=False,
		required=False)

	toolbar_sub = schema.Bool(
		title=_(u'label_toolbar_sub', default=u"Subscript"),
		description=_(u"help_toolbar_sub", default=u""),
		default=False,
		required=False)

	toolbar_sup = schema.Bool(
		title=_(u'label_toolbar_sup', default=u"Superscript"),
		description=_(u"help_toolbar_sup", default=u""),
		default=False,
		required=False)

	toolbar_forecolor = schema.Bool(
		title=_(u'label_toolbar_forecolor', default=u"Forecolor"),
		description=_(u"help_toolbar_forecolor", default=u""),
		default=False,
		required=False)

	toolbar_backcolor = schema.Bool(
		title=_(u'label_toolbar_backcolor', default=u"Backcolor"),
		description=_(u"help_toolbar_backcolor", default=u""),
		default=False,
		required=False)

	toolbar_justifyleft = schema.Bool(
		title=_(u'label_toolbar_justifyleft', default=u"Align left"),
		description=_(u"help_toolbar_justifyleft", default=u""),
		default=True,
		required=False)

	toolbar_justifycenter = schema.Bool(
		title=_(u'label_toolbar_justifycenter', default=u"Align center"),
		description=_(u"help_toolbar_justifycenter", default=u""),
		default=True,
		required=False)

	toolbar_justifyright = schema.Bool(
		title=_(u'label_toolbar_justifyright', default=u"Align right"),
		description=_(u"help_toolbar_justifyright", default=u""),
		default=True,
		required=False)

	toolbar_justifyfull = schema.Bool(
		title=_(u'label_toolbar_justifyfull', default=u"Align full"),
		description=_(u"help_toolbar_justifyfull", default=u""),
		default=True,
		required=False)

	toolbar_bullist = schema.Bool(
		title=_(u'label_toolbar_bullist', default=u"Unordered list"),
		description=_(u"help_toolbar_bullist", default=u""),
		default=True,
		required=False)

	toolbar_numlist = schema.Bool(
		title=_(u'label_toolbar_numlist', default=u"Ordered list"),
		description=_(u"help_toolbar_numlist", default=u""),
		default=True,
		required=False)

	toolbar_outdent = schema.Bool(
		title=_(u'label_toolbar_outdent', default=u"Outdent"),
		description=_(u"help_toolbar_outdent", default=u""),
		default=True,
		required=False)

	toolbar_indent = schema.Bool(
		title=_(u'label_toolbar_indent', default=u"Indent"),
		description=_(u"help_toolbar_indent", default=u""),
		default=True,
		required=False)

	toolbar_tablecontrols = schema.Bool(
		title=_(u'label_toolbar_tablecontrols', default=u"Table controls"),
		description=_(u"help_toolbar_tablecontrols", default=u""),
		default=True,
		required=False)

	toolbar_link = schema.Bool(
		title=_(u'label_toolbar_link', default=u"Insert/edit link"),
		description=_(u"help_toolbar_link", default=u""),
		default=True,
		required=False)

	toolbar_unlink = schema.Bool(
		title=_(u'label_toolbar_unlink', default=u"Unlink"),
		description=_(u"help_toolbar_unlink", default=u""),
		default=True,
		required=False)

	toolbar_anchor = schema.Bool(
		title=_(u'label_toolbar_anchor', default=u"Insert/edit anchor"),
		description=_(u"help_toolbar_anchor", default=u""),
		default=True,
		required=False)

	toolbar_image = schema.Bool(
		title=_(u'label_toolbar_image', default=u"Insert/edit image"),
		description=_(u"help_toolbar_image", default=u""),
		default=True,
		required=False)

	toolbar_media = schema.Bool(
		title=_(u'label_toolbar_media', default=u"Insert/edit media"),
		description=_(u"help_toolbar_media", default=u""),
		default=False,
		required=False)

	toolbar_charmap = schema.Bool(
		title=_(u'label_toolbar_charmap', default=u"Insert custom character"),
		description=_(u"help_toolbar_charmap", default=u""),
		default=False,
		required=False)

	toolbar_hr = schema.Bool(
		title=_(u'label_toolbar_hr', default=u"Insert horizontal ruler"),
		description=_(u"help_toolbar_hr", default=u""),
		default=False,
		required=False)

	toolbar_advhr = schema.Bool(
		title=_(u'label_toolbar_advhr', default=u"Insert advanced horizontal ruler"),
		description=_(u"help_toolbar_advhr", default=u""),
		default=False,
		required=False)

	toolbar_insertdate = schema.Bool(
		title=_(u'label_toolbar_insertdate', default=u"Insert date"),
		description=_(u"help_toolbar_insertdate", default=u""),
		default=False,
		required=False)

	toolbar_inserttime = schema.Bool(
		title=_(u'label_toolbar_inserttime', default=u"Insert time"),
		description=_(u"help_toolbar_inserttime", default=u""),
		default=False,
		required=False)

	toolbar_emotions = schema.Bool(
		title=_(u'label_toolbar_emotions', default=u"Emotions"),
		description=_(u"help_toolbar_emotions", default=u""),
		default=False,
		required=False)

	toolbar_nonbreaking = schema.Bool(
		title=_(u'label_toolbar_nonbreaking', default=u"Insert non-breaking space character"),
		description=_(u"help_toolbar_nonbreaking", default=u""),
		default=False,
		required=False)

	toolbar_pagebreak = schema.Bool(
		title=_(u'label_toolbar_pagebreak', default=u"Insert page break"),
		description=_(u"help_toolbar_pagebreak", default=u""),
		default=False,
		required=False)

	toolbar_print = schema.Bool(
		title=_(u'label_toolbar_print', default=u"Print"),
		description=_(u"help_toolbar_print", default=u""),
		default=False,
		required=False)

	toolbar_preview = schema.Bool(
		title=_(u'label_toolbar_preview', default=u"Preview"),
		description=_(u"help_toolbar_preview", default=u""),
		default=False,
		required=False)

	toolbar_iespell = schema.Bool(
		title=_(u'label_toolbar_iespell', default=u"Spellchecker"),
		description=_(u"help_toolbar_iespell", default=u""),
		default=False,
		required=False)

	toolbar_removeformat = schema.Bool(
		title=_(u'label_toolbar_removeformat', default=u"Remove formatting"),
		description=_(u"help_toolbar_removeformat", default=u""),
		default=False,
		required=False)

	toolbar_cleanup = schema.Bool(
		title=_(u'label_toolbar_cleanup', default=u"Cleanup messy code"),
		description=_(u"help_toolbar_cleanup", default=u""),
		default=False,
		required=False)

	toolbar_visualaid = schema.Bool(
		title=_(u'label_toolbar_visualaid', default=u"Toggle guidelines/invisible objects"),
		description=_(u"help_toolbar_visualaid", default=u""),
		default=False,
		required=False)

	toolbar_visualchars = schema.Bool(
		title=_(u'label_toolbar_visualchars', default=u"Visual control characters on/off"),
		description=_(u"help_toolbar_visualchars", default=u""),
		default=False,
		required=False)

	toolbar_code = schema.Bool(
		title=_(u'label_toolbar_code', default=u"Edit HTML Source"),
		description=_(u"help_toolbar_code", default=u""),
		default=True,
		required=False)

	toolbar_fullscreen = schema.Bool(
		title=_(u'label_toolbar_fullscreen', default=u"Toggle fullscreen mode"),
		description=_(u"help_toolbar_fullscreen", default=u""),
		default=True,
		required=False)

class ITinyMCELibraries(Interface):
	"""This interface defines the libraries properties."""

class ITinyMCEResourceTypes(Interface):
	"""This interface defines the resource types properties."""

	link_using_uids = schema.Bool(
		title=_(u'label_link_using_uids', default=u"Link using UIDs"),
		description=_(u"help_link_using_uids", default=u"Links to objects on this site can use unique object ids so that the links remain valid even if the target object is renamed or moved elsewhere on the site."),
		default=False,
		required=False)

	allow_captioned_images = schema.Bool(
		title=_(u'label_allow_captioned_images', default=u"Allow captioned images"),
		description=_(u"help_allow_captioned_images", default=u"Images will be automatically captioned."),
		default=False,
		required=False)

	containsobjects = schema.Text(
		title=_(u'label_containsobjects', default=u'Contains Objects'),
		description=_(u'help_containsobjects', default=u"Enter a list of content types which can contain other objects. Format is one contenttype per line."),
		default=u'ATFolder\nATBTreeFolder\nPlone Site',
		required=False) 

	containsanchors = schema.Text(
		title=_(u'label_containsanchors', default=u'Contains Anchors'),
		description=_(u'help_containsanchors', default=u"Enter a list of content types which can contain anchors. Format is one contenttype per line."),
		default=u'ATEvent\nATNewsItem\nATDocument\nATRelativePathCriterion',
		required=False) 

	linkable = schema.Text(
		title=_(u'label_linkable', default=u'Linkable Objects'),
		description=_(u'help_linkable', default=u"Enter a list of content types which can be linked. Format is one contenttype per line."),
		default=u'ATTopic\nATEvent\nATFile\nATFolder\nATImage\nATBTreeFolder\nATNewsItem\nATDocument',
		required=False) 

	imageobjects = schema.Text(
		title=_(u'label_imageobjects', default=u'Image Objects'),
		description=_(u'help_linkable', default=u"Enter a list of content types which can be used as images. Format is one contenttype per line."),
		default=u'ATImage',
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
