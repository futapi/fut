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


def baseId(resource_id, version=False):
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

def itemParse(item_data):
    """Parser for item data. Returns nice dictionary."""
    return {
            'tradeId':      item_data['tradeId'],
            'buyNowPrice':  item_data['buyNowPrice'],
            'tradeState':   item_data['tradeState'],
            'bidState':     item_data['bidState'],
            'startingBid':  item_data['startingBid'],
            'id':           item_data['itemData']['id'],  # auction start
            'timestamp':    item_data['itemData']['timestamp'],
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

def auctionParse(auction_data):
    """
    auction paser
    """
    return {
        'id':           auction_data['id'],  # auction start
        'timestamp':    auction_data['timestamp'],
        'rating':       auction_data['rating'],
        'assetId':      auction_data['assetId'],
        'resourceId':   auction_data['resourceId'],
        'itemState':    auction_data['itemState'],
        'rareflag':     auction_data['rareflag'],
        'formation':    auction_data['formation'],
        'injuryType':   auction_data['injuryType'],
        'injuryGames':  auction_data['injuryGames'],
        'lastSalePrice':auction_data['lastSalePrice'],
        'fitness':      auction_data['fitness'],
        'training':     auction_data['training'],
        'discardValue': auction_data['discardValue'],
        'suspension':   auction_data['suspension'],
        'contract':     auction_data['contract'],
        'playStyle':    auction_data.get('playStyle'),  # used only for players
        'discardValue': auction_data['discardValue'],
        'itemType':     auction_data['itemType'],
        'owners':       auction_data['owners'],
    }

def cardInfo(resource_id):
    """Returns card info."""
    # TODO: add referer to headers (futweb)
    url = '{}{}.json'.format(urls['card_info'], baseId(resource_id))
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
        data = {'email': email,
                'password': passwd,
                '_rememberMe': 'on',
                'rememberMe': 'on',
                '_eventId':
                'submit', 'facebookAuth': ''}
        rc = self.r.post(urls['login'], data=data).text
        # TODO: catch invalid data exception
        #self.nucleus_id = re.search('userid : "([0-9]+)"', rc).group(1)  # we'll get it later

        # === lanuch futweb
        self.r.headers['Referer'] = urls['fut_home']  # prepare headers
        rc = self.r.get(urls['futweb']).text
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
        rc = self.r.get(urls['acc_info']).json()['userAccountInfo']['personas'][0]
        self.persona_id = rc['personaId']
        self.persona_name = rc['personaName']
        self.clubs = [i for i in rc['userClubList']]
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
        self.r.headers['X-UT-SID'] = self.sid = rc['sid']

        # validate (secret question)
        self.r.headers['Accept'] = 'text/json'  # prepare headers
        del self.r.headers['Origin']
        rc = self.r.get(urls['fut_question']).json()
        if rc.get('string') != 'Already answered question.':
            # answer question
            data = {'answer': self.secret_answer_hash}
            self.r.headers['Content-Type'] = 'application/x-www-form-urlencoded'  # requests bug?
            rc = self.r.post(urls['fut_validate'], data=data).json()
            self.r.headers['Content-Type'] = 'application/json'
        self.r.headers['X-UT-PHISHING-TOKEN'] = self.token = rc['token']

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
        if rc.text == '':
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

    def baseId(self, *args, **kwargs):
        """Alias for baseId."""
        return baseId(*args, **kwargs)

    def cardInfo(self, *args, **kwargs):
        """Alias for cardInfo."""
        return cardInfo(*args, **kwargs)

    def searchAuctions(self, ctype, level=None, category=None, min_price=None,
                       max_price=None, min_buy=None, max_buy=None, league=None,
                       club=None, position=None, nationality=None, playStyle=None,
                       start=0, page_size=16):
        """Search specific items on transfer market."""
        # TODO: add "search" alias
        if start > 0 and page_size == 16:
            page_size = 13
        elif page_size > 50:  # server restriction
            page_size = 50
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
        return [itemParse(i) for i in rc['auctionInfo']]

    def bid(self, trade_id, bid):
        """Make a bid."""
        rc = self.__get__(urls['fut']['PostBid'], params={'tradeIds': trade_id})['auctionInfo'][0]
        if rc['currentBid'] < bid and self.credits >= bid:
            data = {'bid': bid}
            url = '{0}/{1}/bid'.format(urls['fut']['PostBid'], trade_id)
            rc = self.__put__(url, data=json.dumps(data))['auctionInfo'][0]
        if rc['bidState'] == 'highest' or (rc['tradeState'] == 'closed' and rc['bidState'] == 'buyNow'):  # checking 'tradeState' is required?
        	return True
        else:
            return False

    def tradepile(self):
        """Returns items in tradepile."""
        rc = self.__get__(urls['fut']['TradePile'])
        # {"duplicateItemIdList":[{"itemId":106141947333,"duplicateItemId":105507948593},{"itemId":106089292920,"duplicateItemId":105507948593},{"itemId":105997261642,"duplicateItemId":105507948593},{"itemId":106437259823,"duplicateItemId":105507948593},{"itemId":105830172434,"duplicateItemId":105507048043}],"auctionInfo":[{"itemData":{"id":106101707703,"timestamp":1382982319,"itemType":"player","formation":"f4321","untradeable":false,"teamid":240,"resourceId":1610756481,"assetId":143745,"itemState":"free","rating":84,"preferredPosition":"LM","injuryGames":0,"statsList":[{"value":5,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"attributeList":[{"value":74,"index":0},{"value":75,"index":1},{"value":84,"index":2},{"value":88,"index":3},{"value":49,"index":4},{"value":70,"index":5}],"lifetimeStats":[{"value":38,"index":0},{"value":14,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"lastSalePrice":1800,"owners":5,"morale":50,"training":0,"injuryType":"shoulder","suspension":0,"fitness":99,"assists":0,"discardValue":672,"cardsubtypeid":2,"contract":16,"rareflag":1,"playStyle":259,"lifetimeAssists":8,"loyaltyBonus":0},"tradeId":137591211535,"startingBid":1800,"buyNowPrice":2200,"offers":0,"tradeState":"closed","watched":true,"bidState":"none","currentBid":1800,"expires":-1,"sellerName":"Bailen United","sellerEstablished":1288998842,"sellerId":0},{"itemData":{"id":106340770067,"timestamp":1383708120,"itemType":"player","formation":"f451","untradeable":false,"teamid":240,"resourceId":1610806483,"assetId":193747,"itemState":"free","rating":81,"preferredPosition":"CAM","injuryGames":0,"statsList":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"attributeList":[{"value":75,"index":0},{"value":72,"index":1},{"value":83,"index":2},{"value":81,"index":3},{"value":60,"index":4},{"value":62,"index":5}],"lifetimeStats":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"lastSalePrice":1900,"owners":4,"morale":50,"training":0,"injuryType":"none","suspension":0,"fitness":99,"assists":0,"discardValue":648,"cardsubtypeid":2,"contract":7,"rareflag":1,"playStyle":250,"lifetimeAssists":0,"loyaltyBonus":0},"tradeId":137604642922,"startingBid":1600,"buyNowPrice":1900,"offers":0,"tradeState":"closed","watched":true,"bidState":"none","currentBid":1900,"expires":-1,"sellerName":"Bailen United","sellerEstablished":1288998842,"sellerId":0},{"itemData":{"id":106341478475,"timestamp":1383712264,"itemType":"player","formation":"f4231","untradeable":false,"teamid":240,"resourceId":1610806483,"assetId":193747,"itemState":"free","rating":81,"preferredPosition":"CAM","injuryGames":0,"statsList":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"attributeList":[{"value":75,"index":0},{"value":72,"index":1},{"value":83,"index":2},{"value":81,"index":3},{"value":60,"index":4},{"value":62,"index":5}],"lifetimeStats":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"lastSalePrice":1900,"owners":4,"morale":50,"training":0,"injuryType":"none","suspension":0,"fitness":99,"assists":0,"discardValue":648,"cardsubtypeid":2,"contract":7,"rareflag":1,"playStyle":250,"lifetimeAssists":0,"loyaltyBonus":0},"tradeId":137604615652,"startingBid":1600,"buyNowPrice":1900,"offers":0,"tradeState":"closed","watched":true,"bidState":"none","currentBid":1900,"expires":-1,"sellerName":"Bailen United","sellerEstablished":1288998842,"sellerId":0},{"itemData":{"id":105997261642,"timestamp":1382675466,"itemType":"player","formation":"f442","untradeable":false,"teamid":240,"resourceId":1610806483,"assetId":193747,"itemState":"free","rating":81,"preferredPosition":"CAM","injuryGames":0,"statsList":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"attributeList":[{"value":75,"index":0},{"value":72,"index":1},{"value":83,"index":2},{"value":81,"index":3},{"value":60,"index":4},{"value":62,"index":5}],"lifetimeStats":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"lastSalePrice":1200,"owners":2,"morale":50,"training":0,"injuryType":"none","suspension":0,"fitness":99,"assists":0,"discardValue":648,"cardsubtypeid":2,"contract":7,"rareflag":1,"playStyle":250,"lifetimeAssists":0,"loyaltyBonus":0},"tradeId":137610216656,"startingBid":1600,"buyNowPrice":1900,"offers":0,"tradeState":"expired","watched":true,"bidState":"none","currentBid":0,"expires":-1,"sellerName":"Bailen United","sellerEstablished":1288998842,"sellerId":0},{"itemData":{"id":106089292920,"timestamp":1382950547,"itemType":"player","formation":"f4222","untradeable":false,"teamid":240,"resourceId":1610806483,"assetId":193747,"itemState":"free","rating":81,"preferredPosition":"CAM","injuryGames":0,"statsList":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"attributeList":[{"value":75,"index":0},{"value":72,"index":1},{"value":83,"index":2},{"value":81,"index":3},{"value":60,"index":4},{"value":62,"index":5}],"lifetimeStats":[{"value":2,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"lastSalePrice":850,"owners":7,"morale":50,"training":0,"injuryType":"none","suspension":0,"fitness":95,"assists":0,"discardValue":648,"cardsubtypeid":2,"contract":5,"rareflag":1,"playStyle":250,"lifetimeAssists":1,"loyaltyBonus":0},"tradeId":137610155304,"startingBid":1600,"buyNowPrice":1900,"offers":0,"tradeState":"expired","watched":true,"bidState":"none","currentBid":0,"expires":-1,"sellerName":"Bailen United","sellerEstablished":1288998842,"sellerId":0},{"itemData":{"id":105830172434,"timestamp":1382120299,"itemType":"player","formation":"f41212","untradeable":false,"teamid":240,"resourceId":1610756481,"assetId":143745,"itemState":"free","rating":84,"preferredPosition":"LM","injuryGames":0,"statsList":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"attributeList":[{"value":74,"index":0},{"value":75,"index":1},{"value":84,"index":2},{"value":88,"index":3},{"value":49,"index":4},{"value":70,"index":5}],"lifetimeStats":[{"value":10,"index":0},{"value":2,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"lastSalePrice":1200,"owners":6,"morale":50,"training":0,"injuryType":"foot","suspension":0,"fitness":90,"assists":0,"discardValue":672,"cardsubtypeid":2,"contract":11,"rareflag":1,"playStyle":250,"lifetimeAssists":0,"loyaltyBonus":0},"tradeId":0,"startingBid":0,"buyNowPrice":0,"offers":0,"tradeState":null,"watched":false,"bidState":null,"currentBid":0,"expires":0,"sellerName":null,"sellerEstablished":0,"sellerId":0},{"itemData":{"id":106141947333,"timestamp":1383150444,"itemType":"player","formation":"f4231","untradeable":false,"teamid":240,"resourceId":1610806483,"assetId":193747,"itemState":"free","rating":81,"preferredPosition":"CAM","injuryGames":0,"statsList":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"attributeList":[{"value":75,"index":0},{"value":72,"index":1},{"value":83,"index":2},{"value":81,"index":3},{"value":60,"index":4},{"value":62,"index":5}],"lifetimeStats":[{"value":28,"index":0},{"value":5,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"lastSalePrice":950,"owners":5,"morale":50,"training":0,"injuryType":"none","suspension":0,"fitness":76,"assists":0,"discardValue":648,"cardsubtypeid":2,"contract":0,"rareflag":1,"playStyle":250,"lifetimeAssists":13,"loyaltyBonus":0},"tradeId":0,"startingBid":0,"buyNowPrice":0,"offers":0,"tradeState":null,"watched":false,"bidState":null,"currentBid":0,"expires":0,"sellerName":null,"sellerEstablished":0,"sellerId":0},{"itemData":{"id":106437259823,"timestamp":1383952994,"itemType":"player","formation":"f41212","untradeable":false,"teamid":240,"resourceId":1610806483,"assetId":193747,"itemState":"free","rating":81,"preferredPosition":"CAM","injuryGames":0,"statsList":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"attributeList":[{"value":75,"index":0},{"value":72,"index":1},{"value":83,"index":2},{"value":81,"index":3},{"value":60,"index":4},{"value":62,"index":5}],"lifetimeStats":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"lastSalePrice":1000,"owners":3,"morale":50,"training":0,"injuryType":"none","suspension":0,"fitness":99,"assists":0,"discardValue":648,"cardsubtypeid":2,"contract":7,"rareflag":1,"playStyle":250,"lifetimeAssists":0,"loyaltyBonus":0},"tradeId":0,"startingBid":0,"buyNowPrice":0,"offers":0,"tradeState":null,"watched":false,"bidState":null,"currentBid":0,"expires":0,"sellerName":null,"sellerEstablished":0,"sellerId":0}],"currencies":null,"credits":32766,"bidTokens":{},"errorState":null}
        return [itemParse(i) for i in rc['auctionInfo']]

    def watchlist(self):
        """Returns items in watchlist."""
        rc = self.__get__(urls['fut']['WatchList'])
        # {"total":2,"duplicateItemIdList":[{"itemId":105967731721,"duplicateItemId":105507048043},{"itemId":105595815240,"duplicateItemId":105507948593}],"auctionInfo":[{"itemData":{"id":105967731721,"timestamp":1382568771,"itemType":"player","formation":"f343","untradeable":false,"teamid":240,"resourceId":1610756481,"assetId":143745,"itemState":"free","rating":84,"preferredPosition":"LM","injuryGames":0,"statsList":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"attributeList":[{"value":74,"index":0},{"value":75,"index":1},{"value":84,"index":2},{"value":88,"index":3},{"value":49,"index":4},{"value":70,"index":5}],"lifetimeStats":[{"value":16,"index":0},{"value":2,"index":1},{"value":1,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"lastSalePrice":1200,"owners":3,"morale":50,"training":0,"injuryType":"foot","suspension":0,"fitness":99,"assists":0,"discardValue":672,"cardsubtypeid":2,"contract":4,"rareflag":1,"playStyle":264,"lifetimeAssists":1,"loyaltyBonus":0},"tradeId":137610675201,"startingBid":1100,"buyNowPrice":0,"offers":0,"tradeState":"closed","watched":true,"bidState":"highest","currentBid":1200,"expires":-1,"sellerName":"us bag","sellerEstablished":1380674038,"sellerId":0},{"itemData":{"id":105595815240,"timestamp":1381356304,"itemType":"player","formation":"f532","untradeable":false,"teamid":240,"resourceId":1610806483,"assetId":193747,"itemState":"free","rating":81,"preferredPosition":"CAM","injuryGames":0,"statsList":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"attributeList":[{"value":75,"index":0},{"value":72,"index":1},{"value":83,"index":2},{"value":81,"index":3},{"value":60,"index":4},{"value":62,"index":5}],"lifetimeStats":[{"value":87,"index":0},{"value":30,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"lastSalePrice":1100,"owners":4,"morale":50,"training":0,"injuryType":"none","suspension":0,"fitness":99,"assists":0,"discardValue":648,"cardsubtypeid":2,"contract":30,"rareflag":1,"playStyle":253,"lifetimeAssists":19,"loyaltyBonus":0},"tradeId":137602662812,"startingBid":150,"buyNowPrice":0,"offers":0,"tradeState":"closed","watched":true,"bidState":"highest","currentBid":1100,"expires":-1,"sellerName":"castillofc","sellerEstablished":1292195112,"sellerId":0}],"credits":32766}
        return [itemParse(i) for i in rc['auctionInfo']]

    def unassigned(self):
        """Returns Unassigned items (i.e. buyNow items)."""
        rc = self.__get__(urls['fut']['Unassigned'])
        #{"itemData":[{"id":105131466631,"timestamp":1380285149,"itemType":"player","formation":"f4312","untradeable":false,"teamid":111674,"resourceId":1610823657,"assetId":210921,"itemState":"free","rating":53,"preferredPosition":"CB","injuryGames":0,"statsList":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"attributeList":[{"value":50,"index":0},{"value":27,"index":1},{"value":27,"index":2},{"value":28,"index":3},{"value":55,"index":4},{"value":59,"index":5}],"lifetimeStats":[{"value":0,"index":0},{"value":0,"index":1},{"value":0,"index":2},{"value":0,"index":3},{"value":0,"index":4}],"lastSalePrice":200,"owners":2,"morale":50,"training":0,"injuryType":"none","suspension":0,"fitness":99,"assists":0,"discardValue":16,"cardsubtypeid":1,"contract":7,"rareflag":0,"playStyle":250,"lifetimeAssists":0,"loyaltyBonus":0}]}
        print rc
        if len(rc['itemData']) > 0:
            return [auctionParse(i) for i in rc['itemData']]
        else:
            return []

#    def relistAll(self, item_id):
#        """Relist all items in trade pile."""
#        print(self.r.get(urls['fut']['Item']+'/%s' % item_id).text)

    def sell(self, item_id, bid, buy_now=0, duration=3600):
        """Starts auction. Returns trade_id."""
        data = {'buyNowPrice': buy_now, 'startingBid': bid, 'duration': duration, 'itemData':{'id': item_id}}
        rc = self.__post__(urls['fut']['SearchAuctionsListItem'], data=json.dumps(data))
        return rc['id']

    def watchlistDelete(self, trade_id):
        """Removes card from watchlist."""
        params = {'tradeId': trade_id}
        self.__delete__(urls['fut']['WatchList'], params=params)  # returns nothing
        return True

    def tradepileDelete(self, trade_id):
        """Removes card from tradepile."""
        url = '{}/{}'.format(urls['fut']['TradeInfo'], trade_id)
        self.__delete__(url)  # returns nothing
        return True

    def sendToTradepile(self, trade_id, item_id):
        """Sends to tradepile."""
        # TODO: accept multiple trade_ids (just extend list below (+ extend params?))
        if trade_id > 0 :
            # won item
            data = {"itemData": [{"tradeId": trade_id, "pile": "trade", "id": str(item_id)}]}
        else:
            # unassigned item
            data = {"itemData": [{"pile": "trade", "id": str(item_id)}]}

        rc = self.__put__(urls['fut']['Item'], data=json.dumps(data))
        return rc['itemData'][0]['success']

    def getCredits(self):
        """Get credits."""
        rc = self.__get__(urls['fut']['Credits'])
        return rc['credits']

    def keepalive(self):
        """
            keepalive ping.
            GET http://www.easports.com/fifa/football-club/keepalive
            response: OK
        """
        rc = self.__get__(urls['keepalive'])
        print rc
        return True
