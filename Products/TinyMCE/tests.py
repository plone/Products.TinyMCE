"""Test setup for integration and functional tests."""

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

class TinyMCETestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit 
    test cases.
    """

class TinyMCEFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """
