# -*- coding: utf-8 -*-
import unittest

from Products.TinyMCE.browser.compressor import TinyMCECompressorView
from Products.TinyMCE.tests.base import IntegrationTestCase


class UtilTestCase(unittest.TestCase):

    def test_getplugins(self):
        config = {'libraries_spellchecker_choice': 'browser',
                  'customplugins': '',
                  'contextmenu': False,
                  'autoresize': False}
        self.assertTrue('table' in TinyMCECompressorView.getplugins(config))
        self.assertFalse('contextmenu' in TinyMCECompressorView.getplugins(config))
        self.assertFalse('autoresize' in TinyMCECompressorView.getplugins(config))

        config['contextmenu'] = True
        self.assertTrue('table' in TinyMCECompressorView.getplugins(config))
        self.assertTrue('contextmenu' in TinyMCECompressorView.getplugins(config))
        self.assertFalse('autoresize' in TinyMCECompressorView.getplugins(config))

        config['contextmenu'] = False
        config['autoresize'] = True
        self.assertTrue('table' in TinyMCECompressorView.getplugins(config))
        self.assertFalse('contextmenu' in TinyMCECompressorView.getplugins(config))
        self.assertTrue('autoresize' in TinyMCECompressorView.getplugins(config))

        self.assertFalse('foobar' in TinyMCECompressorView.getplugins(config))
        config['libraries_spellchecker_choice'] = 'foobar'
        self.assertTrue('foobar' in TinyMCECompressorView.getplugins(config))

        config['customplugins'] = ['plugin1', 'plugin2|Title of P2']
        self.assertTrue('plugin1,plugin2' in TinyMCECompressorView.getplugins(config))

    def test_getstyles(self):
        config = {'labels': {'label_paragraph': 'Paragraph',
                           'label_styles': 'Styles',
                           'label_plain_cell': 'Plain Cell',
                           'label_lists': 'Lists',
                           },
                  'styles': ['a|class|y', 'foo|bar|x'],
        }
        # XXX
        print TinyMCECompressorView.getstyles(config)

    def test_getlabels(self):
        config = {'labels': {'label_paragraph': 'Paragraph',
                           'label_styles': u'Styles with an ü',
                           'label_plain_cell': 'Plain Cell',
                           'label_lists': 'Lists',
                           },
        }
        self.assertEqual(TinyMCECompressorView.getlabels(config),
                         ("{'label_paragraph': 'Paragraph', "
                          "'label_styles': 'Styles with an \\xc3\\xbc', "
                          "'label_plain_cell': 'Plain Cell', "
                          "'label_lists': 'Lists'}"))


class ViewTestCase(IntegrationTestCase):

    def test_compressorview(self):
        context = self.portal
        request = self.portal.REQUEST
        view = TinyMCECompressorView(context, request)
        setattr(view, '__name__', 'tiny_mce_gzip')
        response = view()
        self.assertTrue(response.startswith(
            "jQuery(function(){jQuery('textarea.mce_editable').tinymce("))
