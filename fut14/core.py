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


def base_id(resource_id, version=False):
    """Calculates base id."""
    v = 0
    if resource_id > 1358954496:
        resource_id -= 1342177280
        v += 1
    if resource_id > 67108864:
        resource_id -= 50331648
        v += 1
    while resource_id > 16777216:
        resource_id -= 16777216
        v += 1

    if version:
        return resource_id, v
    return resource_id

def item_parse(item_data):
    """Parser for item data. Returns nice dictionary."""
    return {
            'tradeId':      item_data['tradeId'],
            'buyNowPrice':  item_data['buyNowPrice'],
            'tradeState':   item_data['tradeState'],
            'bidState':     item_data['bidState'],
            'startingBid':  item_data['startingBid'],
            'id':           item_data['itemData']['id'],
            'timestamp':    item_data['itemData']['timestamp'],  # auction start
            'rating':       item_data['itemData']['rating'],
            'assetId':      item_data['itemData']['assetId'],
            'resourceId':   item_data['itemData']['resourceId'],
            'itemState':    item_data['itemData']['itemState'],
            'rareflag':     item_data['itemData']['rareflag'],
            'formation':    item_data['itemData']['formation'],
            'injuryType':   item_data['itemData']['injuryType'],
            'suspension':   item_data['itemData']['suspension'],
            'contract':     item_data['itemData']['contract'],
            'playStyle':    item_data['itemData'].get('playStyle'),  # used only for players
            'discardValue': item_data['itemData']['discardValue'],
            'itemType':     item_data['itemData']['itemType'],
            'owners':       item_data['itemData']['owners'],
            'offers':       item_data['offers'],
            'currentBid':   item_data['currentBid'],
            'expires':      item_data['expires'],  # seconds left
        }

def card_info(resource_id):
    """Returns card info."""
    # TODO: add referer to headers (futweb)
    url = '{}{}.json'.format(urls['card_info'], base_id(resource_id))
    return requests.get(url).json()


class Core(object):
    def __init__(self, email, passwd, secret_answer):
        # TODO: validate fut request response (200 OK)
        self.email = email
        self.passwd = passwd
        self.secret_answer_hash = EAHashingAlgorithm().EAHash(secret_answer)
        self.r = requests.Session()  # init/reset requests session object
        self.r.headers = headers  # i'm chrome browser now ;-)
        self.credits = 0
        self.__login__(self.email, self.passwd, self.secret_answer_hash)

    def __login__(self, email, passwd, secret_answer_hash):
        """Just log in."""
        # === login
        urls['login'] = self.r.get(urls['fut_home']).url
        self.r.headers['Referer'] = urls['main_site']  # prepare headers
        data = {'email': email, 'password': passwd, '_rememberMe': 'on',
                'rememberMe': 'on', '_eventId': 'submit', 'facebookAuth': ''}
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
            #'X-HTTP-Method-Override': 'GET',  # __request__ method manages this
            'Referer': 'http://www.easports.com/iframe/fut/bundles/futweb/web/flash/FifaUltimateTeam.swf',
            'Origin': 'http://www.easports.com',
            #'Content-Type': 'application/json',  # already set
            'Accept': 'application/json',
        })

#    def __shards__(self):
#        """Returns shards info."""
#        # TODO: headers
#        self.r.headers['X-UT-Route'] = urls['fut_base']
#        return self.r.get(urls['shards']).json()
#        # self.r.headers['X-UT-Route'] = urls['fut_pc']

    def __request__(self, method, url, *args, **kwargs):
        """Prepares headers and sends request. Returns response as a json object."""
        # TODO: update credtis?
        self.r.headers['X-HTTP-Method-Override'] = method.upper()
        rc = self.r.post(url, *args, **kwargs)
        if rc.content == '':
            rc = {}
        else:
            rc = rc.json()
            self.credits = rc.get('credits', self.credits)  # update credits
        return rc

    def __get__(self, url, *args, **kwargs):
        """Sends get request. Returns response as a json object."""
        return self.__request__('GET', url, *args, **kwargs)

    def __post__(self, url, *args, **kwargs):
        """Sends post request. Returns response as a json object."""
        return self.__request__('POST', url, *args, **kwargs)

    def __put__(self, url, *args, **kwargs):
        """Sends put request. Returns response as a json object."""
        return self.__request__('PUT', url, *args, **kwargs)

    def __delete__(self, url, *args, **kwargs):
        """Sends delete request. Returns response as a json object."""
        return self.__request__('DELETE', url, *args, **kwargs)

    def base_id(self, *args, **kwargs):
        """Alias for base_id."""
        return base_id(*args, **kwargs)

    def card_info(self, *args, **kwargs):
        """Alias for card_info."""
        return card_info(*args, **kwargs)

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

        rc = self.__get__(urls['fut']['SearchAuctions'], params=params)

        items = []
        for i in rc['auctionInfo']:
            items.append(item_parse(i))
        return items

    def bid(self, trade_id, bid):
        """Make a bid."""
        rc = self.__get__(urls['fut']['PostBid'], params={'tradeIds': trade_id})
        if rc['auctionInfo'][0]['currentBid'] < bid and self.credits >= bid:
            data = {'bid': bid}
            url = '{0}/{1}/bid'.format(urls['fut']['PostBid'], trade_id)
            rc = self.__put__(url, data=json.dumps(data))

        if rc['auctionInfo'][0]['bidState'] == 'highest':
            return True
        else:
            return False

    def tradepile(self):
        """Returns items in tradepile."""
        rc = self.__get__(urls['fut']['TradePile'])

        items = []
        for i in rc['auctionInfo']:
            items.append(item_parse(i))

        return items

    def watchlist(self):
        """Returns items in watchlist."""
        rc = self.__get__(urls['fut']['WatchList'])

        items = []
        for i in rc['auctionInfo']:
            items.append(item_parse(i))

        return items

#    def relistAll(self, item_id):
#        """Relist all items in trade pile."""
#        print self.r.get(urls['fut']['Item']+'/%s' % item_id).content

    def sell(self, item_id, bid, buy_now=0, duration=3600):
        """Starts auction."""
        data = {'buyNowPrice': buy_now, 'startingBid': bid, 'duration': duration, 'itemData':{'id': item_id}}
        rc = self.__post__(urls['fut']['SearchAuctionsListItem'], data=json.dumps(data))
        return rc['id']

    def watchlist_delete(self, trade_id):
        """Removes card from watchlist."""
        params = {'tradeId': trade_id}
        self.__delete__(urls['fut']['WatchList'], params=params)  # returns nothing
        return True

    def tradepile_delete(self, trade_id):
        """Removes card from tradepile."""
        url = '{}/{}'.format(urls['fut']['TradeInfo'], trade_id)
        self.__delete__(url)  # returns nothing
        return True

    def send_to_tradepile(self, trade_id, item_id):
        """Sends to tradepile."""
        # TODO: accept multiple trade_ids (just extend list below (+ extend params?))
        data = {"itemData": [{"tradeId": trade_id, "pile": "trade", "id": str(item_id)}]}
        rc = self.__put__(urls['fut']['Item'], data=json.dumps(data))
        return rc['itemData'][0]['success']
