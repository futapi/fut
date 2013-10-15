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
from .exceptions import Fut14Error
from .EAHashingAlgorithm import EAHashingAlgorithm


def base_id(resource_id):
    """Calculates base id."""
    if resource_id > 1358954496:
        resource_id -= 1342177280
    if resource_id > 67108864:
        resource_id -= 50331648
    while resource_id > 16777216:
        resource_id -= 16777216
    return resource_id

class Core(object):
    def __init__(self, email, passwd, secret_answer):
        # TODO: better headers managment ("ask" method?)
        # TODO: validate fut request response (200 OK)
        # TODO: card parser method (+base_id calculation)
        self.email = email
        self.passwd = passwd
        self.secret_answer_hash = EAHashingAlgorithm().EAHash(secret_answer)
        self.login(self.email, self.passwd, self.secret_answer_hash)

    def login(self, email, passwd, secret_answer_hash):
        """Just log in."""
        # TODO: update credits (acc info)
        self.r = requests.Session()  # init/reset requests session object
        self.r.headers = headers  # i'm chrome browser now ;-)

        # === login
        urls['login'] = self.r.get(urls['fut_home']).url
        self.r.headers['Referer'] = urls['main_site']  # prepare headers
        data = {'email': email, 'password': passwd, '_rememberMe': 'on', 'rememberMe': 'on', '_eventId': 'submit', 'facebookAuth': ''}
        rc = self.r.post(urls['login'], data=data).content
        # TODO: catch invalid data exception
        #self.nucleus_id = re.search('userid : "([0-9]+)"', rc).group(1)  # we'll get it later

        # === lanuch futweb
        self.r.headers['Referer'] = urls['fut_home']  # prepare headers
        rc = self.r.get(urls['futweb']).content
        if 'EASW_ID' not in rc:
            raise Fut14Error('Invalid email or password.')
        self.nucleus_id = re.search("var EASW_ID = '([0-9]+)';", rc).group(1)
        #urls['fut_base'] = re.search("var BASE_FUT_URL = '(https://.+?)';", rc).group(1)
        #urls['fut_home'] = re.search("var GUEST_APP_URI = '(http://.+?)';", rc).group(1)

        # acc info
        self.r.headers.update({  # prepare headers
            'Content-Type': 'application/json',
            'Accept': 'text/json',
            'Easw-Session-Data-Nucleus-Id': self.nucleus_id,
            'X-UT-Embed-Error': 'true',
            'X-Requested-With': 'XMLHttpRequest',
            'X-UT-Route': urls['fut_host'],
            'Referer': urls['futweb'],
        })
        rc = self.r.get(urls['acc_info']).json()
        self.persona_id = rc['userAccountInfo']['personas'][0]['personaId']
        self.persona_name = rc['userAccountInfo']['personas'][0]['personaName']
        self.clubs = [i for i in rc['userAccountInfo']['personas'][0]['userClubList']]
        # sort clubs by lastAccessTime (latest firts)
        self.clubs.sort(key=lambda i: i['lastAccessTime'], reverse=True)

        # authorization
        self.r.headers.update({  # prepare headers
            'Accept': 'application/json, text/javascript',
            'Origin': 'http://www.easports.com',
        })
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
        rc = self.r.post(urls['fut']['authentication'], data=json.dumps(data)).json()
        #urls['fut_host'] = '{0}://{1}'.format(rc['protocol']+rc['ipPort'])
        self.sid = rc['sid']
        self.r.headers['X-UT-SID'] = self.sid

        # validate (secret question)
        self.r.headers['Accept'] = 'text/json'  # prepare headers
        del self.r.headers['Origin']
        rc = self.r.get(urls['fut_question']).json()
        if rc.get('string') == 'Already answered question.':
            self.token = rc['string']
        else:
            # answer question
            data = {'answer': self.secret_answer_hash}
            self.r.headers['Content-Type'] = 'application/x-www-form-urlencoded'  # requests bug?
            rc = self.r.post(urls['fut_validate'], data=data).json()
            self.r.headers['Content-Type'] = 'application/json'
            self.token = rc['token']
        self.r.headers['X-UT-PHISHING-TOKEN'] = self.token

        # prepare headers for ut operations
        del self.r.headers['Easw-Session-Data-Nucleus-Id']
        del self.r.headers['X-Requested-With']
        del self.r.headers['X-UT-Route']
        self.r.headers.update({
            'X-HTTP-Method-Override': 'GET',
            'Referer': 'http://www.easports.com/iframe/fut/bundles/futweb/web/flash/FifaUltimateTeam.swf',
            'Origin': 'http://www.easports.com',
            #'Content-Type': 'application/json',  # already set
            'Accept': 'application/json',
        })

