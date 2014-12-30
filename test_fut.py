#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for fut."""

import unittest

import fut
from fut.exceptions import FutError


class FutTestCase(unittest.TestCase):

    # _multiprocess_can_split_ = True

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEntryPoints(self):
        fut.Core

    def testInvalidAccount(self):
        self.assertRaises(FutError, fut.Core, 'test', 'test', 'test')


if __name__ == '__main__':
    unittest.main()
