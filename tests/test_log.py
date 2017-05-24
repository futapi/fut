#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for fut.log"""

import unittest

from fut import log


class FutLogTestCase(unittest.TestCase):

    # _multiprocess_can_split_ = True

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEntryPoints(self):
        log.logger

    def testLogger(self):
        self.logger = log.logger(save=True)
        self.logger.debug('test ąćóżź')
        self.logger.info('test ąćóżź')
        self.logger.warning('test ąćóżź')
        self.logger.error('test ąćóżź')
        self.logger.critical('test ąćóżź')

        log_dump = open('fut.log', 'r').read()

        self.assertRegexpMatches(log_dump, '[0-9\- :,]+ \[DEBUG\] \[.+?\] testLogger: test ąćóżź \(line [0-9]+\)')
        self.assertRegexpMatches(log_dump, '[0-9\- :,]+ \[INFO\] \[.+?\] testLogger: test ąćóżź \(line [0-9]+\)')
        self.assertRegexpMatches(log_dump, '[0-9\- :,]+ \[WARNING\] \[.+?\] testLogger: test ąćóżź \(line [0-9]+\)')
        self.assertRegexpMatches(log_dump, '[0-9\- :,]+ \[ERROR\] \[.+?\] testLogger: test ąćóżź \(line [0-9]+\)')
        self.assertRegexpMatches(log_dump, '[0-9\- :,]+ \[CRITICAL\] \[.+?\] testLogger: test ąćóżź \(line [0-9]+\)')

    # def testNullLogger(self):
    #     self.logger = log.logger(save=False)
    #     self.logger.debug('test ąćóżź')
    #     log_dump = open('fut.log', 'r').read()
    #     self.assertEqual(log_dump, '')


if __name__ == '__main__':
    unittest.main()
