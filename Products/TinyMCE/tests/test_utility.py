import unittest
from Products.TinyMCE.tests.base import TinyMCETestCase
from Products.TinyMCE.interfaces.utility import ITinyMCE
from zope.component import getUtility

class TestUtility(TinyMCETestCase):
    """Test the utility"""
    
    def afterSetUp(self):
        """Run before each test"""
        self.utility = getUtility(ITinyMCE)
        
    def beforeTearDown(self):
        """Run after each test"""

    def test_isTinyMCEEnabled(self):
        isenabled = self.utility.isTinyMCEEnabled
        self.failUnless(isenabled)

    def test_getEnabledButtons(self):
        buttons = self.utility.getEnabledButtons()
        self.failUnless(len(buttons) > 0)

    def test_translateButtonsFromKupu(self):
        kupubuttons = ['save-button', 'bold-button']
        buttons = self.utility.translateButtonsFromKupu(kupubuttons)
        self.failUnless(len(buttons) == 2)

def test_suite():
    """Setup test suite"""

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUtility))
    return suite
