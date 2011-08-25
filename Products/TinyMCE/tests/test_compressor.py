#from Products.TinyMCE.tests.base import BaseTestCase
import unittest

from Products.TinyMCE.browser.compressor import (
    split_commas, getplugins, getstyles)

class UtilTestCase(unittest.TestCase):

    def test_splitcommas(self):
        self.assertEqual(split_commas(''), [])
        self.assertEqual(split_commas('a,b,c'), ['a', 'b', 'c'])

    def test_getplugins(self):
        config = {'libraries_spellchecker_choice': 'browser',
                  'customplugins':'',
                  'contextmenu':False,
                  'autoresize':False}
        self.assertTrue('table' in getplugins(config))
        self.assertFalse('contextmenu' in getplugins(config))
        self.assertFalse('autoresize' in getplugins(config))

        config['contextmenu'] = True
        self.assertTrue('table' in getplugins(config))
        self.assertTrue('contextmenu' in getplugins(config))
        self.assertFalse('autoresize' in getplugins(config))

        config['contextmenu'] = False
        config['autoresize'] = True
        self.assertTrue('table' in getplugins(config))
        self.assertFalse('contextmenu' in getplugins(config))
        self.assertTrue('autoresize' in getplugins(config))

        self.assertFalse('foobar' in getplugins(config))
        config['libraries_spellchecker_choice'] = 'foobar'
        self.assertTrue('foobar' in getplugins(config))

    def test_getstyles(self):
        config = {'labels': {'label_paragraph': 'Paragraph',
                           'label_styles': 'Styles',
                           'label_plain_cell': 'Plain Cell',
                           'label_lists': 'Lists',},
                  'styles': ['a|class|y', 'foo|bar|x'],
                          }
        getstyles(config)


