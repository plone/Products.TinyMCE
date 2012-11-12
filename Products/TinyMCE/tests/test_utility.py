# -*- coding: utf-8 -*-
import os
import json

import transaction
from Products.CMFCore.utils import getToolByName
from plone.testing.z2 import Browser

from Products.TinyMCE.tests.base import IntegrationTestCase
from Products.TinyMCE.utility import form_adapter


class UtilityTestCase(IntegrationTestCase):
    """ Test utility of TinyMCE Plone integration """

    def setUp(self):
        super(UtilityTestCase, self).setUp()
        self.utility = form_adapter(self.portal)

    def test_tinymce_configuration(self):
        # Let's get the configuration of TinyMCE and see if it returns a json structure.
        self.assertTrue(self.utility.getConfiguration(self.portal))

        # Now let's change some variables and see it still works.
        self.utility.toolbar_cut = True
        self.utility.toolbar_copy = True
        self.utility.toolbar_paste = True
        self.utility.toolbar_pastetext = True
        self.utility.toolbar_pasteword = True
        self.utility.toolbar_undo = True
        self.utility.toolbar_redo = True
        self.utility.toolbar_search = True
        self.utility.toolbar_replace = True
        self.utility.toolbar_underline = True
        self.utility.toolbar_strikethrough = True
        self.utility.toolbar_sub = True
        self.utility.toolbar_sup = True
        self.utility.toolbar_forecolor = True
        self.utility.toolbar_backcolor = True
        self.utility.toolbar_media = True
        self.utility.toolbar_charmap = True
        self.utility.toolbar_hr = True
        self.utility.toolbar_advhr = True
        self.utility.toolbar_insertdate = True
        self.utility.toolbar_inserttime = True
        self.utility.toolbar_emotions = True
        self.utility.toolbar_nonbreaking = True
        self.utility.toolbar_pagebreak = True
        self.utility.toolbar_print = True
        self.utility.toolbar_preview = True
        self.utility.toolbar_spellchecker = True
        self.utility.toolbar_removeformat = True
        self.utility.toolbar_cleanup = True
        self.utility.toolbar_visualaid = True
        self.utility.toolbar_visualchars = True
        self.utility.toolbar_attribs = True
        self.utility.resizing = False

        # The result should at least contain the new buttons we added.
        self.assertRegexpMatches(self.utility.getConfiguration(self.portal), '\{.+attribs.+}')

        # Let's change some more settings.
        self.utility.toolbar_external = True
        self.utility.autoresize = True
        self.utility.editor_width = u'100'
        self.utility.editor_height = u'abc'
        self.utility.toolbar_width = u'abc'
        self.utility.contextmenu = False
        self.utility.content_css = u'test.css'
        self.utility.link_using_uids = True
        self.utility.allow_captioned_images = True
        self.utility.rooted = True

        props = getToolByName(self, 'portal_properties')
        livesearch = props.site_properties.getProperty('enable_livesearch', False)
        livesearch = False
        livesearch  # pep8

        # The result should contain the settings specified.
        self.assertRegexpMatches(self.utility.getConfiguration(self.portal), '\{.+external.+}')

        # Let's call the portal_factory of a document and make sure the configuration
        # doesn't contain the save button:
        browser = Browser(self.app)
        self.app.acl_users.userFolderAddUser('root', 'secret', ['Manager'], [])
        transaction.commit()
        browser.addHeader('Authorization', 'Basic root:secret')
        browser.open('http://nohost/plone/createObject?type_name=Document')
        self.assertNotIn("&quot;save&quot;:", browser.contents)

        # Do some more toolbar tests, specifically testing the spellchecker button.
        # First, we make sure that no spellchecker is loaded when the toolbar button is
        # hidden.
        self.utility.toolbar_spellchecker = False
        transaction.commit()
        browser.open('http://nohost/plone/createObject?type_name=Document')

        # AtD shouldn't be there:
        self.assertNotIn("&quot;AtD&quot;", browser.contents)

        # Neither should iespell:
        self.assertNotIn("&quot;iespell&quot;", browser.contents)

        # When we have browser as the checker, neither iespell nor AtD should load:
        self.utility.libraries_spellchecker_choice = u'browser'
        transaction.commit()
        browser.open('http://nohost/plone/createObject?type_name=Document')
        self.assertNotIn("&quot;iespell&quot;", browser.contents)
        self.assertNotIn("&quot;AtD&quot;", browser.contents)

    def test_tinymce_configurable_image_dimensions(self):
        # The image scale dimensions being provided to the image chooser should be
        # gathered from the chosen AT content type. Let's begin by creating an
        # AT image:
        id = self.portal.invokeFactory('News Item', id='test')
        self.assertEqual(repr(self.portal[id]), '<ATNewsItem at /plone/test>')

        # Now the values being provided through JSON should be gotten from the ATNewsItem
        # schema:
        primary_field = self.portal.test.schema['image']
        scales = self.utility.getImageScales(primary_field)
        self.assertEqual(scales,
            [{'size': [0, 0], 'title': 'Original', 'value': ''},
            {'size': [16, 16], 'title': 'Listing', 'value': '@@images/image/listing'},
            {'size': [32, 32], 'title': 'Icon', 'value': '@@images/image/icon'},
            {'size': [64, 64], 'title': 'Tile', 'value': '@@images/image/tile'},
            {'size': [128, 128], 'title': 'Thumb', 'value': '@@images/image/thumb'},
            {'size': [200, 200], 'title': 'Mini', 'value': '@@images/image/mini'},
            {'size': [400, 400], 'title': 'Preview', 'value': '@@images/image/preview'},
            {'size': [768, 768], 'title': 'Large', 'value': '@@images/image/large'}]
        )

        # If no primary field is given, we should get the scale dimensions from ATImage:
        scales = self.utility.getImageScales()
        self.assertEqual(scales,
            [{'size': [0, 0], 'title': 'Original', 'value': ''},
            {'size': [16, 16], 'title': 'Listing', 'value': '@@images/image/listing'},
            {'size': [32, 32], 'title': 'Icon', 'value': '@@images/image/icon'},
            {'size': [64, 64], 'title': 'Tile', 'value': '@@images/image/tile'},
            {'size': [128, 128], 'title': 'Thumb', 'value': '@@images/image/thumb'},
            {'size': [200, 200], 'title': 'Mini', 'value': '@@images/image/mini'},
            {'size': [400, 400], 'title': 'Preview', 'value': '@@images/image/preview'},
            {'size': [768, 768], 'title': 'Large', 'value': '@@images/image/large'}]
        )

        # We need to specify a context, if we want the dimension of the original image
        imgdata = open(os.path.join(os.path.dirname(__file__), 'sample.png'))
        self.portal[id].setImage(imgdata)

        scales = self.utility.getImageScales(context=self.portal[id])
        self.assertEqual(scales,
            [{'size': [52, 43], 'title': 'Original', 'value': ''},
            {'size': [16, 16], 'title': 'Listing', 'value': '@@images/image/listing'},
            {'size': [32, 32], 'title': 'Icon', 'value': '@@images/image/icon'},
            {'size': [64, 64], 'title': 'Tile', 'value': '@@images/image/tile'},
            {'size': [128, 128], 'title': 'Thumb', 'value': '@@images/image/thumb'},
            {'size': [200, 200], 'title': 'Mini', 'value': '@@images/image/mini'},
            {'size': [400, 400], 'title': 'Preview', 'value': '@@images/image/preview'},
            {'size': [768, 768], 'title': 'Large', 'value': '@@images/image/large'}]
        )

    def _get_config(self):
        return {
            'libraries_spellchecker_choice': 'browser',
             'customplugins': '',
             'contextmenu': False,
             'autoresize': False,
             'labels': {'label_paragraph': 'Paragraph',
                      'label_styles': u'Styles with an ü',
                      'label_plain_cell': 'Plain Cell',
                      'label_lists': 'Lists',
              },
             'styles': ['a|class|y', 'foo|bar|x'],
             'buttons': ['style', 'tablecontrol', 'forecolor', ] + ['a'] * 30,
             'toolbar_width': '440',
        }

    def test_getPlugins(self):
        self.assertTrue('table' in self.utility.getPlugins())
        self.assertTrue('contextmenu' in self.utility.getPlugins())
        self.assertFalse('autoresize' in self.utility.getPlugins())

        self.utility.contextmenu = False
        self.assertTrue('table' in self.utility.getPlugins())
        self.assertFalse('contextmenu' in self.utility.getPlugins())
        self.assertFalse('autoresize' in self.utility.getPlugins())

        self.utility.autoresize = True
        self.assertTrue('table' in self.utility.getPlugins())
        self.assertFalse('contextmenu' in self.utility.getPlugins())
        self.assertTrue('autoresize' in self.utility.getPlugins())

        self.utility.customplugins = u'plugin1\nplugin2|Title of P2'
        self.assertTrue('plugin1,plugin2' in self.utility.getPlugins())

    def test_getStyles(self):
        config = self._get_config()
        self.assertEqual(self.utility.getStyles(config['styles'],
                                                config['labels']),
            (u'[{ title: "Text", tag: "", className: "-", type: "Text" },'
             u'{ title: "Paragraph", tag: "p", className: " ", type: "Text" },'
             u'{ title: "a", tag: "class", className: "y", type: "Text" },'
             u'{ title: "foo", tag: "bar", className: "x", type: "Text" },'
             u'{ title: "Selection", tag: "", className: "-", type: "Selection" },'
             u'{ title: "Styles with an ü", tag: "", className: "", type: "Selection" },'
             u'{ title: "Tables", tag: "table", className: "-", type: "Tables" },'
             u'{ title: "Plain Cell", tag: "td", className: " ", type: "Tables" },'
             u'{ title: "Lists", tag: "ul", className: "-", type: "Lists" },'
             u'{ title: "Lists", tag: "ol", className: "-", type: "Lists" },'
             u'{ title: "Lists", tag: "dl", className: "-", type: "Lists" },'
             u'{ title: "Lists", tag: "dl", className: " ", type: "Lists" }]'))

    def test_getToolbars(self):
        toolbars = self.utility.getToolbars(self._get_config())
        self.assertEqual(toolbars, ['style,tablecontrol,forecolor,a,a,a,a,a,a,a,a,a,a', 'a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a', 'a', ''])

    def test_content_css_url(self):
        """https://dev.plone.org/ticket/12800"""

        configuration = self.utility.getConfiguration(self.portal)
        content_css_url = json.loads(configuration)['content_css']
        url = '%s/portal_tinymce/@@tinymce-getstyle' % self.portal.absolute_url()
        self.assertEqual(content_css_url,
                         url,
                         msg="content_css has wrong url, reported #12800")

    def test_config_document_base_url(self):
        portal = self.portal

        configuration = json.loads(self.utility.getConfiguration(portal))
        self.assertEqual(configuration['document_url'], 'http://nohost/plone')
        self.assertEqual(configuration['document_base_url'], 'http://nohost/plone/')

        # Check AT document after creation
        portal.invokeFactory(id='doc', type_name='Document')
        portal['doc'].unmarkCreationFlag()
        self.assertEqual(portal['doc'].checkCreationFlag(), False)
        configuration = json.loads(self.utility.getConfiguration(portal['doc']))
        self.assertEqual(configuration['document_url'], 'http://nohost/plone/doc')
        self.assertEqual(configuration['document_base_url'], 'http://nohost/plone/')

        # Check AT folder after creation
        portal.invokeFactory(id='folder', type_name='Folder')
        portal['folder'].unmarkCreationFlag()
        self.assertEqual(portal['folder'].checkCreationFlag(), False)
        configuration = json.loads(self.utility.getConfiguration(portal['folder']))
        self.assertEqual(configuration['document_url'], 'http://nohost/plone/folder')
        self.assertEqual(configuration['document_base_url'], 'http://nohost/plone/folder/')

        # Check AT doc within AT folder after creation
        portal['folder'].invokeFactory(id='doc', type_name='Document')
        portal['folder']['doc'].unmarkCreationFlag()
        self.assertEqual(portal['folder']['doc'].checkCreationFlag(), False)
        configuration = json.loads(self.utility.getConfiguration(portal['folder']['doc']))
        self.assertEqual(configuration['document_url'], 'http://nohost/plone/folder/doc')
        self.assertEqual(configuration['document_base_url'], 'http://nohost/plone/folder/')

    def test_config_document_base_url_during_creation(self):
        portal = self.portal

        # Browse to an add form and read the JSON from it
        browser = Browser(self.app)
        self.app.acl_users.userFolderAddUser('root', 'secret', ['Manager'], [])
        transaction.commit()
        browser.addHeader('Authorization', 'Basic root:secret')
        browser.open('http://nohost/plone/createObject?type_name=Document')
        configuration = self._parsePageConfiguration(browser)
        self.assertIn('http://nohost/plone/portal_factory/Document/document.', configuration['document_url'])
        self.assertEqual(configuration['document_base_url'], 'http://nohost/plone/')

        # Calling getConfiguration direcly on a not-yet-created document
        # breaks, and we fall back to the portal URL. This is possibly a bug.
        portal.invokeFactory(id='doc', type_name='Document')
        self.assertEqual(portal['doc'].checkCreationFlag(), True)
        configuration = json.loads(self.utility.getConfiguration(portal['doc']))
        self.assertEqual(configuration['document_url'], 'http://nohost/plone')
        self.assertEqual(configuration['document_base_url'], 'http://nohost/plone/')

    def _parsePageConfiguration(self, browser):
        """Find the TinyMCE config on the current page and parse it
        """
        for form in browser.mech_browser.forms():
            for control in form.controls:
                if 'data-mce-config' in getattr(control, 'attrs', {}):
                    return json.loads(control.attrs['data-mce-config'])
        raise ValueError('No control had data-mce-config attribute')
