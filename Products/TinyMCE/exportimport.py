from zope.schema import getFieldsInOrder
from zope.schema.interfaces import IText, IBool, ITextLine

from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase

from Products.CMFCore.utils import getToolByName

from Products.TinyMCE.interfaces.utility import ITinyMCELayout
from Products.TinyMCE.interfaces.utility import ITinyMCEToolbar
from Products.TinyMCE.interfaces.utility import ITinyMCEResourceTypes
from Products.TinyMCE.setuphandlers import register_transform_policy, TINYMCE_OUTPUT_TRANSFORMATION


class TinyMCESettingsXMLAdapter(XMLAdapterBase):

    name = 'tinymce'

    _LOGGER_ID = 'portal_tinymce'

    attributes = {
        'layout' : {
            'resizing' : {'type' : 'Bool', 'default' : True},
            'autoresize' : {'type' : 'Bool', 'default' : False},
            'autoresize_bottom_margin' : {'type' : 'Text', 'default' : '40'},
            'editor_width' : {'type' : 'Text', 'default' : '100%'},
            'editor_height' : {'type' : 'Text', 'default' : '400'},
            'directionality' : {'type' : 'Text', 'default' : 'ltr'},
            'content_css' : {'type' : 'Text', 'default' : ''},
            'styles' : {'type' : 'List', 'default' : 'Heading|h2\nSubheading|h3\nLiteral|pre\nDiscreet|p|discreet\nPull-quote|div|pullquote\nCall-out|p|callout\nHighlight|span|visualHighlight\nOdd row|tr|odd\nEven row|tr|even\nHeading cell|th|\nPage break (print only)|div|pageBreak\nClear floats|div|visualClear'},
            'tablestyles' : {'type' : 'List', 'default' : 'Subdued grid|plain\nInvisible grid|invisible\nFancy listing|listing\nFancy grid listing|grid listing\nFancy vertical listing|vertical listing'},
        },
        'toolbar' : {
            'toolbar_width' : {'type' : 'Text', 'default' : '440'},
            'toolbar_external' : {'type' : 'Bool', 'default' : False},
            'toolbar_save' : {'type' : 'Bool', 'default' : True},
            'toolbar_cut' : {'type' : 'Bool', 'default' : False},
            'toolbar_copy' : {'type' : 'Bool', 'default' : False},
            'toolbar_paste' : {'type' : 'Bool', 'default' : False},
            'toolbar_pastetext' : {'type' : 'Bool', 'default' : False},
            'toolbar_pasteword' : {'type' : 'Bool', 'default' : False},
            'toolbar_undo' : {'type' : 'Bool', 'default' : False},
            'toolbar_redo' : {'type' : 'Bool', 'default' : False},
            'toolbar_search' : {'type' : 'Bool', 'default' : False},
            'toolbar_replace' : {'type' : 'Bool', 'default' : False},
            'toolbar_style' : {'type' : 'Bool', 'default' : True},
            'toolbar_bold' : {'type' : 'Bool', 'default' : True},
            'toolbar_italic' : {'type' : 'Bool', 'default' : True},
            'toolbar_underline' : {'type' : 'Bool', 'default' : False},
            'toolbar_strikethrough' : {'type' : 'Bool', 'default' : False},
            'toolbar_sub' : {'type' : 'Bool', 'default' : False},
            'toolbar_sup' : {'type' : 'Bool', 'default' : False},
            'toolbar_forecolor' : {'type' : 'Bool', 'default' : False},
            'toolbar_backcolor' : {'type' : 'Bool', 'default' : False},
            'toolbar_justifyleft' : {'type' : 'Bool', 'default' : True},
            'toolbar_justifycenter' : {'type' : 'Bool', 'default' : True},
            'toolbar_justifyright' : {'type' : 'Bool', 'default' : True},
            'toolbar_justifyfull' : {'type' : 'Bool', 'default' : True},
            'toolbar_bullist' : {'type' : 'Bool', 'default' : True},
            'toolbar_numlist' : {'type' : 'Bool', 'default' : True},
            'toolbar_outdent' : {'type' : 'Bool', 'default' : True},
            'toolbar_indent' : {'type' : 'Bool', 'default' : True},
            'toolbar_tablecontrols' : {'type' : 'Bool', 'default' : True},
            'toolbar_link' : {'type' : 'Bool', 'default' : True},
            'toolbar_unlink' : {'type' : 'Bool', 'default' : True},
            'toolbar_anchor' : {'type' : 'Bool', 'default' : True},
            'toolbar_image' : {'type' : 'Bool', 'default' : True},
            'toolbar_media' : {'type' : 'Bool', 'default' : False},
            'toolbar_charmap' : {'type' : 'Bool', 'default' : False},
            'toolbar_hr' : {'type' : 'Bool', 'default' : False},
            'toolbar_advhr' : {'type' : 'Bool', 'default' : False},
            'toolbar_insertdate' : {'type' : 'Bool', 'default' : False},
            'toolbar_inserttime' : {'type' : 'Bool', 'default' : False},
            'toolbar_emotions' : {'type' : 'Bool', 'default' : False},
            'toolbar_nonbreaking' : {'type' : 'Bool', 'default' : False},
            'toolbar_pagebreak' : {'type' : 'Bool', 'default' : False},
            'toolbar_print' : {'type' : 'Bool', 'default' : False},
            'toolbar_preview' : {'type' : 'Bool', 'default' : False},
            'toolbar_iespell' : {'type' : 'Bool', 'default' : False},
            'toolbar_removeformat' : {'type' : 'Bool', 'default' : False},
            'toolbar_cleanup' : {'type' : 'Bool', 'default' : False},
            'toolbar_visualaid' : {'type' : 'Bool', 'default' : False},
            'toolbar_visualchars' : {'type' : 'Bool', 'default' : False},
            'toolbar_code' : {'type' : 'Bool', 'default' : True},
            'toolbar_fullscreen' : {'type' : 'Bool', 'default' : True},
        },
        'resourcetypes' : {
            'link_using_uids' : {'type' : 'Bool', 'default' : False},
            'containsobjects' : {'type' : 'List', 'default' : 'ATFolder\nATBTreeFolder\nPlone Site'},
            'containsanchors' : {'type' : 'List', 'default' : 'ATEvent\nATNewsItem\nATDocument\nATRelativePathCriterion'},
            'linkable' : {'type' : 'List', 'default' : 'ATTopic\nATEvent\nATFile\nATFolder\nATImage\nATBTreeFolder\nATNewsItem\nATDocument'},
            'imageobjects' : {'type' : 'List', 'default' : 'ATImage'},
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

                if category[field]['type'] == 'Bool':
                    fieldnode.setAttribute('value', unicode(bool(fieldvalue)))
                elif category[field]['type'] == 'Text':

                    # Check for NoneType
                    if fieldvalue:
                        fieldnode.setAttribute('value', fieldvalue)
                    else:
                        fieldnode.setAttribute('value', '')
                elif category[field]['type'] == 'List':
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

        if self.environ.shouldPurge():
            self._purgeAttributes()

        for categorynode in node.childNodes:
            if categorynode.nodeName != '#text':
                for fieldnode in categorynode.childNodes:
                    if fieldnode.nodeName != '#text':
                        if self.attributes[categorynode.nodeName][fieldnode.nodeName]['type'] == 'Bool':
                            if fieldnode.hasAttribute('value'):
                                setattr(self.context, fieldnode.nodeName, self._convertToBoolean(fieldnode.getAttribute('value')))
                        elif self.attributes[categorynode.nodeName][fieldnode.nodeName]['type'] == 'Text':
                            if fieldnode.hasAttribute('value'):
                                setattr(self.context, fieldnode.nodeName, fieldnode.getAttribute('value'))
                        elif self.attributes[categorynode.nodeName][fieldnode.nodeName]['type'] == 'List':
                            field = getattr(self.context, fieldnode.nodeName)
                            items = field.split('\n')
                            for element in fieldnode.childNodes:
                                if element.nodeName != '#text':
                                    if element.getAttribute('value') not in items:
                                        items.append(element.getAttribute('value'))
                            string = '\n'.join(items)
                            setattr(self.context, fieldnode.nodeName, string.decode())
        # TODO : check if policy transform is needed, and how to get the s
        register_transform_policy(self.context, "text/x-html-safe", TINYMCE_OUTPUT_TRANSFORMATION)
        self._logger.info('TinyMCE Settings imported.')

    def _purgeAttributes(self):
        """Purge current attributes"""

        # Loop through categories
        for key in self.attributes.keys():
            category = self.attributes[key]

            # Loop through fields in category
            for field in category.keys():
                fieldvalue = getattr(self.context, field)

                fieldvalue = category[field]['default']

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
