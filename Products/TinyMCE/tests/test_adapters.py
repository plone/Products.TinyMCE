"""
This functionality is added to plone content types using adapters.
"""
import os

try:
    import simplejson as json
    json  # Pyflakes
except ImportError:
    import json

from zope.component import getUtility

from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails
from Products.TinyMCE.adapters.interfaces.Save import ISave
from Products.TinyMCE.adapters.interfaces.JSONSearch import IJSONSearch
from Products.TinyMCE.adapters.interfaces.JSONFolderListing import IJSONFolderListing
from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.tests.base import FunctionalTestCase


class AdaptersTestCase(FunctionalTestCase):

    def setUp(self):
        super(AdaptersTestCase, self).setUp()
        self.utility = getUtility(ITinyMCE)
        folder = self.portal.invokeFactory('Folder', id='folder')
        self.document = self.portal.invokeFactory('Document', id='document')
        self.folder_object = self.portal[folder]

    def test_json_details_document(self):
        # This class is used to get detail from a certain object. Let's create a Document.
        self.assertEqual(repr(self.portal[self.document]), '<ATDocument at /plone/document>')

        # The basic details should return the following.
        obj = IJSONDetails(self.portal[self.document])
	details = json.loads(obj.getDetails())
        should = {"url": "http://nohost/plone/document", "thumb": "", "description": "", "anchors": [], "title": "document"}
	for key, val in should.iteritems():
            self.assertEqual(details[key], val)


        # Let's set some more details like description and body text.
        self.portal[self.document].setDescription('Test')
        self.portal[self.document].setText(u'<p><a name="anchor">anchor</a></p>', mimetype='text/html')

        # The details will now contain a bit more info.
	details = json.loads(obj.getDetails())
        should = {"url": "http://nohost/plone/document", "thumb": "", "description": "Test", "anchors": ["anchor"], "title": "document"}
	for key, val in should.iteritems():
            self.assertEqual(details[key], val)

    def test_json_details_image(self):
        # We can also get the details of an image object.
        image = self.portal.invokeFactory('Image', id='image')
        self.assertEqual(repr(self.portal[image]), '<ATImage at /plone/image>')

        imgdata = open(os.path.join(os.path.dirname(__file__), 'sample.png'))
        self.portal[image].setImage(imgdata)

        # The details will now also include the thumbnail url and the imagescales.
        obj = IJSONDetails(self.portal[image])
        self.assertRegexpMatches(obj.getDetails(),
                                 r'"scales": \[\{"size": \[52, 43\], "value": "", "title": "Original"\}.+\], ')
        self.assertRegexpMatches(obj.getDetails(),
                                 r'"thumb": "http://nohost/plone/resolveuid/.*/@@images/image/thumb".+')

    def test_json_folder_listing(self):
        # The folder listing is used in the link and image drawers to show the contents
        # of a folder. Let's see what items our current siteroot has.

        linkableportal_types = self.utility.linkable.split('\n')
        linkableportal_types.extend(self.utility.containsobjects.split('\n'))
        object = IJSONFolderListing(self.portal)
        self.assertRegexpMatches(object.getListing(
            filter_portal_types=linkableportal_types,
            rooted=False,
            document_base_url='http://nohost/plone',
            upload_type='File',
        ), '\{"parent_url": "", "path": \[.+],.+"items": \[.+]}')

        # Let's create some more content to get breadcrumbs.
        document = self.folder_object.invokeFactory('Document', id='document')

        # When we call the getListing method on the document we should get the listing of
        # its parent.
        obj = IJSONFolderListing(self.folder_object.get(document))
        self.assertRegexpMatches(obj.getListing(
            filter_portal_types=[],
            rooted='False',
            document_base_url='http://nohost/plone/folder',
        ), '\{"parent_url": "http://nohost/plone".+}')

        # We can also select rooted so we don't get all the breadcrumbs.
        self.assertRegexpMatches(obj.getListing(
            filter_portal_types=[],
            rooted='True',
            document_base_url='http://nohost/plone/folder',
        ), '\{.*"path": \[{"url": "http://nohost/plone/folder".*}')

    def test_json_search(self):
        # Create an Event
        self.portal.invokeFactory('Event', id='events', title='Events')

        # The json search is used the look for content types within the self.portal. Let's see
        # if we can find some items containing the searchterm 'Events'
        linkable_portal_types = self.utility.linkable.split('\n')
        linkable_portal_types.extend(self.utility.containsobjects.split('\n'))

        obj = IJSONSearch(self.portal)
        self.assertRegexpMatches(
            obj.getSearchResults(filter_portal_types=linkable_portal_types,
            searchtext='Events',
        ), '\{.*"title": "Events", "url": "http://nohost/plone/events".*}')

    def test_json_save(self):
        # This class is used to save a document using json. Let's try and set some value.
        document = self.folder_object.invokeFactory('Document', id='document')
        obj = ISave(self.folder_object[document])
        obj.save(fieldname='text', text='<p>test</p>')

        # The document should now contain our new text.
        self.assertEqual(self.folder_object[self.document].getText(), '<p>test</p>')
