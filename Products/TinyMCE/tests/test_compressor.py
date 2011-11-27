# -*- coding: utf-8 -*-

from Products.TinyMCE.browser.compressor import TinyMCECompressorView
from Products.TinyMCE.tests.base import IntegrationTestCase


class ViewTestCase(IntegrationTestCase):

    def setUp(self):
        super(ViewTestCase, self).setUp()
        self.portal.invokeFactory('Folder', 'foobar')

    def test_compressorview_basic(self):
        view = TinyMCECompressorView(self.portal.foobar, self.portal.REQUEST)
        self.assertTrue(view().startswith(
            "jQuery(function($){"))

    def test_compressorview_customplugins(self):
        self.portal.portal_tinymce.customplugins = "plonebrowser,plonelink|"
        view = TinyMCECompressorView(self.portal.foobar, self.portal.REQUEST)
        self.assertIn('plonelink', view())

    def test_compressorview_dexterity(self):
        pass  # TODO
