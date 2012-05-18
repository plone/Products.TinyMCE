import unittest

import zope.interface

from Products.TinyMCE.bbb import implementedOrProvidedBy


class TestObject(object):
    """ A simple object """


class ITestIface(zope.interface.Interface):
    """ A simple interface """


class BBBTests(unittest.TestCase):

    def test_implementedOrProvidedBy(self):
        myobj = TestObject()
        self.assertFalse(implementedOrProvidedBy(ITestIface, myobj))
        zope.interface.directlyProvides(myobj, ITestIface)
        self.assertTrue(implementedOrProvidedBy(ITestIface, myobj))
