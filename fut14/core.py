# -*- coding: utf-8 -*-

"""
fut14.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut14's basic methods.

"""

import requests
import xmltodict
#from time import time

from .config import headers
from .urls import urls
from .exceptions import Fut14Error
#from .EAHashingAlgorithm import EAHashingAlgorithm


class Core(object):
    def __init__(self, email, passwd, secret_answer):
        self.email = email
        self.passwd = passwd
        #eahashor = EAHashingAlgorithm()
        #self.secret_answer_hash = eahashor.EAHash(secret_answer)
        self.secret_answer_hash = None
        self.login(self.email, self.passwd, self.secret_answer_hash)

    def login(self, email, passwd, secret_answer_hash):
        """Just log in."""
        self.r = requests.Session()
        self.r.headers = headers
        self.r.headers['Referer'] = urls['main_site']
        data = {'email': email, 'password': passwd, 'overlay-stay-signed': 'ON'}
        rc = xmltodict.parse(self.r.post(urls['login'], data=data).content)

        if 'authenticate' in rc and rc['authenticate']['success'] == '0':
            raise Fut14Error('Invalid email or password.')

        self.player_id = rc['login']['player']['id']
        self.nucleus_id = rc['login']['player']['nucleusId']
        self.persona_id = rc['login']['player']['preferredPersona']['id']
        self.persona_gamertag = rc['login']['player']['preferredPersona']['gamertag']
        self.persona_platform = rc['login']['player']['preferredPersona']['platform']

        # prepare headers for ut operations
        self.r.headers['Content-Type'] = 'application/json'
        self.r.headers['Easw-Session-Data-Nucleus-Id'] = self.nucleus_id
        self.r.headers['X-UT-Embed-Error'] = 'true'
        self.r.headers['X-Requested-With'] = 'XMLHttpRequest'
        # TODO: dynamic create urls based on shards

#    def shards(self):
#        """Returns shards info."""
#        self.r.headers['X-UT-Route'] = urls['home']
#        return self.r.get(urls['shards']).json()

    def getClubs(self):
        """Returns all clubs info."""
        self.r.headers['X-UT-Route'] = urls['home_pc']
        rc = self.r.get(urls['acc_info']).json()
        clubs = [i for i in rc['userAccountInfo']['personas'][0]['userClubList']]
        return clubs
