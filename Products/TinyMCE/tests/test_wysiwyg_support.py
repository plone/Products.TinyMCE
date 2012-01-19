import re

import transaction
from plone.testing.z2 import Browser

from Products.TinyMCE.tests.base import IntegrationTestCase
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD


class WysiwygSupportTestCase(IntegrationTestCase):

    def setUp(self):
        super(WysiwygSupportTestCase, self).setUp()
        # Unhide exceptions.

    def test_personalized(self):
        self.portal.error_log._ignored_exceptions = ()
        browser = Browser(self.app)
        portal_url = self.portal.absolute_url()

        # Get an account and login via the login form.
        browser.open(portal_url + '/login_form')
        browser.getControl(name='__ac_name').value = TEST_USER_NAME
        browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        browser.getControl(name='submit').click()

        # Create a blank page for test edits. (front-page is too noisy.)
        testpage = self.portal.absolute_url() + '/' + self.portal.invokeFactory('Document', 'testpage') + '/edit'
        self.assertEqual(testpage, 'http://nohost/plone/testpage/edit')
        transaction.commit()

        # Set up personalize_form
        personalizer = portal_url + '/personalize_form'
        self.assertEqual(personalizer, 'http://nohost/plone/personalize_form')
        browser.open(personalizer)
        browser.getControl(name='email').value = 'test@example.org'
        browser.getControl(name='form.button.Save').click()
        self.assertIn('<dd>Your personal settings have been saved.</dd>', browser.contents)

        #Test different editors
        #----------------------
        #Which editor is used is set globally and can be overridden in the personal preferences.
        #This results in the following matrix:
        #=====       =====                   ======
        #Global      Personal                Expected
        #=====       =====                   ======
        #TinyMCE     Use site's default      TinyMCE
        #TinyMCE     None                    Basic textarea
        #TinyMCE     TinyMCE                 TinyMCE
        #<empty>     Use site's default      Basic textarea
        #<empty>     None                    Basic textarea
        #<empty>     TinyMCE                 TinyMCE
        #=====       =====                   ======

        # Set the editor globally to TinyMCE:
        self.portal.portal_properties.site_properties.default_editor = 'TinyMCE'
        transaction.commit()

        # If the user sets 'Use site's default'...
        browser.open(personalizer)
        browser.getControl(name='wysiwyg_editor').value = ['']
        browser.getControl(name='form.button.Save').click()
        self.assertIn('<dd>Your personal settings have been saved.</dd>', browser.contents)

        # we should get TinyMCE:
        browser.open(testpage)
        self.assertIn('tiny_mce_gzip.js', browser.contents)
        self.assertIn('jquery.tinymce', browser.contents)

        # If the user sets 'None'...
        browser.open(personalizer)
        browser.getControl(name='wysiwyg_editor').value = ['None']
        browser.getControl(name='form.button.Save').click()
        self.assertIn('<dd>Your personal settings have been saved.</dd>', browser.contents)

        # We should get just a textarea:
        browser.open(testpage)
        # The '[\W]*' means: any number and type of white space.  We
        # do this because in combination with five.pt the html can be
        # slightly different.
        self.assertTrue(
            re.search('<textarea name="text"[\W]*rows="25"[\W]id="text"',
                       browser.contents) is not None)

        # If the user sets 'TinyMCE'...
        browser.open(personalizer)
        browser.getControl(name='wysiwyg_editor').value = ['TinyMCE']
        browser.getControl(name='form.button.Save').click()
        self.assertIn('<dd>Your personal settings have been saved.</dd>', browser.contents)

        # we should get TinyMCE:
        browser.open(testpage)
        self.assertIn('tiny_mce_gzip.js', browser.contents)
        self.assertIn('jquery.tinymce', browser.contents)

        # Set the editor globally to nothing:
        self.portal.portal_properties.site_properties.default_editor = ''
        transaction.commit()

        # If the user sets 'Use site's default'...
        browser.open(personalizer)
        browser.getControl(name='wysiwyg_editor').value = ['']
        browser.getControl(name='form.button.Save').click()
        self.assertIn('<dd>Your personal settings have been saved.</dd>', browser.contents)

        # we should get just a textarea:
        browser.open(testpage)
        self.assertTrue(
            re.search('<textarea name="text"[\W]*rows="25"[\W]id="text"',
                       browser.contents) is not None)

        # If the user sets 'None'...
        browser.open(personalizer)
        browser.getControl(name='wysiwyg_editor').value = ['None']
        browser.getControl(name='form.button.Save').click()
        self.assertIn('<dd>Your personal settings have been saved.</dd>', browser.contents)

        # we should get just a textarea:
        browser.open(testpage)
        self.assertTrue(
            re.search('<textarea name="text"[\W]*rows="25"[\W]id="text"',
                       browser.contents) is not None)

        # If the user sets 'TinyMCE'...
        browser.open(personalizer)
        browser.getControl(name='wysiwyg_editor').value = ['TinyMCE']
        browser.getControl(name='form.button.Save').click()
        self.assertIn('<dd>Your personal settings have been saved.</dd>', browser.contents)

        # we should get TinyMCE:
        browser.open(testpage)
        self.assertIn('tiny_mce_gzip.js', browser.contents)
        self.assertIn('jquery.tinymce', browser.contents)
