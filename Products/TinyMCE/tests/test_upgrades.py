from zope.component import getUtility
from Products.CMFCore.utils import getToolByName

from Products.TinyMCE.upgrades import upgrade_10_to_11
from Products.TinyMCE.upgrades import upgrade_12_to_13
from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.tests.base import FunctionalTestCase


class UpgradesTestCase(FunctionalTestCase):

    def test_upgrade_profile(self):
        # First set the entity encoding to a different value.
        tinymce = getUtility(ITinyMCE)
        tinymce.entity_encoding = u"named"

        # Then run the upgrade from 1.0. to 1.1.
        portal_setup = getToolByName(self.portal, 'portal_setup')
        upgrade_10_to_11(portal_setup)

        # And check the outcome
        self.assertEqual(tinymce.entity_encoding, u'raw')

    def test_upgrade_profile_12_13(self):
        portal_setup = getToolByName(self.portal, 'portal_setup')
        portal_jstool = getToolByName(self.portal, 'portal_javascripts')
        portal_ksstool = getToolByName(self.portal, 'portal_kss')
        
        new_ids = 'jquery.tinymce.js',
        js = portal_jstool.getResourceIds()
        for id in new_ids:    
            if id in js:
                portal_jstool.unregisterResource(id) 
        upgrade_12_to_13(portal_setup)
        js = portal_jstool.getResourceIds()
        for id in new_ids:
            self.assertIn(id, js)
        self.assertFalse('tiny_mce.js' in js)
        self.assertFalse('tiny_mce_init.js' in js)

        kss = portal_ksstool.getResourceIds()
        self.assertFalse('++resource++tinymce.kss/tinymce.kss' in kss)
        
