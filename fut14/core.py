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

from .config import headers, headers_and, headers_ios
from .log import logger
from .urls import urls
from .exceptions import (Fut14Error, ExpiredSession, InternalServerError,
                         UnknownError, PermissionDenied, Conflict,
                         MultipleSession, FeatureDisabled)
from .EAHashingAlgorithm import EAHashingAlgorithm



def baseId(resource_id, version=False):
    """Calculates base id (assetId?)."""
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
            'tradeId':       item_data.get('tradeId'),
            'buyNowPrice':   item_data.get('buyNowPrice'),
            'tradeState':    item_data.get('tradeState'),
            'bidState':      item_data.get('bidState'),
            'startingBid':   item_data.get('startingBid'),
            'id':            item_data['itemData']['id'],
            'timestamp':     item_data['itemData']['timestamp'],  # auction start
            'rating':        item_data['itemData']['rating'],
            'assetId':       item_data['itemData']['assetId'],
            'resourceId':    item_data['itemData']['resourceId'],
            'itemState':     item_data['itemData']['itemState'],
            'rareflag':      item_data['itemData']['rareflag'],
            'formation':     item_data['itemData']['formation'],
            'leagueId':      item_data['itemData']['leagueId'],
            'injuryType':    item_data['itemData']['injuryType'],
            'injuryGames':   item_data['itemData']['injuryGames'],
            'lastSalePrice': item_data['itemData']['lastSalePrice'],
            'fitness':       item_data['itemData']['fitness'],
            'training':      item_data['itemData']['training'],
            'suspension':    item_data['itemData']['suspension'],
            'contract':      item_data['itemData']['contract'],
            #'position':      item_data['itemData']['preferredPosition'],
            'playStyle':     item_data['itemData'].get('playStyle'),  # used only for players
            'discardValue':  item_data['itemData']['discardValue'],
            'itemType':      item_data['itemData']['itemType'],
            'owners':        item_data['itemData']['owners'],
            'offers':        item_data.get('offers'),
            'currentBid':    item_data.get('currentBid'),
            'expires':       item_data.get('expires'),  # seconds left
            #'sellerEstablished': item_data.get('sellerEstablished'),
            #'sellerId':      item_data.get('sellerId'),
            #'sellerName':    item_data.get('sellerName'),
            #'watched':    item_data.get('watched'),
        }

'''  # different urls (platforms)
def cardInfo(resource_id):
    """Returns card info."""
    # TODO: add referer to headers (futweb)
    url = '{}{}.json'.format(self.urls['card_info'], baseId(resource_id))
    return requests.get(url).json()
'''


class Core(object):
    def __init__(self, email, passwd, secret_answer, platform='pc', emulate=None, debug=False):
        self.debug = debug
        if self.debug: self.logger = logger('DEBUG')
        # TODO: validate fut request response (200 OK)
        self.__login__(email, passwd, secret_answer, platform, emulate)

    def __login__(self, email, passwd, secret_answer, platform='pc', emulate=None):
        """Just log in."""
        # TODO: split into smaller methods
        secret_answer_hash = EAHashingAlgorithm().EAHash(secret_answer)
        self.credits = 0
        # create session
        self.r = requests.Session()  # init/reset requests session object
        if emulate == 'and':
            self.r.headers = headers_and.copy()  # i'm android now ;-)
        elif emulate == 'ios':
            self.r.headers = headers_ios.copy()  # i'm ios phone now ;-)
        else:
            self.r.headers = headers.copy()  # i'm chrome browser now ;-)
        self.urls = urls(platform)
        # emulate
        if emulate == 'ios':
            sku = 'FUT14IOS'
            clientVersion = 8
        elif emulate == 'and':
            sku = 'FUT14AND'
            clientVersion = 8
