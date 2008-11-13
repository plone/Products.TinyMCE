from Products.TinyMCE.tests.base import TinyMCETestCase
from Products.TinyMCE.interfaces.utility import ITinyMCE
from zope.component import getUtility
from zope.testing import doctestunit
from Testing import ZopeTestCase as ztc
import doctest
import unittest

def test_suite():
    """This sets up a test suite that actually runs the tests in transforms_integration.txt"""
    return unittest.TestSuite([
        # The actual test is in transforms_integration.txt
        ztc.ZopeDocFileSuite(
            'tests/transforms_integration.txt', package='Products.TinyMCE',
            test_class=TinyMCETestCase),
        ])
