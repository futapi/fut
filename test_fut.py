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
        self.assertEqual(fut.core.baseId(149147), 149147)
        self.assertEqual(fut.core.baseId(205069), 205069)
        self.assertEqual(fut.core.baseId(173306), 173306)
        self.assertEqual(fut.core.baseId(173208), 173208)
        self.assertEqual(fut.core.baseId(164082), 164082)
        self.assertEqual(fut.core.baseId(222492), 222492)
        self.assertEqual(fut.core.baseId(124635), 124635)
        self.assertEqual(fut.core.baseId(194911), 194911)
        self.assertEqual(fut.core.baseId(50562314), 230666)
        self.assertEqual(fut.core.baseId(67340541), 231677)
        self.assertEqual(fut.core.baseId(84072233), 186153)
        self.assertEqual(fut.core.baseId(67319481), 210617)
        self.assertEqual(fut.core.baseId(50510135), 178487)
        self.assertEqual(fut.core.baseId(50556989), 225341)
        self.assertEqual(fut.core.baseId(67340541), 231677)

    def testDatabase(self):
        self.db_nations = fut.core.nations()
        self.db_leagues = fut.core.leagues()
        self.db_teams = fut.core.teams()
        self.db_players = fut.core.players()

        self.assertEqual(self.db_nations[1], 'Albania')
        self.assertEqual(self.db_nations[133], 'Nigeria')
        self.assertEqual(self.db_nations[190], 'United Arab Emirates')
        self.assertEqual(self.db_leagues[68], 'Süper Lig')
        self.assertEqual(self.db_leagues[80], 'Österreichische Fußball-Bundesliga')
        self.assertEqual(self.db_leagues[66], 'T-Mobile Ekstraklasa')
        self.assertEqual(self.db_teams[1], 'Arsenal')
        self.assertEqual(self.db_teams[1458], 'SAİ Kayseri Erciyesspor')
        self.assertEqual(self.db_teams[111827], 'Club Deportivo Guadalajara')
        self.assertEqual(self.db_players[227223], {'lastname': 'Vita', 'surname': None, 'rating': 65, 'nationality': 27, 'id': 227223, 'firstname': 'Alessio'})
        self.assertEqual(self.db_players[159017], {'lastname': 'Hämäläinen', 'surname': None, 'rating': 72, 'nationality': 17, 'id': 159017, 'firstname': 'Kasper'})
        self.assertEqual(self.db_players[1179], {'lastname': 'Buffon', 'surname': None, 'rating': 88, 'nationality': 27, 'id': 1179, 'firstname': 'Gianluigi'})

    def testInvalidAccount(self):
        self.assertRaises(FutError, fut.Core, 'test', 'test', 'test')


if __name__ == '__main__':
    unittest.main()
