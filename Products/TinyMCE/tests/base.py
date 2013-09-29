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


# Test for Archetypes
try:
    import Products.Archetypes
    Products.Archetypes    # pyflakes
    HAS_AT = True
except ImportError:
    HAS_AT = False

# Test for Dexterity
try:
    import plone.app.contenttypes
    plone.app.contenttypes   # pyflakes
    HAS_DX = True
except ImportError:
    HAS_DX = False

# register testing types in portal_setup
from Products.GenericSetup import EXTENSION, profile_registry
def register_test_profile():
    profile_registry.registerProfile('tinymce_testing',
            'TinyMCE testing profile',
            'Extension profile for testing TinyMCE including sample content types',
            'profiles/testing',
            'Products.TinyMCE',
            EXTENSION)


class TinyMCELayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import Products.TinyMCE
        self.loadZCML(package=Products.TinyMCE)
        import Products.TinyMCE.tests
        self.loadZCML(package=Products.TinyMCE.tests,
                      name='skins.zcml')
        z2.installProduct(app, 'Products.TinyMCE')
        if HAS_DX:
            self.loadZCML(package=plone.app.contenttypes)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'Products.TinyMCE:TinyMCE')
        if HAS_DX:
            self.applyProfile(portal, 'plone.app.contenttypes:default')
            register_test_profile()
            self.applyProfile(portal, 'Products.TinyMCE:tinymce_testing')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'Products.TinyMCE')


FIXTURE = TinyMCELayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="TinyMCELayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="TinyMCELayer:Functional")


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
