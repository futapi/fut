# -*- coding: utf-8 -*-

"""
fut.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut's basic methods.

"""

import requests
import re
from time import time
try:
    from cookielib import LWPCookieJar
except ImportError:
    from http.cookiejar import LWPCookieJar
try:
    import simplejson as json
except ImportError:
    import json

from .config import headers, headers_and, headers_ios, flash_agent, cookies_file, timeout
from .log import logger
from .urls import urls
from .exceptions import (FutError, ExpiredSession, InternalServerError,
                         UnknownError, PermissionDenied, Captcha,
                         Conflict, MaxSessions, MultipleSession,
                         FeatureDisabled, doLoginFail, NoUltimateTeam)
from .EAHashingAlgorithm import EAHashingAlgorithm


def baseId(resource_id, return_version=False):
    """Calculate base id and version from a resource id.

    :params resource_id: Resource id.
    :params return_version: (optional) True if You need version, returns (resource_id, version).
    """
    version = 0
    resource_id = abs(resource_id)

    while resource_id > 0x01000000:  # 16777216
        version += 1
        if version == 1:
            resource_id -= 0x80000000  # 2147483648
        elif version == 2:
            resource_id -= 0x03000000  # 50331648
        else:
            resource_id -= 0x01000000  # 16777216
        resource_id = abs(resource_id)

    if return_version:
        return resource_id, version

    return resource_id


def itemParse(item_data, full=True):
    """Parser for item data. Returns nice dictionary.

    :params iteam_data: Item data received from ea servers.
    :params full: (optional) False if You're snipping and don't need extended info.
    """
    # TODO: object
    # TODO: parse all data
    return_data = {
        'tradeId':           item_data.get('tradeId'),
        'buyNowPrice':       item_data.get('buyNowPrice'),
        'tradeState':        item_data.get('tradeState'),
        'bidState':          item_data.get('bidState'),
        'startingBid':       item_data.get('startingBid'),
        'id':                item_data['itemData']['id'],
        'offers':            item_data.get('offers'),
        'currentBid':        item_data.get('currentBid'),
        'expires':           item_data.get('expires'),  # seconds left
        'sellerEstablished': item_data.get('sellerEstablished'),
        'sellerId':          item_data.get('sellerId'),
        'sellerName':        item_data.get('sellerName'),
        'watched':           item_data.get('watched'),
    }
    if full:
        return_data.update({
            'timestamp':     item_data['itemData'].get('timestamp'),  # auction start
            'rating':        item_data['itemData'].get('rating'),
            'assetId':       item_data['itemData'].get('assetId'),
            'resourceId':    item_data['itemData'].get('resourceId'),
            'itemState':     item_data['itemData'].get('itemState'),
            'rareflag':      item_data['itemData'].get('rareflag'),
            'formation':     item_data['itemData'].get('formation'),
            'leagueId':      item_data['itemData'].get('leagueId'),
            'injuryType':    item_data['itemData'].get('injuryType'),
            'injuryGames':   item_data['itemData'].get('injuryGames'),
            'lastSalePrice': item_data['itemData'].get('lastSalePrice'),
            'fitness':       item_data['itemData'].get('fitness'),
            'training':      item_data['itemData'].get('training'),
            'suspension':    item_data['itemData'].get('suspension'),
            'contract':      item_data['itemData'].get('contract'),
            # 'position':     item_data['itemData']['preferredPosition'],
            'playStyle':     item_data['itemData'].get('playStyle'),  # used only for players
            'discardValue':  item_data['itemData'].get('discardValue'),
            'itemType':      item_data['itemData'].get('itemType'),
            'cardType':      item_data['itemData'].get("cardsubtypeid"),  # used only for cards
            'owners':        item_data['itemData'].get('owners'),
        })
    return return_data


'''  # different urls (platforms)
def cardInfo(resource_id):
    """Return card info."""
    # TODO: add referer to headers (futweb)
    url = '{0}{1}.json'.format(self.urls['card_info'], baseId(resource_id))
    return requests.get(url, timeout=timeout).json()
'''


