#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for fut.core"""

import unittest
import responses
import re
import json
from sys import path, version_info

from fut import core
from fut.urls import messages_url, card_info_url
from fut.exceptions import FutError

if version_info[0] == 2:  # utf8 for python2
    from codecs import open


class FutCoreTestCase(unittest.TestCase):

    # _multiprocess_can_split_ = True

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEntryPoints(self):
        core.Core

    def testBaseId(self):
        # TODO: 3x test for every version
        self.assertEqual(core.baseId(124635), 124635)
        self.assertEqual(core.baseId(124635, return_version=True), (124635, 0))
        self.assertEqual(core.baseId(149147, return_version=True), (149147, 0))
        self.assertEqual(core.baseId(222492, return_version=True), (222492, 0))
        self.assertEqual(core.baseId(50510135, return_version=True), (178487, 3))
        self.assertEqual(core.baseId(50556989, return_version=True), (225341, 3))
        self.assertEqual(core.baseId(50562314, return_version=True), (230666, 3))
        self.assertEqual(core.baseId(67340541, return_version=True), (231677, 4))
        self.assertEqual(core.baseId(67319481, return_version=True), (210617, 4))
        self.assertEqual(core.baseId(84072233, return_version=True), (186153, 5))

    @responses.activate
    def testDatabase(self):
        responses.add(responses.GET,
                      messages_url,
                      body=open(path[0] + '/tests/data/en_US.json', 'r').read())
        responses.add(responses.GET,
                      '{0}{1}.json'.format(card_info_url, 'players'),
                      json=json.loads(open(path[0] + '/tests/data/players.json', 'r').read()))  # load json to avoid encoding errors

        self.db_nations = core.nations()
        self.db_leagues = core.leagues()
        self.db_teams = core.teams()
        self.db_stadiums = core.stadiums()
        self.db_balls = core.balls()
        self.db_players = core.players()
        self.db_playstyles = core.playstyles()

        # TODO: drop re, use xmltodict
        # TODO: year in config
        year = 2018
        rc = open(path[0] + '/tests/data/en_US.json', 'r', encoding='utf8').read()
        for i in re.findall('"search.nationName.nation([0-9]+)": "(.+)"', rc[:]):
            self.assertEqual(self.db_nations[int(i[0])], i[1])

        for i in re.findall('"global.leagueFull.%s.league([0-9]+)": "(.+)"' % year, rc[:]):
            self.assertEqual(self.db_leagues[int(i[0])], i[1])

        for i in re.findall('"global.teamFull.%s.team([0-9]+)": "(.+)"' % year, rc[:]):
            self.assertEqual(self.db_teams[int(i[0])], i[1])

        for i in re.findall('"global.stadiumFull.%s.stadium([0-9]+)": "(.+)"' % year, rc[:]):
            self.assertEqual(self.db_stadiums[int(i[0])], i[1])

        for i in re.findall('"BallName_([0-9]+)": "(.+)"', rc[:]):
            self.assertEqual(self.db_balls[int(i[0])], i[1])

        for i in re.findall('"playstyles.%s.playstyle([0-9]+)": "(.+)"' % year, rc[:]):
            self.assertEqual(self.db_playstyles[int(i[0])], i[1])

        rc = json.loads(open(path[0] + '/tests/data/players.json', 'r').read())
        for i in rc['Players'] + rc['LegendsPlayers']:
            self.assertEqual(self.db_players[i['id']],
                             {'id': i['id'],
                              'firstname': i['f'],
                              'lastname': i['l'],
                              'surname': i.get('c'),
                              'rating': i['r'],
                              'nationality': i['n']})

    def testInvalidAccount(self):
        #  TODO: responses
        self.assertRaises(FutError, core.Core, 'test', 'test', 'test', debug=True)
        # platforms
        self.assertRaises(FutError, core.Core, 'test', 'test', 'test', platform='xbox', debug=True)
        self.assertRaises(FutError, core.Core, 'test', 'test', 'test', platform='xbox360', debug=True)
        self.assertRaises(FutError, core.Core, 'test', 'test', 'test', platform='ps3', debug=True)
        self.assertRaises(FutError, core.Core, 'test', 'test', 'test', platform='ps4', debug=True)
        # emulate
        self.assertRaises(FutError, core.Core, 'test', 'test', 'test', emulate='ios', debug=True)
        self.assertRaises(FutError, core.Core, 'test', 'test', 'test', emulate='and', debug=True)


if __name__ == '__main__':
    unittest.main()
