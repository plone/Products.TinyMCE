# -*- coding: utf-8 -*-

from Products.TinyMCE.browser.compressor import TinyMCECompressorView
from Products.TinyMCE.tests.base import IntegrationTestCase


class ViewTestCase(IntegrationTestCase):

    def test_compressorview(self):
        view = TinyMCECompressorView(self.portal, self.portal.REQUEST)
        setattr(view, '__name__', 'tiny_mce_gzip.js')
        self.assertTrue(view().startswith(
            "jQuery(function($){"))