#    def shards(self):
#        """Returns shards info."""
#        # TODO: headers
#        self.r.headers['X-UT-Route'] = urls['fut_base']
#        return self.r.get(urls['shards']).json()
#        # self.r.headers['X-UT-Route'] = urls['fut_pc']

    def searchAuctions(self, ctype, level=None, category=None, min_price=None,
                       max_price=None, min_buy=None, max_buy=None, league=None,
                       club=None, position=None, nationality=None, playStyle=None,
                       start=0, page_size=16):
        """Search specific items on transfer market."""
        # TODO: add "search" alias
        if start > 0 and page_size == 16:
            page_size = 13
        params = {
            'start': start,
            'num': page_size,
            'type': ctype,  # "type" namespace is reserved in python
        }
        if level:       params['lev'] = level
        if category:    params['cat'] = category
        if min_price:   params['micr'] = min_price
        if max_price:   params['macr'] = max_price
        if min_buy:     params['minb'] = min_buy
        if max_buy:     params['maxb'] = max_buy
        if league:      params['leag'] = league
        if club:        params['team'] = club
        if position:    params['pos'] = position
        if nationality: params['nat'] = nationality
        if playStyle:   params['playStyle'] = playStyle

        rc = self.r.get(urls['fut']['SearchAuctions'], params=params).json()
        self.credits = rc['credits']

        items = []
        for i in rc['auctionInfo']:
            items.append({
                'tradeId':        i['tradeId'],
                'buyNowPrice':    i['buyNowPrice'],
                'tradeState':     i['tradeState'],
                'bidState':       i['bidState'],
                'startingBid':    i['startingBid'],
                'id':             i['itemData']['id'],
                'timestamp':      i['itemData']['timestamp'],  # auction start
                'rating':         i['itemData']['rating'],
                'assetId':        i['itemData']['assetId'],
                'resourceId':     i['itemData']['resourceId'],
                'itemState':      i['itemData']['itemState'],
                'rareflag':       i['itemData']['rareflag'],
                'formation':      i['itemData']['formation'],
                'injuryType':     i['itemData']['injuryType'],
                'suspension':     i['itemData']['suspension'],
                'contract':       i['itemData']['contract'],
                'playStyle':      i['itemData'].get('playStyle'),  # used only for players
                'discardValue':   i['itemData']['discardValue'],
                'itemType':       i['itemData']['itemType'],
                'owners':         i['itemData']['owners'],
                'offers':         i['offers'],
                'currentBid':     i['currentBid'],
                'expires':        i['expires'],  # seconds left
            })
        return items

    def bid(self, trade_id, bid):
        """Make a bid."""
        rc = self.r.get(urls['fut']['PostBid'], params={'tradeIds': trade_id}).json()
        if rc['auctionInfo'][0]['currentBid'] < bid and self.credits >= bid:
            data = {'bid': bid}
            url = '{0}/{1}/bid'.format(urls['fut']['PostBid'], trade_id)

            self.r.headers['X-HTTP-Method-Override'] = 'PUT'  # prepare headers
            rc = self.r.post(url, data=json.dumps(data)).json()
            self.r.headers['X-HTTP-Method-Override'] = 'GET'  # restore headers default

        self.credits = rc['credits']  # update credits info
        if rc['auctionInfo'][0]['bidState'] == 'highest':
            return True
        else:
            return False

    def tradepile(self):
        """Returns trade pile."""
        rc = self.r.get(urls['fut']['TradePile']).json()
        self.credits = rc['credits']  # update credits info

        items = []
        for i in rc['auctionInfo']:
            items.append({
                'tradeId':        i['tradeId'],
                'buyNowPrice':    i['buyNowPrice'],
                'tradeState':     i['tradeState'],
                'bidState':       i['bidState'],
                'startingBid':    i['startingBid'],
                'id':             i['itemData']['id'],
                'timestamp':      i['itemData']['timestamp'],  # auction start
                'rating':         i['itemData']['rating'],
                'assetId':        i['itemData']['assetId'],
                'resourceId':     i['itemData']['resourceId'],
                'itemState':      i['itemData']['itemState'],
                'rareflag':       i['itemData']['rareflag'],
                'formation':      i['itemData']['formation'],
                'injuryType':     i['itemData']['injuryType'],
                'suspension':     i['itemData']['suspension'],
                'contract':       i['itemData']['contract'],
                'playStyle':      i['itemData'].get('playStyle'),  # used only for players
                'discardValue':   i['itemData']['discardValue'],
                'itemType':       i['itemData']['itemType'],
                'owners':         i['itemData']['owners'],
                'offers':         i['offers'],
                'currentBid':     i['currentBid'],
                'expires':        i['expires'],  # seconds left
            })

        return items

#    def relistAll(self, item_id):
#        """Relist all items in trade pile."""
#        print self.r.get(urls['fut']['Item']+'/%s' % item_id).content

    def sell(self, item_id, bid, buy_now=0, duration=3600):
        """Starts auction."""
        data = {'buyNowPrice': buy_now, 'startingBid': bid, 'duration': duration, 'itemData':{'id': item_id}}

        self.r.headers['X-HTTP-Method-Override'] = 'POST'  # prepare headers
        rc = self.r.post(urls['fut']['SearchAuctionsListItem'], data=json.dumps(data)).json()
        self.r.headers['X-HTTP-Method-Override'] = 'GET'  # restore headers default

        return rc['id']

    def watchlist_delete(self, trade_id):
        """Removes card from watchlist."""
        params = {'tradeId': trade_id}

        self.r.headers['X-HTTP-Method-Override'] = 'DELETE'  # prepare headers
        self.r.post(urls['fut']['WatchList'], params=params)  # returns nothing
        self.r.headers['X-HTTP-Method-Override'] = 'GET'  # restore headers default

        return True

    def tradepile_delete(self, trade_id):
        """Removes card from tradepile."""
        url = '{}/{}'.format(urls['fut']['TradeInfo'], trade_id)

        self.r.headers['X-HTTP-Method-Override'] = 'DELETE'  # prepare headers
        self.r.post(url)  # returns nothing
        self.r.headers['X-HTTP-Method-Override'] = 'GET'  # restore headers default

        return True

    def send_to_tradepile(self, trade_id):
        """Sends to tradepile."""
        # TODO: accept multiple trade_ids (just extend list below (+ extend params?))
        data = {'auctionInfo': [{'id': trade_id}]}
        params = {'tradeId': trade_id}

        self.r.headers['X-HTTP-Method-Override'] = 'PUT'  # prepare headers
        self.r.post(urls['fut']['WatchList'], params=params, data=json.dumps(data))  # returns nothing
        self.r.headers['X-HTTP-Method-Override'] = 'GET'  # restore headers default

        return True
