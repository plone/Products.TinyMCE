from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility
from zope.interface import classProvides

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

    resizing = FieldProperty(ITinyMCELayout['resizing'])
    editor_width = FieldProperty(ITinyMCELayout['editor_width'])
    editor_height = FieldProperty(ITinyMCELayout['editor_height'])
    directionality = FieldProperty(ITinyMCELayout['directionality'])
    content_css = FieldProperty(ITinyMCELayout['content_css'])
    blockformats = FieldProperty(ITinyMCELayout['blockformats'])
    styles = FieldProperty(ITinyMCELayout['styles'])
    tablestyles = FieldProperty(ITinyMCELayout['tablestyles'])
    rowstyles = FieldProperty(ITinyMCELayout['rowstyles'])
    cellstyles = FieldProperty(ITinyMCELayout['cellstyles'])

    toolbar_width = FieldProperty(ITinyMCEToolbar['toolbar_width'])
    
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

    toolbar_formatselect = FieldProperty(ITinyMCEToolbar['toolbar_formatselect'])
    toolbar_styleselect = FieldProperty(ITinyMCEToolbar['toolbar_styleselect'])

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