# TODO: optimize messages, xml parser might be faster
def nations(timeout=timeout):
    """Return all nations in dict {id0: nation0, id1: nation1}.

    :params year: Year.
    """
    rc = requests.get(urls('pc')['messages'], timeout=timeout).text
    data = re.findall('<trans-unit resname="search.nationName.nation([0-9]+)">\n        <source>(.+)</source>', rc)
    nations = {}
    for i in data:
        nations[int(i[0])] = i[1]
    return nations


def leagues(year=2017, timeout=timeout):
    """Return all leagues in dict {id0: league0, id1: legaue1}.

    :params year: Year.
    """
    rc = requests.get(urls('pc')['messages'], timeout=timeout).text
    data = re.findall('<trans-unit resname="global.leagueFull.%s.league([0-9]+)">\n        <source>(.+)</source>' % year, rc)
    leagues = {}
    for i in data:
        leagues[int(i[0])] = i[1]
    return leagues


def teams(year=2017, timeout=timeout):
    """Return all teams in dict {id0: team0, id1: team1}.

    :params year: Year.
    """
    rc = requests.get(urls('pc')['messages'], timeout=timeout).text
    data = re.findall('<trans-unit resname="global.teamFull.%s.team([0-9]+)">\n        <source>(.+)</source>' % year, rc)
    teams = {}
    for i in data:
        teams[int(i[0])] = i[1]
    return teams


class Core(object):
    def __init__(self, email, passwd, secret_answer, platform='pc', code=None, emulate=None, debug=False, cookies=cookies_file, timeout=timeout):
        self.credits = 0
        self.cookies_file = cookies  # TODO: map self.cookies to requests.Session.cookies?
        self.timeout = timeout
        if debug:  # save full log to file (fut.log)
            self.logger = logger(save=True)
        else:  # NullHandler
            self.logger = logger()
        # TODO: validate fut request response (200 OK)
        self.__login__(email, passwd, secret_answer, platform, code, emulate)

    def __login__(self, email, passwd, secret_answer, platform='pc', code=None, emulate=None):
        """Log in.

        :params email: Email.
        :params passwd: Password.
        :params secret_answer: Answer for secret question.
        :params platform: (optional) [pc/xbox/xbox360/ps3/ps4] Platform.
        :params code: (optional) Security code generated in origin or send via mail/sms.
        :params emulate: (optional) [and/ios] Emulate mobile device.
        """
        # TODO: split into smaller methods
        # TODO: check first if login is needed (https://www.easports.com/fifa/api/isUserLoggedIn)
        # TODO: get gamesku, url from shards !!
        self.emulate = emulate
        secret_answer_hash = EAHashingAlgorithm().EAHash(secret_answer)
        # create session
        self.r = requests.Session()  # init/reset requests session object
        # load saved cookies/session
        if self.cookies_file:
            self.r.cookies = LWPCookieJar(self.cookies_file)
            try:
                self.r.cookies.load(ignore_discard=True)  # is it good idea to load discarded cookies after long time?
            except IOError:
                pass
                # self.r.cookies.save(ignore_discard=True)  # create empty file for cookies
        if emulate == 'and':
            self.r.headers = headers_and.copy()  # i'm android now ;-)
        elif emulate == 'ios':
            self.r.headers = headers_ios.copy()  # i'm ios phone now ;-)
        else:
            self.r.headers = headers.copy()  # i'm chrome browser now ;-)
        self.urls = urls(platform)
        # TODO: urls won't be loaded if we drop here
        if platform == 'pc':
            game_sku = 'FFA17PCC'
        elif platform == 'xbox':
            game_sku = 'FFA17XBO'
        elif platform == 'xbox360':
            game_sku = 'FFA17XBX'
        elif platform == 'ps3':
            game_sku = 'FFA17PS3'  # not tested
        elif platform == 'ps4':
            game_sku = 'FFA17PS4'
            platform = 'ps3'  # ps4 not available?
        else:
            raise FutError(reason='Wrong platform. (Valid ones are pc/xbox/xbox360/ps3/ps4)')
        # if self.r.get(self.urls['main_site']+'/fifa/api/isUserLoggedIn', timeout=timeout).json()['isLoggedIn']:
        #    return True  # no need to log in again
        # emulate
        if emulate == 'ios':
            sku = 'FUT17IOS'
            clientVersion = 21
        elif emulate == 'and':
            sku = 'FUT17AND'
            clientVersion = 21
