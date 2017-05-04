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

    def testBaseId(self):
        # TODO: 3x test for every version
        self.assertEqual(fut.core.baseId(124635), 124635)
        self.assertEqual(fut.core.baseId(124635, return_version=True), (124635, 0))
        self.assertEqual(fut.core.baseId(149147, return_version=True), (149147, 0))
        self.assertEqual(fut.core.baseId(222492, return_version=True), (222492, 0))
        self.assertEqual(fut.core.baseId(50510135, return_version=True), (178487, 3))
        self.assertEqual(fut.core.baseId(50556989, return_version=True), (225341, 3))
        self.assertEqual(fut.core.baseId(50562314, return_version=True), (230666, 3))
        self.assertEqual(fut.core.baseId(67340541, return_version=True), (231677, 4))
        self.assertEqual(fut.core.baseId(67319481, return_version=True), (210617, 4))
        self.assertEqual(fut.core.baseId(84072233, return_version=True), (186153, 5))

    def testDatabase(self):
        self.db_nations = fut.core.nations()
        self.db_leagues = fut.core.leagues()
        self.db_teams = fut.core.teams()
        self.db_players = fut.core.players()

        self.assertEqual(self.db_nations[1], 'Albania')
        self.assertEqual(self.db_nations[133], 'Nigeria')
        self.assertEqual(self.db_nations[190], 'United Arab Emirates')
        self.assertEqual(self.db_leagues[68], u'Süper Lig')
        self.assertEqual(self.db_leagues[80], u'Österreichische Fußball-Bundesliga')
        self.assertEqual(self.db_leagues[66], 'T-Mobile Ekstraklasa')
        self.assertEqual(self.db_teams[1], 'Arsenal')
        self.assertEqual(self.db_teams[1458], u'SAİ Kayseri Erciyesspor')
        self.assertEqual(self.db_teams[111827], 'Club Deportivo Guadalajara')
        self.assertEqual(self.db_players[227223], {'lastname': 'Vita', 'surname': None, 'rating': 65, 'nationality': 27, 'id': 227223, 'firstname': 'Alessio'})
        self.assertEqual(self.db_players[159017], {'lastname': u'Hämäläinen', 'surname': None, 'rating': 72, 'nationality': 17, 'id': 159017, 'firstname': 'Kasper'})
        self.assertEqual(self.db_players[1179], {'lastname': 'Buffon', 'surname': None, 'rating': 88, 'nationality': 27, 'id': 1179, 'firstname': 'Gianluigi'})

    def testInvalidAccount(self):
        self.assertRaises(FutError, fut.Core, 'test', 'test', 'test', debug=True)
        # platforms
        self.assertRaises(FutError, fut.Core, 'test', 'test', 'test', platform='xbox', debug=True)
        self.assertRaises(FutError, fut.Core, 'test', 'test', 'test', platform='xbox360', debug=True)
        self.assertRaises(FutError, fut.Core, 'test', 'test', 'test', platform='ps3', debug=True)
        self.assertRaises(FutError, fut.Core, 'test', 'test', 'test', platform='ps4', debug=True)
        # emulate
        self.assertRaises(FutError, fut.Core, 'test', 'test', 'test', emulate='ios', debug=True)
        self.assertRaises(FutError, fut.Core, 'test', 'test', 'test', emulate='and', debug=True)


if __name__ == '__main__':
    unittest.main()
