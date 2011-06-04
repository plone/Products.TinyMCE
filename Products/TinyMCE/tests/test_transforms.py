from zope.component import getUtility

from Products.CMFPlone.tests import dummy
from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE.tests.base import FunctionalTestCase


class TransformsTestCase(FunctionalTestCase):

        # Tests integration with plone.outputfilters, which provides 2 filters that are
        # applied while rendering rich text:

        # * Resolving UID links to absolute URIs.
        # * Adding captions to images with the "captioned" CSS class.

        # These filters used to be implemented in Products.TinyMCE, so for backwards
        # compatibility they can be enabled via settings in the TinyMCE control panel.

    def test_filters(self):
        # Let's turn these filters on first.
        tinymce_utility = getUtility(ITinyMCE)
        tinymce_utility.link_using_uids = True
        tinymce_utility.allow_captioned_images = True

        # To test the settings, we'll need an image.
        self.portal.invokeFactory('Image', id='image.jpg', title="Image", file=dummy.Image())
        image = getattr(self.portal, 'image.jpg')
        image.setDescription('My caption')
        image.reindexObject()
        UID = image.UID()

        # Let's transform some text/html to text/x-html-safe, which should trigger the
        # filters.
        text = """
<html>
   <head></head>
   <body>
       <img src="resolveuid/%s/image_thumb" class="image-left captioned" width="200" alt="My alt text" />
       <p><img src="/image.jpg" class="image-right captioned" width="200" style="border-width:1px" /></p>
       <pre>This is line 1
             This is line 2</pre>
   </body>
</html>""" % UID
        transformed_text = self.portal.portal_transforms.convertTo('text/x-html-safe', text, mimetype='text/html', context=self.portal)

        # The UID reference should be converted to an absolute url, and a caption should be added.
        self.assertEqual(unicode(transformed_text).replace(' ', ''), u"""
<dl style="width:200px;" class="image-left captioned">
<dt><img src="http://nohost/plone/image.jpg/image_thumb" alt="My alt text" title="Image" height="16" width="200" /></dt>
 <dd class="image-caption" style="width:200px;">My caption</dd>
</dl>
<p><dl style="width:200px;" class="image-right captioned">
<dt><img src="http://nohost/plone/image.jpg/image" alt="Image" title="Image" height="16" width="200" style="border-width:1px" /></dt>
 <dd class="image-caption" style="width:200px;">My caption</dd>
</dl></p>
<pre>This is line 1
      This is line 2</pre>
""".replace(' ', ''))
        # Now turn off the settings.
        tinymce_utility.link_using_uids = False
        tinymce_utility.allow_captioned_images = False

        # Now the filters should not be applied.
        transformed_text_2 = self.portal.portal_transforms.convertTo('text/x-html-safe', text, mimetype='text/html', context=self.portal)
        self.assertNotEqual(unicode(transformed_text_2).replace(' ', ''), unicode(transformed_text).replace(' ', ''))