#        TODO: need more info about log in procedure in game
#        elif emulate == 'xbox':
#            sku = 'FFA16XBX'  # FFA14CAP ?
#            clientVersion = 1
#        elif emulate == 'ps3':
#            sku = 'FFA16PS3'  # FFA14KTL ?
#            clientVersion = 1
#        elif emulate == 'pc':
#            sku = ''  # dunno
#            clientVersion = 1
        elif not emulate:
            sku = 'FUT17WEB'
            clientVersion = 1
        else:
            raise FutError(reason='Invalid emulate parameter. (Valid ones are and/ios).')  # pc/ps3/xbox/
        # === login
        self.urls['login'] = self.r.get(self.urls['fut_home'], timeout=timeout).url
        self.r.headers['Referer'] = self.urls['login']  # prepare headers
        data = {'email': email,
                'password': passwd,
                '_rememberMe': 'on',
                'rememberMe': 'on',
                '_eventId': 'submit'}
        rc = self.r.post(self.urls['login'], data=data, timeout=self.timeout)
        self.logger.debug(rc.content)

        '''  # pops out only on first launch
        if 'FIFA Ultimate Team</strong> needs to update your Account to help protect your gameplay experience.' in rc.text:  # request email/sms code
            self.r.headers['Referer'] = rc.url  # s2
            rc = self.r.post(rc.url.replace('s2', 's3'), {'_eventId': 'submit'}, timeout=self.timeout).content
            self.r.headers['Referer'] = rc.url  # s3
            rc = self.r.post(rc.url, {'twofactorType': 'EMAIL', 'country': 0, 'phoneNumber': '', '_eventId': 'submit'}, timeout=self.timeout)
        '''
        if 'We sent a security code to your' in rc.text or 'Your security code was sent to' in rc.text or 'Enter the 6-digit verification code' in rc.text:  # post code
            # TODO: 'We sent a security code to your email' / 'We sent a security code to your ?'
            # TODO: pick code from codes.txt?
            if not code:
                self.saveSession()
                raise FutError(reason='Error during login process - code is required.')
            self.r.headers['Referer'] = url = rc.url
            # self.r.headers['Upgrade-Insecure-Requests'] = 1  # ?
            # self.r.headers['Origin'] = 'https://signin.ea.com'
            rc = self.r.post(url, {'twofactorCode': code, '_trustThisDevice': 'on', 'trustThisDevice': 'on', '_eventId': 'submit'}, timeout=self.timeout).text
            if 'Incorrect code entered' in rc or 'Please enter a valid security code' in rc:
                raise FutError(reason='Error during login process - provided code is incorrect.')
            self.logger.debug(rc)
            if 'Set Up an App Authenticator' in rc:
                rc = self.r.post(url.replace('s2', 's3'), {'_eventId': 'cancel', 'appDevice': 'IPHONE'}, timeout=self.timeout).text
            self.logger.debug(rc)

        self.r.headers['Referer'] = self.urls['login']
        if self.r.get(self.urls['main_site'] + '/fifa/api/isUserLoggedIn', timeout=self.timeout).json()['isLoggedIn'] is not True:  # TODO: parse error?
            raise FutError(reason='Error during login process (probably invalid email, password or code).')
        # TODO: catch invalid data exception
        # self.nucleus_id = re.search('userid : "([0-9]+)"', rc.text).group(1)  # we'll get it later

        # === lanuch futweb
        self.r.headers['Referer'] = self.urls['fut_home']  # prepare headers
        rc = self.r.get(self.urls['futweb'], timeout=self.timeout)
        self.logger.debug(rc.content)
        rc = rc.text
