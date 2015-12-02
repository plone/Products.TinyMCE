"""
This functionality is added to plone content types using adapters.
"""
import os
from cgi import FieldStorage
from tempfile import TemporaryFile

try:
    import simplejson as json
    json  # Pyflakes
except ImportError:
    import json

from Products.CMFCore.utils import getToolByName
from ZPublisher.HTTPRequest import FileUpload

from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails
from Products.TinyMCE.adapters.interfaces.Save import ISave
from Products.TinyMCE.adapters.interfaces.JSONSearch import IJSONSearch
from Products.TinyMCE.adapters.interfaces.JSONFolderListing import IJSONFolderListing
from Products.TinyMCE.adapters.interfaces.Upload import IUpload
from Products.TinyMCE.tests.base import FunctionalTestCase

from plone.app.textfield.value import RichTextValue


class AdaptersTestCase(FunctionalTestCase):

    def setUp(self):
        super(AdaptersTestCase, self).setUp()

        self.utility = getToolByName(self.portal, 'portal_tinymce')
        self.document = self.portal.invokeFactory('Document', id='document')
        folder = self.portal.invokeFactory('Folder', id='folder')
        self.folder_object = self.portal[folder]

    def test_json_details_document(self):
        # This class is used to get detail from a certain object. Let's create a Document.
        self.assertEqual(repr(self.portal[self.document]), '<Document at /plone/document>')

        # The basic details should return the following.
        obj = IJSONDetails(self.portal[self.document])
        details = json.loads(obj.getDetails())
        should = {"url": "http://nohost/plone/document", "thumb": "", "description": "", "anchors": [], "title": "document"}
        for key, val in should.iteritems():
            self.assertEqual(details[key], val)

        # Let's set some more details like description and body text.
        self.portal[self.document].description = 'Test'
        self.portal[self.document].text = RichTextValue(
            u'<p><a name="anchor">anchor</a></p>',
            'text/plain',
            'text/html'
        )

        # The details will now contain a bit more info.
        details = json.loads(obj.getDetails())
        should = {"url": "http://nohost/plone/document", "thumb": "", "description": "Test", "anchors": ["anchor"], "title": "document"}
        for key, val in should.iteritems():
            self.assertEqual(details[key], val)

    def test_json_details_image(self):
        # We can also get the details of an image object.
        image = self.portal.invokeFactory('Image', id='image')
        self.assertEqual(repr(self.portal[image]), '<Image at /plone/image>')

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
        listing = object.getListing(
                        filter_portal_types=linkableportal_types,
                        rooted=False,
                        document_base_url='http://nohost/plone',
                        upload_type='File')
        self.assertRegexpMatches(listing,
            '\{"parent_url": "", "path": \[.+],.+"items": \[.+]}')
        # no icon for regular contenttypes
        self.assertRegexpMatches(listing, '"icon": null')
        # This is easier to check more rigorously by turning the json
        # back to a Python dict.
        items = json.loads(listing)['items']
        folder_item = [item for item in items if item[u'id'] == u'folder'][0]
        doc_item = [item for item in items if item[u'id'] == u'document'][0]
        self.assertEqual(folder_item[u'icon'], None)
        self.assertEqual(doc_item[u'icon'], None)

        # Let's create some more content to get breadcrumbs.
        document = self.folder_object.invokeFactory('Document', id='document')

        # When we call the getListing method on the document we should get the listing of
        # its parent.
        obj = IJSONFolderListing(self.folder_object.get(document))
        listing = obj.getListing(
                        filter_portal_types=[],
                        rooted='False',
                        document_base_url='http://nohost/plone/folder')
        self.assertRegexpMatches(listing,
                                 '\{"parent_url": "http://nohost/plone".+}')

        # We can also select rooted so we don't get all the breadcrumbs.
        listing = obj.getListing(
                        filter_portal_types=[],
                        rooted='True',
                        document_base_url='http://nohost/plone/folder')
        self.assertRegexpMatches(listing,
            '\{.*"path": \[{"url": "http://nohost/plone/folder".*}')

    def test_json_folder_listing_icon(self):
        self.portal.invokeFactory('File', id='somefile.bin')
        linkable_portal_types = self.utility.linkable.split('\n')
        linkable_portal_types.extend(self.utility.containsobjects.split('\n'))

        obj = IJSONFolderListing(self.portal)
        listing = obj.getListing(
                        filter_portal_types=linkable_portal_types,
                        rooted=False,
                        document_base_url='http://nohost/plone',
                        upload_type='File')
        self.assertRegexpMatches(listing,
            r'"icon": "<img width=\\"16\\" height=\\"16\\" src=\\"http://nohost/plone/application.png\\" alt=\\"File.*?\\" />"')
        # This is easier to check more rigorously by turning the json
        # back to a Python dict.
        items = json.loads(listing)['items']
        file_item = [item for item in items if item[u'id'] == u'somefile.bin'][0]
        self.assertEqual(file_item[u'icon'],
                         '<img width="16" height="16" src="http://nohost/plone/application.png" alt="File Octet Stream" />')

    def test_json_search(self):
        # Create an Event
        self.portal.invokeFactory('Event', id='events', title='Events')

        # The json search is used the look for content types within the self.portal. Let's see
        # if we can find some items containing the searchterm 'Events'
        linkable_portal_types = self.utility.linkable.split('\n')
        linkable_portal_types.extend(self.utility.containsobjects.split('\n'))

        obj = IJSONSearch(self.portal)
        results = obj.getSearchResults(filter_portal_types=linkable_portal_types,
                                         searchtext='Events')
        self.assertRegexpMatches(results,
            '\{.*"title": "Events", "url": "http://nohost/plone/events".*}')
        # icons for contenttypes are included by sprite
        self.assertRegexpMatches(results, '"id": "events", "icon": null}')

    def test_json_search_icon(self):
        self.portal.invokeFactory('File', id='somefile.bin', title='Somefile')
        linkable_portal_types = self.utility.linkable.split('\n')
        linkable_portal_types.extend(self.utility.containsobjects.split('\n'))

        obj = IJSONSearch(self.portal)
        results = obj.getSearchResults(filter_portal_types=linkable_portal_types,
                                         searchtext='somefile')
        self.assertRegexpMatches(results,
            r'"id": "somefile.bin", "icon": "<img width=\\"16\\" height=\\"16\\" src=\\"http://nohost/plone/application.png\\" alt=\\"File.*?\\" />"')

    def test_json_search_wildcard_whitespace(self):
        self.portal.invokeFactory('File', id='somefile bin', title='Somefile bin')
        linkable_portal_types = self.utility.linkable.split('\n')
        linkable_portal_types.extend(self.utility.containsobjects.split('\n'))

        obj = IJSONSearch(self.portal)
        results = obj.getSearchResults(
            filter_portal_types=linkable_portal_types,
            searchtext='somefile bi'
        )
        self.assertRegexpMatches(results,
            r'"id": "somefile bin", "icon": "<img width=\\"16\\" height=\\"16\\" src=\\"http://nohost/plone/application.png\\" alt=\\"File.*?\\" />"')

    def test_json_save(self):
        # This class is used to save a document using json. Let's try and set some value.
        document = self.folder_object.invokeFactory('Document', id='document')
        obj = ISave(self.folder_object[document])
        obj.save(fieldname='text', text='<p>test</p>')

        # The document should now contain our new text.
        self.assertEqual(self.folder_object[self.document].getText(), '<p>test</p>')

    def _prepare_file(self, filename='test.bin', type_='text/plain'):
        fp = TemporaryFile('w+b')
        fp.write('\x00' + 'x' * (1 << 19))
        fp.seek(0)
        env = {'REQUEST_METHOD': 'POST'}
        headers = {'Content-Type': type_,
                   'content-length': 1 << 19,
                   'content-disposition': 'attachment; filename=%s' % filename}
        fs = FieldStorage(fp=fp, environ=env, headers=headers)
        fu = FileUpload(fs)
        fu.read = fp.read
        fu.seek = fp.seek
        fu.tell = fp.tell
        return fu

    def test_json_upload_not_allowed(self):
        self.portal.REQUEST['uploadfile'] = self._prepare_file()
        self.portal.REQUEST['uploadtitle'] = 'foobar'
        self.portal.REQUEST['uploaddescription'] = 'foo'

        obj = IUpload(self.folder_object)
        msg = obj.upload()

        self.assertTrue('resolveuid/' in msg)

    def test_json_upload_image(self):
        self.portal.REQUEST['uploadfile'] = self._prepare_file('common_work.jpeg', type_='image/jpeg')
        self.portal.REQUEST['uploadtitle'] = 'foobar'
        self.portal.REQUEST['uploaddescription'] = 'foo'

        obj = IUpload(self.folder_object)
        msg = obj.upload()
        self.assertTrue('resolveuid/' in msg)
