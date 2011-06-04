from zope.component import queryUtility
from zope.component import getUtility
from Products.CMFCore.interfaces import IPropertiesTool

from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.tests.base import FunctionalTestCase
from Products.TinyMCE.setuphandlers import remove_editor
from Products.TinyMCE.setuphandlers import add_editor
from Products.TinyMCE.setuphandlers import unregisterUtility


class SetupHandlersTestCase(FunctionalTestCase):

    def test_remove_editor(self):
        # First let's remove the editor
        remove_editor(self.portal)

        # Check if it is removed.

        portal_props = getUtility(IPropertiesTool)
        site_props = getattr(portal_props, 'site_properties', None)
        attrname = 'available_editors'
        editors = list(site_props.getProperty(attrname))
        self.assertNotIn('TinyMCE', editors)

        # And now add the editor.
        add_editor(self.portal)

        # And check if it is added.
        editors = list(site_props.getProperty(attrname))
        self.assertIn('TinyMCE', editors)

    def test_unregister_utility(self):
        unregisterUtility(self.portal)

        # And check if the utility is removed.
        self.assertEqual(queryUtility(ITinyMCE, default='Not found'), 'Not found')
