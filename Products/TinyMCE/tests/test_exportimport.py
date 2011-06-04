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
          </resourcetypes>
        </object>
        """

        context = DummyImportContext(self.portal, purge=True)
        context._files = {'tinymce.xml': xml}

        # Now import the file.
        importTinyMCESettings(context)

        # Our specified plugin should now be stored in the utility.

        tinymce_utility = getUtility(ITinyMCE)
        self.assertIn('testplugin', tinymce_utility.customplugins)

        # Let's create a dummy export context.
        context = DummyExportContext(self.portal)

        # And export the current settings.
        exportTinyMCESettings(context)

        # Check if tinymce.xml is exported.
        self.assertEqual(context._wrote[0][0], 'tinymce.xml')

        # Check the contents of the export.
        self.assertIn('testplugin', context._wrote[0][1])
