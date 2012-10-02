"""
This functionality is added to plone content types using adapters.
"""
import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.interface import implementsOnly

from z3c.form import interfaces as z3cform

from Products.TinyMCE.browser.browser import ConfigurationViewlet
from Products.TinyMCE.tests.base import FunctionalTestCase
from Products.TinyMCE.tests.base import HAS_DX, HAS_AT
from Products.Five import BrowserView

if HAS_DX:
    from plone.app.textfield.widget import IRichTextWidget

    class DummyRichTextField(object):
        __name__ = "text"

    class DummyRichTextWidget(object):
        implementsOnly(IRichTextWidget)

        field = DummyRichTextField()

    class DummyWidgets(object):
        prefix = 'widgets.'

        @staticmethod
        def values():
            return [DummyRichTextWidget()]

    class DummyFormView(BrowserView):
        implementsOnly(z3cform.IForm)

        widgets = DummyWidgets()
        prefix = 'form.'


class ConfigurationViewletTestCase(FunctionalTestCase):
    """ Test schema abstraction adapter """

    def makeone(self, context=None, request=None, view=None):
        if context is None:
            context = self.portal
        if request is None:
            request = self.app.REQUEST
        if view is None:
            view = getMultiAdapter(
                (context, request), name="plone"
                )
        return ConfigurationViewlet(context, request, view)

    @unittest.skipUnless(HAS_AT,
            'Archetypes is not installed. Skipping AT schema adapter test.')
    def test_atedit(self):
        self.portal.invokeFactory('Document', id='document')
        document = self.portal['document']
        viewlet = self.makeone(document)
        self.assertFalse(viewlet.suffix)
        self.assertTrue(viewlet.show())
        self.assertEqual(viewlet.suffix, '?p=&f=text')
        # make sure the full context path is in the URL to support
        # independent field configurations
        self.assertEqual(viewlet.render().strip(),
             ('<script type="text/javascript" src="http://nohost/plone/'
              'document/tiny_mce_gzip.js?p=&amp;f=text"></script>'))

    @unittest.skipUnless(HAS_DX,
            'Dexterity is not installed. Skipping DX schema adapter test.')
    def test_z3cform(self):
        view = DummyFormView(self.portal, self.app.REQUEST)
        viewlet = self.makeone(view=view)
        self.assertFalse(viewlet.suffix)
        self.assertTrue(viewlet.show())
        self.assertEqual(viewlet.suffix,
                '?p=form%5C%5C.widgets%5C%5C.&f=text')

    def test_formlib(self):
        from five.formlib import formbase
        from zope.formlib import form
        from zope.interface import Interface
        from zope import schema

        class IEditing(Interface):
            text = schema.Text()

        from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget

        class EditForm(formbase.EditFormBase):
            form_fields = form.Fields(IEditing)
            form_fields['text'].custom_widget = WYSIWYGWidget

        view = EditForm(self.portal, self.app.REQUEST)
        viewlet = self.makeone(view=view)
        self.assertFalse(viewlet.suffix)
        self.assertTrue(viewlet.show())
        self.assertEqual(viewlet.suffix, '?p=form%5C%5C.&f=text')
