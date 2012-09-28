"""
Test widget specific settings overrides.
"""
import json
import unittest2 as unittest

from zope.component import getMultiAdapter

from Products.TinyMCE.tests.base import FunctionalTestCase
from Products.TinyMCE.tests.base import HAS_AT

if HAS_AT:
    from Products.Archetypes import public as atapi

    # https://github.com/plone/Products.TinyMCE/blob/master/docs/source/usage.rst
    AT_FIELD = atapi.TextField(
        'testfield',
        widget=atapi.RichWidget(
            allow_buttons=(

                # Real button which appears in the output
                'bold-button',

                # Should not appear in the output as this button does not exist
                # in the orignal TinyMCE config
                'autodefenestration-button',
            ),

        ),
    )


class WidgetSettingTestCase(FunctionalTestCase):
    """ Test widget specific TinyMCE settings """

    def mockAtContent(self):
        """
        Return faked context object for AT rich text field.

        Create a content with one field which contains only one button set.
        """
        self.portal.invokeFactory("Document", "mydoc")
        doc = self.portal["mydoc"]
        _OrignalSchema = doc.Schema

        def Schema():
            fields = _OrignalSchema().copy()
            fields.addField(AT_FIELD)
            return fields

        doc.Schema = Schema  # I love the evilness of Python
        return doc

    @unittest.skipUnless(HAS_AT,
            'Archetypes is not installed. Skipping AT schema adapter test.')
    def test_at_button_settings(self):
        """
        Create a widget with allow_buttons set and see that these settings are correctly passed
        to the generated config JSON.
        """
        dummy = self.mockAtContent()
        view = getMultiAdapter((dummy, self.portal.REQUEST), name="tinymce-jsonconfiguration")
        view = view.__of__(dummy)

        # Settings output as JSON
        output = view("testfield")

        data = json.loads(output)

        # Mo other buttons should be available
        self.assertEqual(data[u"buttons"], [u'bold'])
