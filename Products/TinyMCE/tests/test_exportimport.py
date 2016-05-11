from zope.component import getUtility
from Products.GenericSetup.tests.common import DummyImportContext
from Products.GenericSetup.tests.common import DummyExportContext

from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.exportimport import importTinyMCESettings
from Products.TinyMCE.exportimport import exportTinyMCESettings
from Products.TinyMCE.tests.base import FunctionalTestCase


class ImportExportTestCase(FunctionalTestCase):

    def test_import_export(self):
        # This module takes care of exporting and importing settings of TinyMCE. Let's
        # create a dummy import context. And a dummy file.

        xml = """\
        <object>
          <resourcetypes>
            <link_using_uids value="True"/>
            <customplugins purge="True">
              <element value="testplugin"/>
            </customplugins>
            <linkable purge="False">
              <element value="Topic"/>
            </linkable>
            <customplugins purge="True">
              <element value="testplugin"/>
            </customplugins>
            <plugins>
              <element value="ploneinlinestyles"/>
              <element value="plonebrowser"/>
            </plugins>
          </resourcetypes>
          <contentbrowser>
            <anchor_selector value="h2,h3"/>
            <link_shortcuts />
          </contentbrowser>
        </object>
        """

        context = DummyImportContext(self.portal, purge=True)
        context._files = {'tinymce.xml': xml}

        # Now import the file.
        importTinyMCESettings(context)

        # Our specified plugin should now be stored in the utility.

        tinymce_utility = getUtility(ITinyMCE)
        self.assertIn('testplugin', tinymce_utility.customplugins)
        self.assertIn('ploneinlinestyles', tinymce_utility.plugins)
        self.assertIn('plonebrowser', tinymce_utility.plugins)
        self.assertTrue(isinstance(tinymce_utility.plugins, (list, tuple)))
        self.assertFalse(tinymce_utility.link_shortcuts)
        self.assertTrue(isinstance(tinymce_utility.link_shortcuts, (list, tuple)))

        # Let's create a dummy export context.
        context = DummyExportContext(self.portal)

        # And export the current settings.
        exportTinyMCESettings(context)

        # Check if tinymce.xml is exported.
        self.assertEqual(context._wrote[0][0], 'tinymce.xml')

        # Check the contents of the export.
        self.assertIn('testplugin', context._wrote[0][1])
