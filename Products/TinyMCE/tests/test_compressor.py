# -*- coding: utf-8 -*-
import unittest

from Products.TinyMCE.browser.compressor import TinyMCECompressorView
from Products.TinyMCE.tests.base import IntegrationTestCase


class UtilTestCase(unittest.TestCase):

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

    def test_getplugins(self):
        config = self._get_config()
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
        TinyMCECompressorView.getstyles(self._get_config())
        # XXX

    def test_getlabels(self):
        self.assertEqual(TinyMCECompressorView.getlabels(self._get_config()),
                         ("{'label_paragraph': 'Paragraph', "
                          "'label_styles': 'Styles with an \\xc3\\xbc', "
                          "'label_plain_cell': 'Plain Cell', "
                          "'label_lists': 'Lists'}"))

    def test_gettoolbars(self):
        toolbars = TinyMCECompressorView.gettoolbars(self._get_config())
        self.assertEqual(toolbars, ['style,tablecontrol,forecolor,a,a,a,a,a,a,a,a,a,a', 'a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a', 'a', ''])


class ViewTestCase(IntegrationTestCase):

    def test_compressorview(self):
        view = TinyMCECompressorView(self.portal, self.portal.REQUEST)
        setattr(view, '__name__', 'tiny_mce_gzip')
        self.assertTrue(view().startswith(
            "jQuery(function(){jQuery('textarea.mce_editable').tinymce("))
