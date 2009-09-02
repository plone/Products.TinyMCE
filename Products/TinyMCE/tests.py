"""Test setup for integration and functional tests."""
import unittest

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """Set up the package and its dependencies."""
    
    fiveconfigure.debug_mode = True
    import Products.TinyMCE
    zcml.load_config('configure.zcml', Products.TinyMCE)
    fiveconfigure.debug_mode = False
    
setup_product()
ptc.setupPloneSite(products=['Products.TinyMCE'])

doc_tests = (
    'imagescales.txt',
    'transforms.txt',
    )

def test_suite():
    """This sets up a test suite that actually runs the tests"""
    return unittest.TestSuite(
        [ztc.ZopeDocFileSuite(
            'tests/%s' % f, package='Products.TinyMCE',
            test_class=ptc.FunctionalTestCase)
            for f in doc_tests],
        )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
