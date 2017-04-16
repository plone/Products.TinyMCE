# -*- coding: utf-8 -*-

from Products.TinyMCE.tests.base import SELENIUM_TESTING
from plone.testing import layered

import os
import robotsuite
import unittest

dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
tests = [f for f in files if f.startswith('test_') and f.endswith('.txt')]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite(t), layer=SELENIUM_TESTING)
        for t in tests
    ])
    return suite
