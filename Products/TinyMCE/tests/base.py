# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2


class TinyMCELayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import Products.TinyMCE
        self.loadZCML(package=Products.TinyMCE)
        z2.installProduct(app, 'Products.TinyMCE')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'Products.TinyMCE:TinyMCE')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'Products.TinyMCE')


FIXTURE = TinyMCELayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="TinyMCELayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="TinyMCELayer:Functional")
SELENIUM_TESTING = FunctionalTesting(
    bases=(FIXTURE, z2.ZSERVER_FIXTURE), name="TinyMCELayer:Selenium")


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)


class IntegrationTestCase(BaseTestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(BaseTestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING


class SeleniumTestCase(BaseTestCase):
    """Base class for functional tests."""

    layer = SELENIUM_TESTING
