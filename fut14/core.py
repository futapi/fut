# -*- coding: utf-8 -*-

"""
fut14.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut14's basic methods.

"""

import requests
import xmltodict
import re
try:
    import simplejson as json
except ImportError:
    import json

from .config import headers
from .urls import urls
from .exceptions import Fut14Error
from .EAHashingAlgorithm import EAHashingAlgorithm


class Core(object):
    def __init__(self, email, passwd, secret_answer):
        # TODO: dynamic create urls based on urls['fut_config']
        self.email = email
        self.passwd = passwd
        eahashor = EAHashingAlgorithm()
        self.secret_answer_hash = eahashor.EAHash(secret_answer)
        self.urls = urls
        self.login(self.email, self.passwd, self.secret_answer_hash)

    def getUrls(self):
        """Gets services urls."""
        rc = xmltodict.parse(requests.get(self.urls['fut_config']).content)
        urls_fut = {}
        services = rc['main']['services']['prod']
        host = self.urls['main_site'].replace('https', 'http')  # it's not working with ssl...
        path = '/iframe/fut%s' % rc['main']['showOffServiceDestination']
        for i in services:
            urls_fut[i] = '%s%s%s' % (host, path, services[i])
        return urls_fut

    def login(self, email, passwd, secret_answer_hash):
        """Just log in."""
        self.r = requests.Session()  # init/reset requests session object
        self.r.headers = headers  # i'm chrome browser now ;-)

        # === update urls
        self.urls = urls
        self.urls['fut'] = self.getUrls()

        # === login
        self.urls['login'] = self.r.get(self.urls['fut_home']).url
        self.r.headers['Referer'] = self.urls['main_site']
        data = {'email': email, 'password': passwd, '_rememberMe': 'on', 'rememberMe': 'on', '_eventId': 'submit', 'facebookAuth': ''}
        rc = self.r.post(self.urls['login'], data=data).content
        # TODO: catch invalid data exception
        #self.nucleus_id = re.search('userid : "([0-9]+)"', rc).group(1)  # we'll get it later

        # === lanuch futweb
        rc = self.r.get(self.urls['futweb']).content
        if 'EASW_ID' not in rc:
            raise Fut14Error('Invalid email or password.')
        self.nucleus_id = re.search("var EASW_ID = '([0-9]+)';", rc).group(1)
        #self.urls['fut_base'] = re.search("var BASE_FUT_URL = '(https://.+?)';", rc).group(1)
        #self.urls['fut_home'] = re.search("var GUEST_APP_URI = '(http://.+?)';", rc).group(1)

        # prepare headers for ut operations
        self.r.headers['Content-Type'] = 'application/json'
        self.r.headers['Easw-Session-Data-Nucleus-Id'] = self.nucleus_id
        self.r.headers['X-UT-Embed-Error'] = 'true'
        self.r.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.r.headers['X-UT-Route'] = self.urls['fut_host']
        #self.r.headers['X-UT-PHISHING-TOKEN'] = ?
        #self.r.headers['X-HTTP-Method-Override'] = ?

        # acc info
        rc = self.r.get(self.urls['acc_info']).json()
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
        rc = self.r.post(self.urls['fut']['authentication'], data=json.dumps(data)).json()
        #self.urls['fut_host'] = '{0}://{1}'.format(rc['protocol']+rc['ipPort'])
        self.sid = rc['sid']
        self.r.headers['X-UT-SID'] = self.sid

        # validate (secret question)
        rc = self.r.get(self.urls['fut_question']).content
        # {"question":1,"attempts":5,"recoverAttempts":20}
        # answer question
        data = {'answer': self.secret_answer_hash}
        self.r.headers['Content-Type'] = 'application/x-www-form-urlencoded'  # requests bug?
        rc = self.r.post(self.urls['fut_validate'], data=data).json()
        self.r.headers['Content-Type'] = 'application/json'
        #{"debug":"Answer is correct.","string":"OK","reason":"Answer is correct.","token":"0000000000000000000","code":"200"}
        self.token = rc['token']
        self.r.headers['X-UT-PHISHING-TOKEN'] = self.token

        #print self.r.get('http://www.easports.com/iframe/fut/p/ut/game/fifa14/settings').content

        #self.r.headers['Referer'] = 'http://www.easports.com/iframe/fut/bundles/futweb/web/flash/FifaUltimateTeam.swf'

#    def shards(self):
#        """Returns shards info."""
#        self.r.headers['X-UT-Route'] = self.urls['fut_base']
#        return self.r.get(self.urls['shards']).json()
#        # self.r.headers['X-UT-Route'] = self.urls['fut_pc']
