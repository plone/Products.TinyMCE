from zope.schema import getFieldsInOrder
from zope.schema.interfaces import IText, IBool, ITextLine

from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase

from Products.CMFCore.utils import getToolByName

from Products.TinyMCE.interfaces.utility import ITinyMCELayout
from Products.TinyMCE.interfaces.utility import ITinyMCEToolbar
from Products.TinyMCE.interfaces.utility import ITinyMCEResourceTypes

class TinyMCESettingsXMLAdapter(XMLAdapterBase):

    attributes = {
        'layout' : {
            'resizing' : 'Bool',
            'autoresize' : 'Bool',
            'editor_width' : 'Text',
            'editor_height' : 'Text',
            'directionality' : 'Text',
            'content_css' : 'Text',
            'styles' : 'List',
            'tablestyles' : 'List',
        },
        'toolbar' : {
            'toolbar_width' : 'Text',
            'toolbar_external' : 'Bool',
            'toolbar_save' : 'Bool',
            'toolbar_cut' : 'Bool',
            'toolbar_copy' : 'Bool',
            'toolbar_paste' : 'Bool',
            'toolbar_pastetext' : 'Bool',
            'toolbar_pasteword' : 'Bool',
            'toolbar_undo' : 'Bool',
            'toolbar_redo' : 'Bool',
            'toolbar_search' : 'Bool',
            'toolbar_replace' : 'Bool',
            'toolbar_style' : 'Bool',
            'toolbar_bold' : 'Bool',
            'toolbar_italic' : 'Bool',
            'toolbar_underline' : 'Bool',
            'toolbar_strikethrough' : 'Bool',
            'toolbar_sub' : 'Bool',
            'toolbar_sup' : 'Bool',
            'toolbar_forecolor' : 'Bool',
            'toolbar_backcolor' : 'Bool',
            'toolbar_justifyleft' : 'Bool',
            'toolbar_justifycenter' : 'Bool',
            'toolbar_justifyright' : 'Bool',
            'toolbar_justifyfull' : 'Bool',
            'toolbar_bullist' : 'Bool',
            'toolbar_numlist' : 'Bool',
            'toolbar_outdent' : 'Bool',
            'toolbar_indent' : 'Bool',
            'toolbar_tablecontrols' : 'Bool',
            'toolbar_link' : 'Bool',
            'toolbar_unlink' : 'Bool',
            'toolbar_anchor' : 'Bool',
            'toolbar_image' : 'Bool',
            'toolbar_media' : 'Bool',
            'toolbar_charmap' : 'Bool',
            'toolbar_hr' : 'Bool',
            'toolbar_advhr' : 'Bool',
            'toolbar_insertdate' : 'Bool',
            'toolbar_inserttime' : 'Bool',
            'toolbar_emotions' : 'Bool',
            'toolbar_nonbreaking' : 'Bool',
            'toolbar_pagebreak' : 'Bool',
            'toolbar_print' : 'Bool',
            'toolbar_preview' : 'Bool',
            'toolbar_iespell' : 'Bool',
            'toolbar_removeformat' : 'Bool',
            'toolbar_cleanup' : 'Bool',
            'toolbar_visualaid' : 'Bool',
            'toolbar_visualchars' : 'Bool',
            'toolbar_code' : 'Bool',
            'toolbar_fullscreen' : 'Bool',
        },
        'resourcetypes' : {
            'containsobjects' : 'List',
            'containsanchors' : 'List',
            'linkable' : 'List',
            'imageobjects' : 'List',
        }
    }

    def _exportNode(self):
        """Export the object as a DOM node"""

        object = self._doc.createElement('object')

        # Loop through categories
        for key in self.attributes.keys():
            category = self.attributes[key]
            categorynode = self._doc.createElement(key)

            # Loop through fields in category
            for field in category.keys():
                fieldnode = self._doc.createElement(field)
                fieldvalue = getattr(self.context, field)

                if category[field] == 'Bool':
                    fieldnode.setAttribute('value', unicode(bool(fieldvalue)))
                elif category[field] == 'Text':

                    # Check for NoneType
                    if fieldvalue:
                        fieldnode.setAttribute('value', fieldvalue)
                    else:
                        fieldnode.setAttribute('value', '')
                elif category[field] == 'List':
                    for value in fieldvalue.split('\n'):
                        if value:
                            child = self._doc.createElement('element')
                            child.setAttribute('value', value)
                            fieldnode.appendChild(child)
                categorynode.appendChild(fieldnode)
            object.appendChild(categorynode)
        return object

    def _importNode(self, node):
        """Import the object from the DOM node"""

        pass

def importTinyMCESettings(context):
    """Import TinyMCE Settings"""
    site = context.getSite()
    tool = getToolByName(site, 'portal_tinymce')

    importObjects(tool, '', context)

def exportTinyMCESettings(context):
    """Export TinyMCE Settings"""
    site = context.getSite()
    tool = getToolByName(site, 'portal_tinymce', None)
    if tool is None:
        return

    exportObjects(tool, '', context)
