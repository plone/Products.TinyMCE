from zope.component import getUtility
from Products.CMFCore.utils import getToolByName

from Products.TinyMCE.upgrades import upgrade_10_to_11
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
