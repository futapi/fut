#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for fut14."""

import unittest

import fut14
from fut14.exceptions import Fut14Error


class Fut14TestCase(unittest.TestCase):

    #_multiprocess_can_split_ = True

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEntryPoints(self):
        fut14.Core

    def testInvalidAccount(self):
        self.assertRaises(Fut14Error, fut14.Core, 'test', 'test', 'test')


if __name__ == '__main__':
    unittest.main()