#        if 'EASW_ID' not in rc:
#            raise FutError(reason='Error during login process (probably invalid email or password).')
        self.nucleus_id = re.search("var EASW_ID = '([0-9]+)';", rc).group(1)
        self.build_cl = re.search("var BUILD_CL = '([0-9]+)';", rc).group(1)
        # self.urls['fut_base'] = re.search("var BASE_FUT_URL = '(https://.+?)';", rc).group(1)
        # self.urls['fut_home'] = re.search("var GUEST_APP_URI = '(http://.+?)';", rc).group(1)

        self.urls = urls(platform, self.build_cl)

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
        rc = self.r.get(self.urls['acc_info'], params={'_': int(time() * 1000)}, timeout=self.timeout)
        self.logger.debug(rc.content)
        # pick persona (first valid for given game_sku)
        personas = rc.json()['userAccountInfo']['personas']
        for p in personas:
            # self.clubs = [i for i in p['userClubList']]
            # sort clubs by lastAccessTime (latest first)
            # self.clubs.sort(key=lambda i: i['lastAccessTime'], reverse=True)
            for c in p['userClubList']:
                if c['skuAccessList'] and game_sku in c['skuAccessList']:
                    self.persona_id = p['personaId']
                    self.persona_name = p['personaName']
                    break

        # authorization
        self.r.headers.update({  # prepare headers
            'Accept': 'application/json, text/javascript',
            'Origin': 'http://www.easports.com',
        })
        data = {'isReadOnly': False,
                'sku': sku,
                'clientVersion': clientVersion,
                # 'nuc': self.nucleus_id,
                'nucleusPersonaId': self.persona_id,
                'nucleusPersonaDisplayName': self.persona_name,
                'gameSku': game_sku,
                'nucleusPersonaPlatform': platform,
                'locale': 'en-GB',
                'method': 'authcode',
                'priorityLevel': 4,
                'identification': {'AuthCode': ''}}
        rc = self.r.post(self.urls['fut']['authentication'], data=json.dumps(data), timeout=self.timeout)
        self.logger.debug(rc.content)
        if rc.status_code == 500:
            raise InternalServerError('Servers are probably temporary down.')
        rc = rc.json()
        # self.urls['fut_host'] = '{0}://{1}'.format(rc['protocol']+rc['ipPort'])
        if rc.get('reason') == 'multiple session':
            raise MultipleSession
        elif rc.get('reason') == 'max sessions':
            raise MaxSessions
        elif rc.get('reason') == 'doLogin: doLogin failed':
            raise doLoginFail
        elif rc.get('reason'):
            raise UnknownError(rc.__str__())
        self.r.headers['X-UT-SID'] = self.sid = rc['sid']

        # validate (secret question)
        self.r.headers['Accept'] = 'text/json'  # prepare headers
        del self.r.headers['Origin']
        rc = self.r.get(self.urls['fut_question'], params={'_': int(time() * 1000)}, timeout=self.timeout)
        self.logger.debug(rc.content)
        rc = rc.json()
        if rc.get('string') != 'Already answered question.':
            # answer question
            data = {'answer': secret_answer_hash}
            self.r.headers['Content-Type'] = 'application/x-www-form-urlencoded'  # requests bug?
            rc = self.r.post(self.urls['fut_validate'], data=data, timeout=self.timeout)
            self.logger.debug(rc.content)
            rc = rc.json()
            if rc['string'] != 'OK':  # we've got error
                if 'Answers do not match' in rc['reason']:
                    raise FutError(reason='Error during login process (invalid secret answer).')
                else:
                    raise UnknownError
            self.r.headers['Content-Type'] = 'application/json'
        self.r.headers['X-UT-PHISHING-TOKEN'] = self.token = rc['token']

        # prepare headers for ut operations
        del self.r.headers['Easw-Session-Data-Nucleus-Id']
        del self.r.headers['X-Requested-With']
        del self.r.headers['X-UT-Route']
        self.r.headers.update({
            # 'X-HTTP-Method-Override': 'GET',  # __request__ method manages this
            'X-Requested-With': flash_agent,
            'Referer': 'https://www.easports.com/iframe/fut16/bundles/futweb/web/flash/FifaUltimateTeam.swf',
            'Origin': 'https://www.easports.com',
            # 'Content-Type': 'application/json',  # already set
            'Accept': 'application/json',
        })

        # get basic user info
        # TODO: parse response (https://gist.github.com/oczkers/526577572c097eb8172f)
        self.__get__(self.urls['fut']['user'])
        # size of piles
        piles = self.pileSize()
        self.tradepile_size = piles['tradepile']
        self.watchlist_size = piles['watchlist']

        self.saveSession()

