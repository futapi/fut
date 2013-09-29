# -*- coding: utf-8 -*-

"""
fut14.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut14's basic methods.

"""

import requests
import re
try:
    import simplejson as json
except ImportError:
    import json

from .config import headers
from .urls import urls
#from .exceptions import Fut14Error
from .EAHashingAlgorithm import EAHashingAlgorithm


class Core(object):
    def __init__(self, email, passwd, secret_answer):
        self.email = email
        self.passwd = passwd
        eahashor = EAHashingAlgorithm()
        self.secret_answer_hash = eahashor.EAHash(secret_answer)
        self.login(self.email, self.passwd, self.secret_answer_hash)

    def login(self, email, passwd, secret_answer_hash):
        """Just log in."""
        self.r = requests.Session()  # init/reset requests session object
        self.r.headers = headers  # i'm chrome browser now ;-)

        # === login
        urls['login'] = self.r.get(urls['fut_home']).url
        self.r.headers['Referer'] = urls['main_site']
        data = {'email': email, 'password': passwd, '_rememberMe': 'on', 'rememberMe': 'on', '_eventId': 'submit', 'facebookAuth': ''}
        rc = self.r.post(urls['login'], data=data).content
        # TODO: catch invalid data exception
        #self.nucleus_id = re.search('userid : "([0-9]+)"', rc).group(1)  # we'll get it later

        # === lanuch futweb
        rc = self.r.get(urls['futweb']).content
        self.nucleus_id = re.search("var EASW_ID = '([0-9]+)';", rc).group(1)
        urls['fut_base'] = re.search("var BASE_FUT_URL = '(https://.+?)';", rc).group(1)

        # prepare headers for ut operations
        self.r.headers['Content-Type'] = 'application/json'
        self.r.headers['Easw-Session-Data-Nucleus-Id'] = self.nucleus_id
        self.r.headers['X-UT-Embed-Error'] = 'true'
        self.r.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.r.headers['X-UT-Route'] = urls['fut_host']
        #self.r.headers['X-UT-PHISHING-TOKEN'] = ?
        #self.r.headers['X-HTTP-Method-Override'] = ?
        # TODO: dynamic create urls based on shards

        # acc info
        rc = self.r.get(urls['acc_info']).json()
        self.persona_id = rc['userAccountInfo']['personas'][0]['personaId']
        self.persona_name = rc['userAccountInfo']['personas'][0]['personaName']
        self.clubs = [i for i in rc['userAccountInfo']['personas'][0]['userClubList']]
        # sort clubs by lastAccessTime (latest firts)
        self.clubs.sort(key=lambda i: i['lastAccessTime'], reverse=True)

        # authorization
        data = {'isReadOnly': False,
                'sku': 'FUT14WEB',
                'clientVersion': 1,
                'nuc': self.nucleus_id,
                'nucleusPersonaId': self.persona_id,
                'nucleusPersonaDisplayName': self.persona_name,
                'nucleusPersonaPlatform': 'pc',  # TODO: multiplatform
                'locale': 'en-GB',
                'method': 'authcode',
                'priorityLevel': 4,
                'identification': {'AuthCode': ''}}
        rc = self.r.post(urls['fut_auth'], data=json.dumps(data)).json()
        #urls['fut_host'] = '{0}://{1}'.format(rc['protocol']+rc['ipPort'])
        self.sid = rc['sid']
        self.r.headers['X-UT-SID'] = self.sid

        # validate (secret question)
        data = {'answer': self.secret_answer_hash}
        print self.r.post(urls['fut_validate'], data=json.dumps(data)).content

        #self.r.headers['Referer'] = 'http://www.easports.com/iframe/fut/bundles/futweb/web/flash/FifaUltimateTeam.swf'

#    def shards(self):
#        """Returns shards info."""
#        self.r.headers['X-UT-Route'] = urls['fut_base']
#        return self.r.get(urls['shards']).json()
#        # self.r.headers['X-UT-Route'] = urls['fut_pc']