#        TODO: need more info about log in procedure in game
#        elif emulate == 'xbox':
#            sku = 'FFA14XBX'  # FFA14CAP ?
#            clientVersion = 1
#        elif emulate == 'ps3':
#            sku = 'FFA14PS3'  # FFA14KTL ?
#            clientVersion = 1
#        elif emulate == 'pc':
#            sku = ''  # dunno
#            clientVersion = 1
        elif not emulate:
            sku = 'FUT14WEB'
            clientVersion = 1
        else:
            raise Fut14Error('Invalid emulate parameter. (Valid ones are and/ios).')  # pc/ps3/xbox/
        # === login
        self.urls['login'] = self.r.get(self.urls['fut_home']).url
        self.r.headers['Referer'] = self.urls['main_site']  # prepare headers
        data = {'email': email,
                'password': passwd,
                '_rememberMe': 'on',
                'rememberMe': 'on',
                '_eventId': 'submit',
                'facebookAuth': ''}
        rc = self.r.post(self.urls['login'], data=data)
        if self.debug: self.logger.debug(rc.content)
        # TODO: catch invalid data exception
        #self.nucleus_id = re.search('userid : "([0-9]+)"', rc.text).group(1)  # we'll get it later

        # === lanuch futweb
        self.r.headers['Referer'] = self.urls['fut_home']  # prepare headers
        rc = self.r.get(self.urls['futweb'])
        if self.debug: self.logger.debug(rc.content)
        rc = rc.text
        if 'EASW_ID' not in rc:
            raise Fut14Error('Error during login process (probably invalid email or password).')
        self.nucleus_id = re.search("var EASW_ID = '([0-9]+)';", rc).group(1)
        #self.urls['fut_base'] = re.search("var BASE_FUT_URL = '(https://.+?)';", rc).group(1)
        #self.urls['fut_home'] = re.search("var GUEST_APP_URI = '(http://.+?)';", rc).group(1)

        # acc info
        self.r.headers.update({  # prepare headers
            'Content-Type': 'application/json',
            'Accept': 'text/json',
            'Easw-Session-Data-Nucleus-Id': self.nucleus_id,
            'X-UT-Embed-Error': 'true',
            'X-Requested-With': 'XMLHttpRequest',
            'X-UT-Route': self.urls['fut_host'],
            'Referer': self.urls['futweb'],
        })
        rc = self.r.get(self.urls['acc_info'])
        if self.debug: self.logger.debug(rc.content)
        rc = rc.json()['userAccountInfo']['personas'][0]
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
                'sku': sku,
                'clientVersion': clientVersion,
                'nuc': self.nucleus_id,
                'nucleusPersonaId': self.persona_id,
                'nucleusPersonaDisplayName': self.persona_name,
                'nucleusPersonaPlatform': platform,
                'locale': 'en-GB',
                'method': 'authcode',
                'priorityLevel': 4,
                'identification': {'AuthCode': ''}}
        rc = self.r.post(self.urls['fut']['authentication'], data=json.dumps(data))
        if self.debug: self.logger.debug(rc.content)
        if rc.status_code == 500:
            raise InternalServerError('Servers are probably temporary down.')
        rc = rc.json()
        #self.urls['fut_host'] = '{0}://{1}'.format(rc['protocol']+rc['ipPort'])
        if rc.get('reason') == 'multiple session':
            raise MultipleSession
        self.r.headers['X-UT-SID'] = self.sid = rc['sid']

        # validate (secret question)
        self.r.headers['Accept'] = 'text/json'  # prepare headers
        del self.r.headers['Origin']
        rc = self.r.get(self.urls['fut_question'])
        if self.debug: self.logger.debug(rc.content)
        rc = rc.json()
        if rc.get('string') != 'Already answered question.':
            # answer question
            data = {'answer': secret_answer_hash}
            self.r.headers['Content-Type'] = 'application/x-www-form-urlencoded'  # requests bug?
            rc = self.r.post(self.urls['fut_validate'], data=data)
            if self.debug: self.logger.debug(rc.content)
            rc = rc.json()
            if rc['string'] != 'OK':  # we've got error
                if 'Answers do not match' in rc['reason']:
                    raise Fut14Error('Error during login process (invalid secret answer).')
                else:
                    raise UnknownError
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

        # get basic user info
        # TODO: parse response (https://gist.github.com/oczkers/526577572c097eb8172f)
        self.__get__(self.urls['fut']['user'])
        # size of piles
        piles = self.pileSize()
        self.tradepile_size = piles['tradepile']
        self.watchlist_size = piles['watchlist']