#    def __shards__(self):
#        """Returns shards info."""
#        # TODO: headers
#        self.r.headers['X-UT-Route'] = self.urls['fut_base']
#        return self.r.get(self.urls['shards'], params={'_': int(time()*1000)}, timeout=self.timeout).json()
#        # self.r.headers['X-UT-Route'] = self.urls['fut_pc']

    def __request__(self, method, url, *args, **kwargs):
        """Prepare headers and sends request. Returns response as a json object.

        :params method: Rest method.
        :params url: Url.
        """
        # TODO: update credtis?
        self.r.headers['X-HTTP-Method-Override'] = method.upper()
        self.logger.debug("request: {0} args={1};  kwargs={2}".format(url, args, kwargs))
        rc = self.r.post(url, timeout=self.timeout, *args, **kwargs)
        self.logger.debug("response: {0}".format(rc.content))
        if not rc.ok:  # status != 200
            raise UnknownError(rc.content)
        if rc.text == '':
            rc = {}
        else:
            captcha_token = rc.headers.get('Proxy-Authorization', '').replace('captcha=', '')  # captcha token (always AAAA ?)
            rc = rc.json()
            # error control
            if 'code' and 'reason' in rc:  # error
                err_code = rc['code']
                err_reason = rc['reason']
                err_string = rc.get('string')  # "human readable" reason?
                if err_reason == 'expired session':  # code?
                    raise ExpiredSession(err_code, err_reason, err_string)
                elif err_code == '500' or err_string == 'Internal Server Error (ut)':
                    raise InternalServerError(err_code, err_reason, err_string)
                elif err_code == '489' or err_string == 'Feature Disabled':
                    raise FeatureDisabled(err_code, err_reason, err_string)
                elif err_code == '465' or err_string == 'No User':
                    raise NoUltimateTeam(err_code, err_reason, err_string)
                elif err_code == '461' or err_string == 'Permission Denied':
                    raise PermissionDenied(err_code, err_reason, err_string)
                elif err_code == '459' or err_string == 'Captcha Triggered':
                    # img = self.r.get(self.urls['fut_captcha_img'], params={'_': int(time()*1000), 'token': captcha_token}, timeout=self.timeout).content  # doesnt work - check headers
                    img = None
                    raise Captcha(err_code, err_reason, err_string, captcha_token, img)
                elif err_code == '409' or err_string == 'Conflict':
                    raise Conflict(err_code, err_reason, err_string)
                else:
                    raise UnknownError(rc.__str__())
            if 'credits' in rc and rc['credits']:
                self.credits = rc['credits']
        self.saveSession()
        return rc

    def __get__(self, url, *args, **kwargs):
        """Send get request. Return response as a json object."""
        return self.__request__('GET', url, *args, **kwargs)

    def __post__(self, url, *args, **kwargs):
        """Send post request. Return response as a json object."""
        return self.__request__('POST', url, *args, **kwargs)

    def __put__(self, url, *args, **kwargs):
        """Send put request. Return response as a json object."""
        return self.__request__('PUT', url, *args, **kwargs)

    def __delete__(self, url, *args, **kwargs):
        """Send delete request. Return response as a json object."""
        return self.__request__('DELETE', url, *args, **kwargs)

    def __sendToPile__(self, pile, trade_id, item_id=None):
        """Send to pile.

        :params trade_id: Trade id.
        :params item_id: (optional) Iteam id.
        """
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
        if rc['itemData'][0]['success']:
            self.logger.info("{0} (itemId: {1}) moved to {2} Pile".format(trade_id, item_id, pile))
        else:
            self.logger.error("{0} (itemId: {1}) NOT MOVED to {2} Pile. REASON: {3}".format(trade_id, item_id, pile, rc['itemData'][0]['reason']))
        return rc['itemData'][0]['success']

    def logout(self, save=True):
        """Log out nicely (like clicking on logout button).

        :params save: False if You don't want to save cookies.
        """
        self.r.get('https://www.easports.com/fifa/logout', timeout=self.timeout)
        if save:
            self.saveSession()
        return True

    # TODO: probably there is no need to refresh on every call?
    @property
    def nations(self):
        """Return all nations in dict {id0: nation0, id1: nation1}.

        :params year: Year.
        """
        return nations()

    @property
    def leagues(self, year=2017):
        """Return all leagues in dict {id0: league0, id1: league1}.

        :params year: Year.
        """
        return leagues(year)

    @property
    def teams(self, year=2017):
        """Return all teams in dict {id0: team0, id1: team1}.

        :params year: Year.
        """
        return teams(year)

    def saveSession(self):
        """Save cookies/session."""
        if self.cookies_file:
            self.r.cookies.save(ignore_discard=True)

    def baseId(self, *args, **kwargs):
        """Calculate base id and version from a resource id."""
        return baseId(*args, **kwargs)

    def cardInfo(self, resource_id):
        """Return card info.

        :params resource_id: Resource id.
        """
        # TODO: add referer to headers (futweb)
        url = '{0}{1}.json'.format(self.urls['card_info'], baseId(resource_id))
        return requests.get(url, timeout=self.timeout).json()

    def searchDefinition(self, asset_id, start=0, count=35):
        """Return variations of the given asset id, e.g. IF cards.

        :param asset_id: Asset id / Definition id.
        :param start: (optional) Start page.
        :param count: (optional) Number of definitions you want to request.
        """
        params = {
            'defId': asset_id,
            'start': start,
            'type': 'player',
            'count': count
        }

        rc = self.__get__(self.urls['fut']['Search'], params=params)
        try:
            return rc['itemData']
        except:
            raise UnknownError('Invalid definition response')
        return rc

    def searchAuctions(self, ctype, level=None, category=None, assetId=None, defId=None,
                       min_price=None, max_price=None, min_buy=None, max_buy=None,
                       league=None, club=None, position=None, nationality=None,
                       playStyle=None, start=0, page_size=16):
        """Prepare search request, send and return parsed data as a dict.

        :param ctype: [development / ? / ?] Card type.
        :param level: (optional) [?/?/gold] Card level.
        :param category: (optional) [fitness/?/?] Card category.
        :param assetId: (optional) Asset id.
        :param defId: (optional) Definition id.
        :param min_price: (optional) Minimal price.
        :param max_price: (optional) Maximum price.
        :param min_buy: (optional) Minimal buy now price.
        :param max_buy: (optional) Maximum buy now price.
        :param league: (optional) League id.
        :param club: (optional) Club id.
        :param position: (optional) Position.
        :param nationality: (optional) Natiion id.
        :param playStyle: (optional) Play style.
        :param start: (optional) Start page.
        :param page_size: (optional) Page size (items per page).
        """
        # TODO: add "search" alias
        # TODO: generator
        if start > 0 and page_size == 16:
            if not self.emulate:  # wbeapp
                page_size = 12
                if start == 16:  # second page
                    start = 12
            elif self.emulate and start == 16:  # emulating android/ios
                start = 15
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
        if defId:       params['definitionId'] = defId
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
        """Make a bid.

        :params trade_id: Trade id.
        :params bid: Amount of credits You want to spend.
        """
        rc = self.tradeStatus(trade_id)[0]
        if rc['currentBid'] < bid and self.credits >= bid:
            data = {'bid': bid}
            url = '{0}/{1}/bid'.format(self.urls['fut']['PostBid'], trade_id)
            rc = self.__put__(url, data=json.dumps(data))['auctionInfo'][0]
        if rc['bidState'] == 'highest' or (rc['tradeState'] == 'closed' and rc['bidState'] == 'buyNow'):  # checking 'tradeState' is required?
            return True
        else:
            return False

    def club(self, count=10, level=10, type=1, start=0):
        """Return items in your club, excluding consumables.

        :params count: (optional) Number of cards You want to request (Default: 10).
        :params level: (optional) 10 = all | 3 = gold | 2 = silver | 1 = bronze (Default: 10).
        :params type: (optional) 1 = players | 100 = staff | 142 = club items (Default: 1).
        :params start: (optional) Position to start from (Default: 0).
        """
        params = {'count': count, 'level': level, 'type': type, 'start': start}
        rc = self.__get__(self.urls['fut']['Club'], params=params)
        return [itemParse({'itemData': i}) for i in rc['itemData']]

    def squad(self, squad_id=0):
        """Return a squad.

        :params squad_id: Squad id.
        """
        # TODO: ability to return other info than players only
        url = '{0}/{1}'.format(self.urls['fut']['Squad'], squad_id)
        rc = self.__get__(url)
        # return rc
        return [itemParse(i) for i in rc['players']]

    '''
    def squads(self):
        """Return squads list."""
        # TODO: ability to get full squad info (full=True)
        return self.squad(squad_id='list')
    '''

    def tradeStatus(self, trade_id):
        """Return trade status.

        :params trade_id: Trade id.
        """
        if not isinstance(trade_id, (list, tuple)):
            trade_id = (trade_id,)
        trade_id = (str(i) for i in trade_id)
        params = {'itemdata': 'true', 'tradeIds': ','.join(trade_id)}
        rc = self.__get__(self.urls['fut']['TradeStatus'], params=params)
        return [itemParse(i, full=False) for i in rc['auctionInfo']]

    def tradepile(self):
        """Return items in tradepile."""
        rc = self.__get__(self.urls['fut']['TradePile'])
        return [itemParse(i) for i in rc['auctionInfo']]

    def watchlist(self):
        """Return items in watchlist."""
        rc = self.__get__(self.urls['fut']['WatchList'])
        return [itemParse(i) for i in rc['auctionInfo']]

    def unassigned(self):
        """Return Unassigned items (i.e. buyNow items)."""
        rc = self.__get__(self.urls['fut']['Unassigned'])
        return [itemParse({'itemData': i}) for i in rc['itemData']]

    def sell(self, item_id, bid, buy_now=0, duration=3600):
        """Start auction. Returns trade_id.

        :params item_id: Item id.
        :params bid: Stard bid.
        :params buy_now: Buy now price.
        :params duration: Auction duration in seconds (Default: 3600).
        """
        # TODO: auto send to tradepile
        data = {'buyNowPrice': buy_now, 'startingBid': bid, 'duration': duration, 'itemData': {'id': item_id}}
        rc = self.__post__(self.urls['fut']['SearchAuctionsListItem'], data=json.dumps(data))
        return rc['id']

    def quickSell(self, item_id):
        """Quick sell.

        :params item_id: Item id.
        """
        if not isinstance(item_id, (list, tuple)):
            item_id = (item_id,)
        item_id = (str(i) for i in item_id)
        params = {'itemIds': ','.join(item_id)}
        self.__delete__(self.urls['fut']['Item'], params=params)  # returns nothing
        return True

    def watchlistDelete(self, trade_id):
        """Remove cards from watchlist.

        :params trade_id: Trade id.
        """
        if not isinstance(trade_id, (list, tuple)):
            trade_id = (trade_id,)
        trade_id = (str(i) for i in trade_id)
        params = {'tradeId': ','.join(trade_id)}
        self.__delete__(self.urls['fut']['WatchList'], params=params)  # returns nothing
        return True

    def tradepileDelete(self, trade_id):
        """Remove card from tradepile.

        :params trade_id: Trade id.
        """
        url = '{0}/{1}'.format(self.urls['fut']['TradeInfo'], trade_id)
        self.__delete__(url)  # returns nothing
        return True

    def sendToTradepile(self, trade_id, item_id, safe=True):
        """Send to tradepile (alias for __sendToPile__).

        :params trade_id: Trade id.
        :params item_id: Item id.
        :params safe: (optional) False to disable tradepile free space check.
        """
        if safe and len(self.tradepile()) >= self.tradepile_size:  # TODO?: optimization (don't parse items in tradepile)
            return False
        return self.__sendToPile__('trade', trade_id, item_id)

    def sendToClub(self, trade_id, item_id):
        """Send to club (alias for __sendToPile__).

        :params trade_id: Trade id.
        :params item_id: Item id.
        """
        return self.__sendToPile__('club', trade_id, item_id)

    def sendToWatchlist(self, trade_id):
        """Send to watchlist.

        :params trade_id: Trade id.
        """
        return self.__sendToPile__('watchlist', trade_id)

    def relist(self, clean=False):
        """Relist all tradepile. Returns True or number of deleted (sold) if clean was set.

        :params clean: (optional) True if You want to purge pile from sold cards.
        """
        # TODO: return relisted ids
        self.__put__(self.urls['fut']['SearchAuctionsReListItem'])
        # {"tradeIdList":[{"id":139632781208},{"id":139632796467}]}
        if clean:  # remove sold cards
            sold = 0
            for i in self.tradepile():
                if i['tradeState'] == 'closed':
                    self.tradepileDelete(i['tradeId'])
                    sold += 1
            return sold
        return True

    def keepalive(self):
        """Refresh credit amount to let know that we're still online. Returns credit amount."""
        return self.__get__(self.urls['fut']['Credits'])['credits']

    def pileSize(self):
        """Return size of tradepile and watchlist."""
        rc = self.__get__(self.urls['fut']['PileSize'])['entries']
        return {'tradepile': rc[0]['value'],
                'watchlist': rc[2]['value']}

    def stats(self):
        """Return all stats."""
        # TODO: add self.urls['fut']['Stats']
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
        url = '{0}/alltime/user/{1}'.format(self.urls['fut']['LeaderboardEntry'], self.persona_id)
        rc = self.__get__(url)
        data.update({
            'earnings': rc['category'][0]['score']['value'],    # competitor
            'transfer': rc['category'][1]['score']['value'],    # trader
            'club_value': rc['category'][2]['score']['value'],  # collector
            'top_squad': rc['category'][3]['score']['value']    # builder
        })
        return data

    def clubInfo(self):
        """Return getReliability."""
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

    def messages(self):
        """Return active messages."""
        rc = self.__get__(self.urls['fut']['ActiveMessage'])
        try:
            return rc['activeMessage']
        except:
            raise UnknownError('Invalid activeMessage response')

    def messageDelete(self, message_id):
        """Delete the specified message, by id.

        :params message_id: Message id.
        """
        url = '{0}/{1}'.format(self.urls['fut']['ActiveMessage'], message_id)
        self.__delete__(url)
