# -*- coding: utf-8 -*-

"""
fut.db
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut's database.

"""
import requests
import re
from .config import timeout
from .urls import urls


class Nation(object):
    """Nation object.

    :param id: nation id.
    :param name: nation name.
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name


class League(object):
    """League object.

    :param id: league id.
    :param name: league name.
    :param year: year.
    """
    def __init__(self, id, name, year):
        self.id = id
        self.name = name
        self.year = year


class Team(object):
    """Team object.

    :param id: team id.
    :param name: team name.
    :param year: year.
    """
    def __init__(self, id, name, year):
        self.id = id
        self.name = name
        self.year = year


class Player(object):
    """Player object.

    :param id: player id/base_id.
    :param firstname: firstname.
    :param lastname: lastname.
    :param surname: surname, not every player has it.
    :param rating: rating.
    :param nationality: nationality.
    """
    def __init__(self, id, firstname, lastname, surname, rating, nationality):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.rating = rating
        self.nationality = nationality


class Db(object):
    def __init__(self, timeout=timeout):
        self.timeout = timeout
        self.messages = requests.get(urls('pc')['messages'], timeout=self.timeout).text  # TODO: optimizate by not using text here
        self._nations = None
        self._leagues = {}
        self._teams = {}
        self._players = None
        # TODO: optimize messages, xml parser might be faster

    def nations(self):
        """Return all nations in dict {id0: nation0, id1: nation1}."""
        if not self._nations:
            print('reload nations')
            data = re.findall('<trans-unit resname="search.nationName.nation([0-9]+)">\n        <source>(.+)</source>', self.messages)
            self._nations = {}
            for i in data:
                self._nations[int(i[0])] = Nation(i[0], i[1])
        return self._nations

    def leagues(self, year=2017):
        """Return all leagues in dict {id0: league0, id1: legaue1}.

        :params year: Year.
        """
        if year not in self._leagues:
            data = re.findall('<trans-unit resname="global.leagueFull.%s.league([0-9]+)">\n        <source>(.+)</source>' % year, self.messages)
            self._leagues[year] = {}
            for i in data:
                self._leagues[year][int(i[0])] = League(i[0], i[1], year=year)
        return self._leagues[year]


    def teams(self, year=2017):
        """Return all teams in dict {id0: team0, id1: team1}.

        :params year: Year.
        """
        if year not in self._teams:
            data = re.findall('<trans-unit resname="global.teamFull.%s.team([0-9]+)">\n        <source>(.+)</source>' % year, self.messages)
            self._teams[year] = {}
            for i in data:
                self._teams[year][int(i[0])] = Team(i[0], i[1], year=year)
        return self._teams[year]

    def players(self):
        """Return all players."""
        if not self._players:
            rc = requests.get('{0}{1}.json'.format(urls('pc')['card_info'], 'players'), timeout=self.timeout).json()
            self._players = {}
            for i in rc['Players'] + rc['LegendsPlayers']:
                self._players[i['id']] = Player(id=i['id'],
                                           firstname=i['f'],
                                           lastname=i['l'],
                                           surname=i.get('c'),
                                           rating=i['r'],
                                           nationality=self.nations()[i['n']])
        return self._players
