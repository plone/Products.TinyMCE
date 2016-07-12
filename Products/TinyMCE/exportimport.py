from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase

from Products.CMFCore.utils import getToolByName


class TinyMCESettingsXMLAdapter(XMLAdapterBase):
    name = 'tinymce'
    _LOGGER_ID = 'portal_tinymce'

    attributes = {
        'layout': {
            'resizing': {'type': 'Bool', 'default': True},
            'autoresize': {'type': 'Bool', 'default': False},
            'editor_width': {'type': 'Text', 'default': u'100%'},
            'editor_height': {'type': 'Text', 'default': u'400'},
            'contextmenu': {'type': 'Bool', 'default': True},
            'content_css': {'type': 'Text', 'default': u''},
            'styles': {
                'type': 'List', 'default':
                u'Heading|h2|\n'
                u'Subheading|h3|\n'
                u'Literal|pre|\n'
                u'Discreet|span|discreet\n'
                u'Pull-quote|blockquote|pullquote\n'
                u'Call-out|p|callout\n'
                u'Highlight|span|visualHighlight\n'
                u'Odd row|tr|odd\n'
                u'Even row|tr|even\n'
                u'Heading cell|th|\n'
                u'Page break (print only)|div|pageBreak\n'
                u'Clear floats|div|visualClear\n'
            },
            'tablestyles': {
                'type': 'List', 'default':
                u'Subdued grid|plain\n'
                u'Invisible grid|invisible\n'
                u'Fancy listing|listing\n'
            },
            'tablerowstyles': {
                'type': 'List', 'default':
                u'Even|even\n'
                u'Odd|odd\n'
            },
        },
        'toolbar': {
            'toolbar_width': {'type': 'Text', 'default': u'440'},
            'toolbar_external': {'type': 'Bool', 'default': False},
            'toolbar_save': {'type': 'Bool', 'default': True},
            'toolbar_cut': {'type': 'Bool', 'default': False},
            'toolbar_copy': {'type': 'Bool', 'default': False},
            'toolbar_paste': {'type': 'Bool', 'default': False},
            'toolbar_pastetext': {'type': 'Bool', 'default': False},
            'toolbar_pasteword': {'type': 'Bool', 'default': False},
            'toolbar_undo': {'type': 'Bool', 'default': False},
            'toolbar_redo': {'type': 'Bool', 'default': False},
            'toolbar_search': {'type': 'Bool', 'default': False},
            'toolbar_replace': {'type': 'Bool', 'default': False},
            'toolbar_style': {'type': 'Bool', 'default': True},
            'toolbar_bold': {'type': 'Bool', 'default': True},
            'toolbar_italic': {'type': 'Bool', 'default': True},
            'toolbar_underline': {'type': 'Bool', 'default': False},
            'toolbar_strikethrough': {'type': 'Bool', 'default': False},
            'toolbar_sub': {'type': 'Bool', 'default': False},
            'toolbar_sup': {'type': 'Bool', 'default': False},
            'toolbar_forecolor': {'type': 'Bool', 'default': False},
            'toolbar_backcolor': {'type': 'Bool', 'default': False},
            'toolbar_justifyleft': {'type': 'Bool', 'default': True},
            'toolbar_justifycenter': {'type': 'Bool', 'default': True},
            'toolbar_justifyright': {'type': 'Bool', 'default': True},
            'toolbar_justifyfull': {'type': 'Bool', 'default': True},
            'toolbar_bullist': {'type': 'Bool', 'default': True},
            'toolbar_numlist': {'type': 'Bool', 'default': True},
            'toolbar_definitionlist': {'type': 'Bool', 'default': True},
            'toolbar_outdent': {'type': 'Bool', 'default': True},
            'toolbar_indent': {'type': 'Bool', 'default': True},
            'toolbar_tablecontrols': {'type': 'Bool', 'default': True},
            'toolbar_link': {'type': 'Bool', 'default': True},
            'toolbar_unlink': {'type': 'Bool', 'default': True},
            'toolbar_anchor': {'type': 'Bool', 'default': True},
            'toolbar_image': {'type': 'Bool', 'default': True},
            'toolbar_media': {'type': 'Bool', 'default': False},
            'toolbar_charmap': {'type': 'Bool', 'default': False},
            'toolbar_hr': {'type': 'Bool', 'default': False},
            'toolbar_advhr': {'type': 'Bool', 'default': False},
            'toolbar_insertdate': {'type': 'Bool', 'default': False},
            'toolbar_inserttime': {'type': 'Bool', 'default': False},
            'toolbar_emotions': {'type': 'Bool', 'default': False},
            'toolbar_nonbreaking': {'type': 'Bool', 'default': False},
            'toolbar_pagebreak': {'type': 'Bool', 'default': False},
            'toolbar_print': {'type': 'Bool', 'default': False},
            'toolbar_preview': {'type': 'Bool', 'default': False},
            'toolbar_spellchecker': {'type': 'Bool', 'default': False},
            'toolbar_removeformat': {'type': 'Bool', 'default': False},
            'toolbar_cleanup': {'type': 'Bool', 'default': False},
            'toolbar_visualaid': {'type': 'Bool', 'default': False},
            'toolbar_visualchars': {'type': 'Bool', 'default': False},
            'toolbar_attribs': {'type': 'Bool', 'default': False},
            'toolbar_code': {'type': 'Bool', 'default': True},
            'toolbar_fullscreen': {'type': 'Bool', 'default': True},
            'customtoolbarbuttons': {'type': 'List', 'default': u''},
        },
        'resourcetypes': {
            'link_using_uids': {'type': 'Bool', 'default': False},
            'allow_captioned_images': {'type': 'Bool', 'default': False},
            'containsobjects': {
                'type': 'List', 'default':
                u'Folder\n'
                u'Plone Site\n'
            },
            'containsanchors': {
                'type': 'List', 'default':
                u'ATRelativePathCriterion\n'
                u'Document\n'
                u'Event\n'
                u'News Item\n'
            },
            'linkable': {
                'type': 'List', 'default':
                u'Collection\n'
                u'Document\n'
                u'Event\n'
                u'File\n'
                u'Folder\n'
                u'Image\n'
                u'News Item\n'
            },
            'imageobjects': {'type': 'List', 'default': u'Image'},
            'plugins': {'type': 'Selection', 'default': []},
            'customplugins': {'type': 'List', 'default': u''},
            'entity_encoding': {'type': 'Text', 'default': u'raw'},
            'rooted': {'type': 'Bool', 'default': False},
        },
        'contentbrowser': {
            'anchor_selector': {'type': 'Text', 'default': u'h2,h3'},
            'link_shortcuts': {'type': 'Selection', 'default': []},
            'image_shortcuts': {'type': 'Selection', 'default': []},
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
                    if not fieldvalue:
                        fieldnode.setAttribute('value', '')
                    else:
                        for value in fieldvalue.split('\n'):
                            if value:
                                child = self._doc.createElement('element')
                                child.setAttribute('value', value)
                                fieldnode.appendChild(child)
                elif category[field]['type'] == 'Selection':
                    if not fieldvalue:
                        fieldnode.setAttribute('value', '')
                    else:
                        for value in fieldvalue:
                            if value:
                                child = self._doc.createElement('element')
                                child.setAttribute('value', value)
                                fieldnode.appendChild(child)
                categorynode.appendChild(fieldnode)
            object.appendChild(categorynode)
        return object

    def _importNode(self, node):
        """Import the object from the DOM node"""
        if self.environ.shouldPurge() or node.getAttribute("purge").lower() == 'true':
            self._purgeAttributes()

        for categorynode in node.childNodes:
            if categorynode.nodeName != '#text' and categorynode.nodeName != '#comment':
                for fieldnode in categorynode.childNodes:
                    if fieldnode.nodeName != '#text' and fieldnode.nodeName != '#comment':
                        if self.attributes[categorynode.nodeName][fieldnode.nodeName]['type'] == 'Bool':
                            if fieldnode.hasAttribute('value'):
                                setattr(self.context, fieldnode.nodeName, self._convertToBoolean(fieldnode.getAttribute('value')))
                        elif self.attributes[categorynode.nodeName][fieldnode.nodeName]['type'] == 'Text':
                            if fieldnode.hasAttribute('value'):
                                setattr(self.context, fieldnode.nodeName, fieldnode.getAttribute('value'))
                        elif self.attributes[categorynode.nodeName][fieldnode.nodeName]['type'] == 'List':
                            field = getattr(self.context, fieldnode.nodeName)
                            if field is None or fieldnode.getAttribute("purge").lower() == 'true':
                                items = {}
                            else:
                                items = dict.fromkeys(field.split('\n'))
                            for element in fieldnode.childNodes:
                                if element.nodeName != '#text' and element.nodeName != '#comment':
                                    if element.getAttribute('remove').lower() == 'true' and \
                                            element.getAttribute('value') in items:
                                        del(items[element.getAttribute('value')])
                                    elif element.getAttribute('remove').lower() != 'true' and \
                                            element.getAttribute('value') not in items:
                                        items[element.getAttribute('value')] = None
                            string = '\n'.join(sorted(items.keys()))

                            # Don't break on international characters or otherwise
                            # funky data -
                            if type(string) == str:
                                # On Plone 4.1 this should not be reached
                                # as string is unicode in any case
                                string = string.decode("utf-8", "ignore")

                            setattr(self.context, fieldnode.nodeName, string)
                        elif self.attributes[categorynode.nodeName][fieldnode.nodeName]['type'] == 'Selection':
                            field = getattr(self.context, fieldnode.nodeName)
                            if field is None or fieldnode.getAttribute("purge").lower() == 'true':
                                items = []
                            else:
                                items = field
                            for element in fieldnode.childNodes:
                                if element.nodeName != '#text' and element.nodeName != '#comment':
                                    remove = element.getAttribute('remove').lower() == 'true'
                                    value = element.getAttribute('value')
                                    if remove and value in items:
                                        items.remove(value)
                                    if not remove and value not in items:
                                        items.append(value)

                            for index, key in enumerate(items):
                                # Don't break on international characters or otherwise
                                # funky data -
                                if isinstance(key, str):
                                    # On Plone 4.1 this should not be reached
                                    # as string is unicode in any case
                                    items[index] = key.decode("utf-8", "ignore")

                            setattr(self.context, fieldnode.nodeName, items)

        self._logger.info('TinyMCE Settings imported.')

    def _purgeAttributes(self):
        """Purge current attributes"""

        # Loop through categories
        for key in self.attributes.keys():
            category = self.attributes[key]

            # Loop through fields in category
            for field in category.keys():
                setattr(self.context, field, category[field]['default'])


def importTinyMCESettings(context):
    """Import TinyMCE Settings"""
    site = context.getSite()
    tool = getToolByName(site, 'portal_tinymce', None)
    if tool is None:
        return

    importObjects(tool, '', context)


def exportTinyMCESettings(context):
    """Export TinyMCE Settings"""
    site = context.getSite()
    tool = getToolByName(site, 'portal_tinymce', None)
    if tool is None:
        return

    exportObjects(tool, '', context)
