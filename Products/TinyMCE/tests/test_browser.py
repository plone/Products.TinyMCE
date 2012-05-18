# -*- coding: utf-8 -*-
from Products.TinyMCE.tests.base import IntegrationTestCase
from Products.TinyMCE.tests.base import FunctionalTestCase

from Products.TinyMCE.browser.atanchors import ATAnchorView


class BrowserTestCase(FunctionalTestCase):

    def setUp(self):
        super(BrowserTestCase, self).setUp()
        self.image = self.portal.invokeFactory('Image', id='image')
        self.document = self.portal.invokeFactory('Document', id='document')

    def test_url(self):
        # We get the url by specifying the uid of the document.
        self.portal.REQUEST['uid'] = self.portal[self.document].UID()
        output = self.portal.restrictedTraverse('/plone/portal_tinymce/@@tinymce-getpathbyuid')()
        self.assertEqual(output, 'http://nohost/plone/document')

        # If we don't specify the uid we get an empty string.
        self.portal.REQUEST['uid'] = None
        output = self.portal.restrictedTraverse('/plone/portal_tinymce/@@tinymce-getpathbyuid')()
        self.assertEqual(output, '')

        self.portal.REQUEST['uid'] = 'asd'
        # If we specify a non existing uid we should get an empty string.
        output = self.portal.restrictedTraverse('/plone/portal_tinymce/@@tinymce-getpathbyuid')()
        self.assertEqual(output, '')

    def test_getstyle(self):
        # This browserview will return all the stylesheets used. Let's call the
        # browser view.
        output = self.portal.restrictedTraverse('/plone/portal_tinymce/@@tinymce-getstyle')()
        self.assertRegexpMatches(output, '<!-- @import url\(.+portal_css.+\); -->')

    def test_controlpanel(self):
        # Open the TinyMCE control panel.
        self.portal.restrictedTraverse('/plone/portal_tinymce/@@tinymce-controlpanel')()

    def test_jsonlinkablefolderlisting(self):
        # We can call the linkable folder listing browserview on the site root to get a
        # list of linkable items.
        output = self.portal.restrictedTraverse('/plone/@@tinymce-jsonlinkablefolderlisting')(False, 'http://nohost/plone/')
        self.assertIn('"id": "document"', output)

    def test_jsonimagefolderlisting(self):
        # Now we can get a listing of the images and check if our image is there.e/'})
        output = self.portal.restrictedTraverse('/plone/@@tinymce-jsonimagefolderlisting')(False, 'http://nohost/plone/')
        self.assertIn('"id": "image"', output)

    def test_jsonlinkablesearch(self):
        # If we want to search for a linkable item we can call the json linkable search
        # browser view and specify a searchtext. Let's find our document.
        output = self.portal.restrictedTraverse('/plone/@@tinymce-jsonlinkablesearch')('Document')
        self.assertIn('"id": "document"', output)

    def test_jsonimagesearch(self):
        # The images have a similar search method. Let's find our image.
        output = self.portal.restrictedTraverse('/plone/@@tinymce-jsonimagesearch')('Image')
        self.assertIn('"id": "image"', output)

    def test_jsondetails(self):
        # When we call the json details view on a document we will get the details of
        # the specific item.
        output = self.portal.restrictedTraverse('/plone/document/@@tinymce-jsondetails')()
        self.assertIn('document', output)

    def test_save(self):
        # Let's call the save method to store some content in the document we created.
        self.portal.restrictedTraverse('/plone/document/@@tinymce-save')('test', 'text')
        self.assertEqual(self.portal[self.document].getText(), 'test')

    def test_configuration(self):
        document_jsonconfig_url = '/plone/document/@@tinymce-jsonconfiguration'
        output = self.portal.restrictedTraverse(document_jsonconfig_url)('text')
        self.assertIn('buttons', output)

        # If we configure directivity to 'auto', the directivity is set depending
        # on the content language.
        doc = self.portal[self.document]
        self.assertEqual(doc.Language(), 'en')
        output = self.portal.restrictedTraverse(document_jsonconfig_url)('text')
        self.assertIn('"directionality": "ltr"', output)
        doc.setLanguage('ar')
        output = self.portal.restrictedTraverse(document_jsonconfig_url)('text')
        self.assertIn('"directionality": "rtl"', output)

        # TODO: upload


class AnchorTestCase(IntegrationTestCase):

    def setUp(self):
        super(AnchorTestCase, self).setUp()
        self.document = self.portal.invokeFactory('Document', id='document')

    def test_brokenxml(self):
        context = self.portal['document']
        context.setText('''<p><div></p>''')
        view = ATAnchorView(context, self.app.REQUEST)
        self.assertEqual(view.listAnchorNames(), [])

    def test_primaryfield(self):
        context = self.portal['document']
        context.setText('''<p><a name="foobar"></a></p>''')
        view = ATAnchorView(context, self.app.REQUEST)
        self.assertEqual(view.listAnchorNames(), ['foobar'])

    def test_notprimaryfield(self):
        context = self.portal['document']
        context.setLocation('''<p><a name="foobar"></a></p>''')
        context.setText('')
        view = ATAnchorView(context, self.app.REQUEST)
        self.assertEqual(view.listAnchorNames(), [])
        self.assertEqual(view.listAnchorNames('location'), ['foobar'])
