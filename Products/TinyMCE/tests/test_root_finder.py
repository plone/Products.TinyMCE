from plone.app.layout.navigation.interfaces import INavigationRoot

from Products.CMFCore.utils import getToolByName

from Products.TinyMCE.adapters.interfaces.RootFinder import IRootFinder
from Products.TinyMCE.tests.base import FunctionalTestCase

from zope.interface import alsoProvides


class RootFinderNavRootTest(FunctionalTestCase):

    def setUp(self):
        super(RootFinderNavRootTest, self).setUp()

        self.utility = getToolByName(self.portal, 'portal_tinymce')
        self.utility.use_plone_site_as_root = False

        self.portal.invokeFactory('Folder', id='folder')
        self.folder = self.portal['folder']
        alsoProvides(self.folder, INavigationRoot)
        self.folder.invokeFactory('Document', id='document')        
        self.doc_in_nav_root = self.folder['document']
        self.portal.invokeFactory('Document', id='document')        
        self.doc_in_portal = self.portal['document']

    def test_child_in_nav_root(self):
        root_finder = IRootFinder(self.doc_in_nav_root)
        self.assertFalse(root_finder.is_root_object())
        self.assertEqual(root_finder.get_root_object(), self.folder)
        self.assertEqual(
                root_finder.get_root_url(), 'http://nohost/plone/folder')
        
    def test_nav_root(self):
        root_finder = IRootFinder(self.folder)
        self.assertTrue(root_finder.is_root_object())
        self.assertEqual(root_finder.get_root_object(), self.folder)
        self.assertEqual(
                root_finder.get_root_url(), 'http://nohost/plone/folder')
        
    def test_portal(self):
        root_finder = IRootFinder(self.portal)
        self.assertTrue(root_finder.is_root_object())
        self.assertEqual(root_finder.get_root_object(), self.portal)
        self.assertEqual(root_finder.get_root_url(), 'http://nohost/plone')
        
    def test_child_in_portal(self):
        root_finder = IRootFinder(self.doc_in_portal)
        self.assertFalse(root_finder.is_root_object())
        self.assertEqual(root_finder.get_root_object(), self.portal)
        self.assertEqual(root_finder.get_root_url(), 'http://nohost/plone')

        
class RootFinderSiteRootTest(FunctionalTestCase):

    def setUp(self):
        super(RootFinderSiteRootTest, self).setUp()

        self.utility = getToolByName(self.portal, 'portal_tinymce')
        self.utility.use_plone_site_as_root = True

        self.portal.invokeFactory('Folder', id='folder')
        self.folder = self.portal['folder']
        alsoProvides(self.folder, INavigationRoot)
        self.folder.invokeFactory('Document', id='document')        
        self.doc_in_nav_root = self.folder['document']
        self.portal.invokeFactory('Document', id='document')        
        self.doc_in_portal = self.portal['document']

    def test_child_in_nav_root(self):
        root_finder = IRootFinder(self.doc_in_nav_root)
        self.assertFalse(root_finder.is_root_object())
        self.assertEqual(root_finder.get_root_object(), self.portal)
        self.assertEqual(root_finder.get_root_url(), 'http://nohost/plone')
        
    def test_nav_root(self):
        root_finder = IRootFinder(self.folder)
        self.assertFalse(root_finder.is_root_object())
        self.assertEqual(root_finder.get_root_object(), self.portal)
        self.assertEqual(root_finder.get_root_url(), 'http://nohost/plone')
        
    def test_portal(self):
        root_finder = IRootFinder(self.portal)
        self.assertTrue(root_finder.is_root_object())
        self.assertEqual(root_finder.get_root_object(), self.portal)
        self.assertEqual(root_finder.get_root_url(), 'http://nohost/plone')
        
    def test_child_in_portal(self):
        root_finder = IRootFinder(self.doc_in_portal)
        self.assertFalse(root_finder.is_root_object())
        self.assertEqual(root_finder.get_root_object(), self.portal)
        self.assertEqual(root_finder.get_root_url(), 'http://nohost/plone')