#    def __shards__(self):
#        """Returns shards info."""
#        # TODO: headers
#        self.r.headers['X-UT-Route'] = self.urls['fut_base']
#        return self.r.get(self.urls['shards']).json()
#        # self.r.headers['X-UT-Route'] = self.urls['fut_pc']

    def __request__(self, method, url, *args, **kwargs):
        """Prepares headers and sends request. Returns response as a json object."""
        # TODO: update credtis?
        self.r.headers['X-HTTP-Method-Override'] = method.upper()
        rc = self.r.post(url, *args, **kwargs)
        if self.debug: self.logger.debug(rc.content)
        if not rc.ok:  # status != 200
            raise UnknownError(rc.content)
        if rc.text == '':
            self.keepalive()  # credits not avaible in response, manualy updating
            rc = {}
        else:
            rc = rc.json()
            # error control
            if 'code' and 'reason' in rc:  # error
                if rc['reason'] == 'expired session':
                    raise ExpiredSession
                elif rc.get('string') == 'Internal Server Error (ut)':
                    raise InternalServerError
                elif rc.get('string') == 'Permission Denied':
                    raise PermissionDenied
                elif rc.get('string') == 'Conflict':
                    raise Conflict
                elif rc.get('string') == 'Feature Disabled':
                    raise FeatureDisabled
                else:
                    raise UnknownError(rc.__str__())
            # update credits
            if 'credits' not in rc:
                self.keepalive()  # credits not avaible in response, manualy updating
            else:
                self.credits = rc['credits']
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

    def __sendToPile__(self, pile, trade_id, item_id=None):
        """Sends to pile."""
        # TODO: accept multiple trade_ids (just extend list below (+ extend params?))
        if pile == 'watchlist':
            params = {'tradeId': trade_id}
            data = {'auctionInfo': [{'id': trade_id}]}
            self.__put__(self.urls['fut']['WatchList'], params=params, data=json.dumps(data))
            return True

        if trade_id > 0:
            # won item
            data = {"itemData": [{"tradeId": trade_id, "pile": pile, "id": str(item_id)}]}
        else:
            # unassigned item
            data = {"itemData": [{"pile": pile, "id": str(item_id)}]}

        rc = self.__put__(self.urls['fut']['Item'], data=json.dumps(data))
        return rc['itemData'][0]['success']

    def baseId(self, *args, **kwargs):
        """Alias for baseId."""
        return baseId(*args, **kwargs)

    def cardInfo(self, resource_id):
        """Returns card info."""
        # TODO: add referer to headers (futweb)
        url = '{}{}.json'.format(self.urls['card_info'], baseId(resource_id))
        return requests.get(url).json()

    def searchAuctions(self, ctype, level=None, category=None, assetId=None,
                       min_price=None, max_price=None, min_buy=None, max_buy=None,
                       league=None, club=None, position=None, nationality=None,
                       playStyle=None, start=0, page_size=16):
        """Search specific items on transfer market."""
        # TODO: add "search" alias
        # TODO: generator
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
        if assetId:     params['maskedDefId'] = assetId
        if min_price:   params['micr'] = min_price
        if max_price:   params['macr'] = max_price
        if min_buy:     params['minb'] = min_buy
        if max_buy:     params['maxb'] = max_buy
        if league:      params['leag'] = league
        if club:        params['team'] = club
        if position:    params['pos'] = position
        if nationality: params['nat'] = nationality
        if playStyle:   params['playStyle'] = playStyle

        rc = self.__get__(self.urls['fut']['SearchAuctions'], params=params)
        return [itemParse(i) for i in rc['auctionInfo']]

    def bid(self, trade_id, bid):
        """Make a bid."""
        rc = self.__get__(self.urls['fut']['PostBid'], params={'tradeIds': trade_id})['auctionInfo'][0]
        if rc['currentBid'] < bid and self.credits >= bid:
            data = {'bid': bid}
            url = '{0}/{1}/bid'.format(self.urls['fut']['PostBid'], trade_id)
            rc = self.__put__(url, data=json.dumps(data))['auctionInfo'][0]
        if rc['bidState'] == 'highest' or (rc['tradeState'] == 'closed' and rc['bidState'] == 'buyNow'):  # checking 'tradeState' is required?
        	return True
        else:
            return False

    def club(self, count=10, level=10, type=1, start=0):
        """
            Returns items in your club, excluding consumables

            count - the number of cards you want to request
            level - Not quite sure, It always seems to be 10
            type - the type of card that you need:
                set to 1 for players
                set to 100 for staff
                set to 142 for club items
            start - position to start from
        """
        data = {'count': count, 'level': level, 'type': type, 'start': start}
        rc = self.__get__(self.urls['fut']['Club'], data=json.dumps(data))
        return [itemParse({'itemData': i}) for i in rc['itemData']]

    def squad(self, squad_num=0):
        """Return a squad."""
        url = '{}/{}'.format(self.urls['fut']['Squad'], squad_num)
        rc = self.__get__(url)
        return rc

    def tradepile(self):
        """Returns items in tradepile."""
        rc = self.__get__(self.urls['fut']['TradePile'])
        return [itemParse(i) for i in rc['auctionInfo']]

    def watchlist(self):
        """Returns items in watchlist."""
        rc = self.__get__(self.urls['fut']['WatchList'])
        return [itemParse(i) for i in rc['auctionInfo']]

    def unassigned(self):
        """Returns Unassigned items (i.e. buyNow items)."""
        rc = self.__get__(self.urls['fut']['Unassigned'])
        return [itemParse({'itemData': i}) for i in rc['itemData']]

    def sell(self, item_id, bid, buy_now=0, duration=3600):
        """Starts auction. Returns trade_id."""
        # TODO: auto send to tradepile
        data = {'buyNowPrice': buy_now, 'startingBid': bid, 'duration': duration, 'itemData':{'id': item_id}}
        rc = self.__post__(self.urls['fut']['SearchAuctionsListItem'], data=json.dumps(data))
        return rc['id']

    def quickSell(self, item_id):
        """Quick sell."""
        params = {'itemIds': item_id}
        self.__delete__(self.urls['fut']['Item'], params=params)  # returns nothing
        return True

    def watchlistDelete(self, trade_id):
        """Removes card from watchlist."""
        params = {'tradeId': trade_id}
        self.__delete__(self.urls['fut']['WatchList'], params=params)  # returns nothing
        return True

    def tradepileDelete(self, trade_id):
        """Removes card from tradepile."""
        url = '{}/{}'.format(self.urls['fut']['TradeInfo'], trade_id)
        self.__delete__(url)  # returns nothing
        return True

    def sendToTradepile(self, trade_id, item_id, safe=True):
        """Sends to tradepile (alias for __sendToPile__)."""
        if safe and len(self.tradepile()) >= self.tradepile_size:  # TODO?: optimization (don't parse items in tradepile)
            return False
        return self.__sendToPile__('trade', trade_id, item_id)

    def sendToClub(self, trade_id, item_id):
        """Sends to club (alias for __sendToPile__)."""
        return self.__sendToPile__('club', trade_id, item_id)

    def sendToWatchlist(self, trade_id):
        """Sends to watchlist."""
        return self.__sendToPile__('watchlist', trade_id)

    def relist(self, clean=False):
        """Relist all tradepile. Returns True or number of deleted (sold) if clean was set."""
        # TODO: return relisted ids
        self.__put__(self.urls['fut']['SearchAuctionsReListItem'])
        #{"tradeIdList":[{"id":139632781208},{"id":139632796467}]}
        if clean:  # remove sold cards
            sold = 0
            for i in self.tradepile():
                if i['tradeState'] == 'closed':
                    self.tradepileDelete(i['tradeId'])
                    sold += 1
            return sold
        return True

    def keepalive(self):
        """Just refresh credit amount to let know that we're still online. Returns credit amount."""
        return self.__get__(self.urls['fut']['Credits'])

    def pileSize(self):
        """Returns size of tradepile and watchlist."""
        rc = self.__get__(self.urls['fut']['PileSize'])['entries']
        return {'tradepile': rc[0]['value'],
                'watchlist': rc[2]['value']}

    def stats(self):
        """Returns all stats."""
        # won-draw-loss
        rc = self.__get__(self.urls['fut']['user'])
        data = {
            'won': rc['won'],
            'draw': rc['draw'],
            'loss': rc['loss'],
            'matchUnfinishedTime': rc['reliability']['matchUnfinishedTime'],
            'finishedMatches': rc['reliability']['finishedMatches'],
            'reliability': rc['reliability']['reliability'],
            'startedMatches': rc['reliability']['startedMatches'],
        }
        # leaderboard
        url = '{}/alltime/user/{}'.format(self.urls['fut']['LeaderboardEntry'], self.persona_id)
        rc = self.__get__(url)
        data.update({
            'earnings': rc['category'][0]['score']['value'],   #competitor
            'transfer': rc['category'][1]['score']['value'],   #trader
            'club_value': rc['category'][2]['score']['value'], #collector
            'top_squad': rc['category'][3]['score']['value']   #builder
            })
        return data

    def clubInfo(self):
        """Returns getReliability"""
        # TODO?: return specific club
        rc = self.__get__(self.urls['fut']['user'])
        return {
            'personaName': rc['personaName'],
            'clubName': rc['clubName'],
            'clubAbbr': rc['clubAbbr'],
            'established': rc['established'],
            'divisionOffline': rc['divisionOffline'],
            'divisionOnline': rc['divisionOnline'],
            'trophies': rc['trophies'],
            'seasonTicket': rc['seasonTicket']
        }
