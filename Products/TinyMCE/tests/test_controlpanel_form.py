import transaction
from plone.testing.z2 import Browser

from Products.TinyMCE.tests.base import FunctionalTestCase
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles


class ControlpanelTestCase(FunctionalTestCase):
    """ Test the fix for Ticket #12212  """

    def setUp(self):
        super(ControlpanelTestCase, self).setUp()
        # we need to be a Manager
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        transaction.commit()

    def test_cancel_button(self):
        browser = Browser(self.portal)
        portal_url = self.portal.absolute_url()

        # Get an account and login via the login form.
        browser.open(portal_url + '/login_form')
        browser.getControl(name='__ac_name').value = TEST_USER_NAME
        browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        browser.getControl(name='submit').click()

        # click the cancel button. Without the fix for #12212
        browser.open(portal_url + '/portal_tinymce/@@tinymce-controlpanel')
        browser.getControl(name='form.actions.cancel').click()
        self.assertTrue('<dd>Changes canceled.</dd>' in browser.contents)
        self.assertEqual(browser.url,
            'http://nohost/plone/plone_control_panel')

    def test_save_button(self):
        browser = Browser(self.portal)
        portal_url = self.portal.absolute_url()

        browser.open(portal_url + '/login_form')
        browser.getControl(name='__ac_name').value = TEST_USER_NAME
        browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        browser.getControl(name='submit').click()

        # click the save button. Because of the fix for #12212 we had to
        # extend the controlpanel form by own buttons
        browser.open(portal_url + '/portal_tinymce/@@tinymce-controlpanel')
        browser.getControl(name='form.contextmenu').value = False
        browser.getControl(name='form.actions.save').click()

        self.assertTrue('<dd>Changes saved.</dd>' in browser.contents)
        self.assertEqual(browser.url,
            'http://nohost/plone/portal_tinymce/@@tinymce-controlpanel')
