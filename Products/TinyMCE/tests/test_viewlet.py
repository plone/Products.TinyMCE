"""
This functionality is added to plone content types using adapters.
"""
import os

try:
    import simplejson as json
    json  # Pyflakes
except ImportError:
    import json

import unittest2 as unittest

from zope.component import getUtility, createObject, getMultiAdapter

from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails
from Products.TinyMCE.adapters.interfaces.Save import ISave
from Products.TinyMCE.adapters.interfaces.JSONSearch import IJSONSearch
from Products.TinyMCE.adapters.interfaces.JSONFolderListing import IJSONFolderListing
from Products.TinyMCE.browser.browser import ConfigurationViewlet
from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.tests.base import FunctionalTestCase
from Products.TinyMCE.tests.base import HAS_DX, HAS_AT

if HAS_DX:
    from plone.dexterity.interfaces import IDexterityFTI

from Products.Five import BrowserView
class DummyAddView(BrowserView):

    @property
    def ti(self):
        class DummyTi(object):
            def getId(self):
                return "tinymce_test"
        return DummyTi()

class ConfigurationViewletTestCase(FunctionalTestCase):
    """ Test schema abstraction adapter """

    def makeone(self, context=None, request=None, view=None):
        if context is None:
            context = self.portal
        if request is None:
            request = self.app.REQUEST
        if view is None:
            plone_view = getMultiAdapter((context, request), name="plone")
        return ConfigurationViewlet(context, request, view)

    @unittest.skipUnless(HAS_AT,
            'Archetypes is not installed. Skipping AT schema adapter test.')
    def test_atedit(self):
        self.portal.invokeFactory('Document', id='document')
        document = self.portal['document']
        viewlet = self.makeone(document)
        self.assertFalse(viewlet.suffix)
        self.assertTrue(viewlet.show())
        self.assertEqual(viewlet.suffix, '?p=&f=text')

    @unittest.skipUnless(HAS_DX,
            'Dexterity is not installed. Skipping DX schema adapter test.')
    def test_dxedit(self):
        fti = getUtility(IDexterityFTI, name="tinymce_test")
        content = createObject(fti.factory)
        content = content.__of__(self.portal)
        viewlet = self.makeone(content)
        self.assertFalse(viewlet.suffix)
        self.assertTrue(viewlet.show())
        self.assertEqual(viewlet.suffix,
                '?p=form%5C%5C.widgets%5C%5C.&f=text&f=suffix')

    @unittest.skipUnless(HAS_DX,
            'Dexterity is not installed. Skipping DX schema adapter test.')
    def test_dxadd(self):
        view = DummyAddView(self.portal, self.app.REQUEST)
        viewlet = self.makeone(view=view)
        self.assertFalse(viewlet.suffix)
        self.assertTrue(viewlet.show())
        self.assertEqual(viewlet.suffix,
                '?p=form%5C%5C.widgets%5C%5C.&f=text&f=suffix')

    def test_portlet(self):
        from plone.portlet.static.static import EditForm
        view = EditForm(self.portal, self.app.REQUEST)
        viewlet = self.makeone(view=view)
        self.assertFalse(viewlet.suffix)
        self.assertTrue(viewlet.show())
        self.assertEqual(viewlet.suffix, '?p=form%5C%5C.&f=text')
