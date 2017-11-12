# -*- coding: utf-8 -*-

"""
fut.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut's basic methods.

"""

import requests
import re
import random
import time
import json
import pyotp
# from datetime import datetime, timedelta
try:
    from cookielib import LWPCookieJar
except ImportError:
    from http.cookiejar import LWPCookieJar

try:  # python2 compatibility
    input = raw_input
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

from .pin import Pin
from .config import headers, headers_and, headers_ios, cookies_file, token_file, timeout, delay
from .log import logger
from .urls import client_id, auth_url, card_info_url, messages_url
from .exceptions import (FutError, ExpiredSession, InternalServerError,
                         UnknownError, PermissionDenied, Captcha,
                         Conflict, MaxSessions, MultipleSession,
                         Unauthorized, FeatureDisabled, doLoginFail,
                         NoUltimateTeam, MarketLocked)
from .EAHashingAlgorithm import EAHashingAlgorithm


def baseId(resource_id, return_version=False):
    """Calculate base id and version from a resource id.

    :params resource_id: Resource id.
    :params return_version: (optional) True if You need version, returns (resource_id, version).
    """
    version = 0
    resource_id = resource_id + 0xC4000000  # 3288334336
    # TODO: version is broken due ^^, needs refactoring

    while resource_id > 0x01000000:  # 16777216
        version += 1
        if version == 1:
            resource_id -= 0x80000000  # 2147483648  # 0x50000000  # 1342177280 ?  || 0x2000000  # 33554432
        elif version == 2:
            resource_id -= 0x03000000  # 50331648
        else:
            resource_id -= 0x01000000  # 16777216

    if return_version:
        return resource_id, version - 67  # just correct "magic number"

    return resource_id


def itemParse(item_data, full=True):
    """Parser for item data. Returns nice dictionary.

    :params item_data: Item data received from ea servers.
    :params full: (optional) False if you're sniping and don't need extended info. Anyone really use this?
    """
    # TODO: object
    # TODO: dynamically parse all data
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
            'timestamp':        item_data['itemData'].get('timestamp'),  # auction start
            'rating':           item_data['itemData'].get('rating'),
            'assetId':          item_data['itemData'].get('assetId'),
            'resourceId':       item_data['itemData'].get('resourceId'),
            'itemState':        item_data['itemData'].get('itemState'),
            'rareflag':         item_data['itemData'].get('rareflag'),
            'formation':        item_data['itemData'].get('formation'),
            'leagueId':         item_data['itemData'].get('leagueId'),
            'injuryType':       item_data['itemData'].get('injuryType'),
            'injuryGames':      item_data['itemData'].get('injuryGames'),
            'lastSalePrice':    item_data['itemData'].get('lastSalePrice'),
            'fitness':          item_data['itemData'].get('fitness'),
            'training':         item_data['itemData'].get('training'),
            'suspension':       item_data['itemData'].get('suspension'),
            'contract':         item_data['itemData'].get('contract'),
            'position':         item_data['itemData'].get('preferredPosition'),
            'playStyle':        item_data['itemData'].get('playStyle'),  # used only for players
            'discardValue':     item_data['itemData'].get('discardValue'),
            'itemType':         item_data['itemData'].get('itemType'),
            'cardType':         item_data['itemData'].get('cardsubtypeid'),  # alias
            'cardsubtypeid':    item_data['itemData'].get('cardsubtypeid'),  # used only for cards
            'owners':           item_data['itemData'].get('owners'),
            'untradeable':      item_data['itemData'].get('untradeable'),
            'morale':           item_data['itemData'].get('morale'),
            'statsList':        item_data['itemData'].get('statsList'),  # what is this?
            'lifetimeStats':    item_data['itemData'].get('lifetimeStats'),
            'attributeList':    item_data['itemData'].get('attributeList'),
            'teamid':           item_data['itemData'].get('teamid'),
            'assists':          item_data['itemData'].get('assists'),
            'lifetimeAssists':  item_data['itemData'].get('lifetimeAssists'),
            'loyaltyBonus':     item_data['itemData'].get('loyaltyBonus'),
            'pile':             item_data['itemData'].get('pile'),
            'nation':           item_data['itemData'].get('nation'),  # nation_id?
            'year':             item_data['itemData'].get('resourceGameYear'),  # alias
            'resourceGameYear': item_data['itemData'].get('resourceGameYear'),
            'marketDataMinPrice': item_data['itemData'].get('marketDataMinPrice'),
            'marketDataMaxPrice': item_data['itemData'].get('marketDataMaxPrice'),
            'count':            item_data.get('count'),  # consumables only (?)
            'untradeableCount': item_data.get('untradeableCount'),  # consumables only (?)
            'loans':            item_data.get('loans'),
        })
        if 'item' in item_data:  # consumables only (?)
            return_data.update({
                'cardassetid':  item_data['item'].get('cardassetid'),
                'weightrare':   item_data['item'].get('weightrare'),
                'gold':         item_data['item'].get('gold'),
                'silver':       item_data['item'].get('silver'),
                'bronze':       item_data['item'].get('bronze'),
                'consumablesContractPlayer':    item_data['item'].get('consumablesContractPlayer'),
                'consumablesContractManager':    item_data['item'].get('consumablesContractManager'),
                'consumablesFormationPlayer':    item_data['item'].get('consumablesFormationPlayer'),
                'consumablesFormationManager':    item_data['item'].get('consumablesFormationManager'),
                'consumablesPosition':    item_data['item'].get('consumablesPosition'),
                'consumablesTraining':    item_data['item'].get('consumablesTraining'),
                'consumablesTrainingPlayer':    item_data['item'].get('consumablesTrainingPlayer'),
                'consumablesTrainingManager':    item_data['item'].get('consumablesTrainingManager'),
                'consumablesTrainingGk':    item_data['item'].get('consumablesTrainingGk'),
                'consumablesTrainingPlayerPlayStyle':    item_data['item'].get('consumablesTrainingPlayerPlayStyle'),
                'consumablesTrainingGkPlayStyle':    item_data['item'].get('consumablesTrainingGkPlayStyle'),
                'consumablesTrainingManagerLeagueModifier':    item_data['item'].get('consumablesTrainingManagerLeagueModifier'),
                'consumablesHealing':    item_data['item'].get('consumablesHealing'),
                'consumablesTeamTalksPlayer':    item_data['item'].get('consumablesTeamTalksPlayer'),
                'consumablesTeamTalksTeam':    item_data['item'].get('consumablesTeamTalksTeam'),
                'consumablesFitnessPlayer':    item_data['item'].get('consumablesFitnessPlayer'),
                'consumablesFitnessTeam':    item_data['item'].get('consumablesFitnessTeam'),
                'consumables':    item_data['item'].get('consumables'),
            })

    return return_data


'''  # different urls (platforms)
def cardInfo(resource_id):
    """Return card info."""
    # TODO: add referer to headers (futweb)
    url = '{0}{1}.json'.format(self.urls['card_info'], baseId(resource_id))
    return requests.get(url, timeout=timeout).json()
'''


# TODO: optimize messages (parse whole messages once!), xml parser might be faster
# TODO: parse more data (short club names etc.)
def nations(timeout=timeout):
    """Return all nations in dict {id0: nation0, id1: nation1}.

    :params year: Year.
    """
    rc = requests.get(messages_url, timeout=timeout)
    rc.encoding = 'utf-8'  # guessing takes huge amount of cpu time
    rc = rc.text
    data = re.findall('"search.nationName.nation([0-9]+)": "(.+)"', rc)
    nations = {}
    for i in data:
        nations[int(i[0])] = i[1]
    return nations


def leagues(year=2018, timeout=timeout):
    """Return all leagues in dict {id0: league0, id1: legaue1}.

    :params year: Year.
    """
    rc = requests.get(messages_url, timeout=timeout)
    rc.encoding = 'utf-8'  # guessing takes huge amount of cpu time
    rc = rc.text
    data = re.findall('"global.leagueFull.%s.league([0-9]+)": "(.+)"' % year, rc)
    leagues = {}
    for i in data:
        leagues[int(i[0])] = i[1]
    return leagues


def teams(year=2018, timeout=timeout):
    """Return all teams in dict {id0: team0, id1: team1}.

    :params year: Year.
    """
    rc = requests.get(messages_url, timeout=timeout)
    rc.encoding = 'utf-8'  # guessing takes huge amount of cpu time
    rc = rc.text
    data = re.findall('"global.teamFull.%s.team([0-9]+)": "(.+)"' % year, rc)
    teams = {}
    for i in data:
        teams[int(i[0])] = i[1]
    return teams


def stadiums(year=2018, timeout=timeout):
    """Return all stadium in dict {id0: stadium0, id1: stadium1}.

    :params year: Year.
    """
    rc = requests.get(messages_url, timeout=timeout)
    rc.encoding = 'utf-8'  # guessing takes huge amount of cpu time
    rc = rc.text
    data = re.findall('"global.stadiumFull.%s.stadium([0-9]+)": "(.+)"' % year, rc)
    stadiums = {}
    for i in data:
        stadiums[int(i[0])] = i[1]
    return stadiums


def balls(timeout=timeout):
    """Return all balls in dict {id0: ball0, id1: ball1}."""
    rc = requests.get(messages_url, timeout=timeout)
    rc.encoding = 'utf-8'  # guessing takes huge amount of cpu time
    rc = rc.text
    data = re.findall('"BallName_([0-9]+)": "(.+)"', rc)
    balls = {}
    for i in data:
        balls[int(i[0])] = i[1]
    return balls


def players(timeout=timeout):
    """Return all players in dict {id: c, f, l, n, r}.
    id, rank, nationality(?), first name, last name.
    """
    rc = requests.get('{0}{1}.json'.format(card_info_url, 'players'), timeout=timeout).json()
    players = {}
    for i in rc['Players'] + rc['LegendsPlayers']:
        players[i['id']] = {'id': i['id'],
                            'firstname': i['f'],
                            'lastname': i['l'],
                            'surname': i.get('c'),
                            'rating': i['r'],
                            'nationality': i['n']}  # replace with nationality object when created
    return players


def playstyles(year=2018, timeout=timeout):
    """Return all playstyles in dict {id0: playstyle0, id1: playstyle1}.

    :params year: Year.
    """
    rc = requests.get(messages_url, timeout=timeout)
    rc.encoding = 'utf-8'  # guessing takes huge amount of cpu time
    rc = rc.text
    data = re.findall('"playstyles.%s.playstyle([0-9]+)": "(.+)"' % year, rc)
    playstyles = {}
    for i in data:
        playstyles[int(i[0])] = i[1]
    return playstyles


class Core(object):
    def __init__(self, email, passwd, secret_answer, platform='pc', code=None, totp=None, sms=False, emulate=None, debug=False, cookies=cookies_file, token=token_file, timeout=timeout, delay=delay, proxies=None):
        self.credits = 0
        self.duplicates = []
        self.cookies_file = cookies  # TODO: map self.cookies to requests.Session.cookies?
        self.token_file = token
        self.timeout = timeout
        self.delay = delay
        self.request_time = 0
        # db
        self._players = None
        self._nations = None
        self._leagues = {}
        self._teams = {}
        self._usermassinfo = {}
        logger(save=debug)  # init root logger
        self.logger = logger(__name__)
        # TODO: validate fut request response (200 OK)
        self.__launch__(email, passwd, secret_answer, platform=platform, code=code, totp=totp, sms=sms, emulate=emulate, proxies=proxies)

    def __login__(self, email, passwd, code=None, totp=None, sms=False):
        """Log in - needed only if we don't have access token or it's expired."""
        params = {'prompt': 'login',
                  'accessToken': 'null',
                  'client_id': client_id,
                  'response_type': 'token',
                  'display': 'web2/login',
                  'locale': 'en_US',
                  'redirect_uri': 'https://www.easports.com/fifa/ultimate-team/web-app/auth.html',
                  'scope': 'basic.identity offline signin'}
        self.r.headers['Referer'] = 'https://www.easports.com/fifa/ultimate-team/web-app/'
        rc = self.r.get('https://accounts.ea.com/connect/auth', params=params, timeout=self.timeout)
        # TODO: validate (captcha etc.)
        if rc.url != 'https://www.easports.com/fifa/ultimate-team/web-app/auth.html':  # redirect target  # this check is probably not needed
            self.r.headers['Referer'] = rc.url
            # origin required?
            data = {'email': email,
                    'password': passwd,
                    'country': 'US',  # is it important?
                    'phoneNumber': '',  # TODO: add phone code verification
                    'passwordForPhone': '',
                    'gCaptchaResponse': '',
                    'isPhoneNumberLogin': 'false',  # TODO: add phone login
                    'isIncompletePhone': '',
                    '_rememberMe': 'on',
                    'rememberMe': 'on',
                    '_eventId': 'submit'}
            rc = self.r.post(rc.url, data=data, timeout=self.timeout)
            # rc = rc.text

            if "'successfulLogin': false" in rc.text:
                failedReason = re.search('general-error">\s+<div>\s+<div>\s+(.*)\s.+', rc.text).group(1)
                # Your credentials are incorrect or have expired. Please try again or reset your password.
                raise FutError(reason=failedReason)

            if 'var redirectUri' in rc.text:
                rc = self.r.get(rc.url, params={'_eventId': 'end'})  # initref param was missing here

            '''  # pops out only on first launch
            if 'FIFA Ultimate Team</strong> needs to update your Account to help protect your gameplay experience.' in rc:  # request email/sms code
                self.r.headers['Referer'] = rc.url  # s2
                rc = self.r.post(rc.url.replace('s2', 's3'), {'_eventId': 'submit'}, timeout=self.timeout).content
                self.r.headers['Referer'] = rc.url  # s3
                rc = self.r.post(rc.url, {'twofactorType': 'EMAIL', 'country': 0, 'phoneNumber': '', '_eventId': 'submit'}, timeout=self.timeout)
            '''

            # click button to send code
            if 'Login Verification' in rc.text:  # click button to get code sent
                if totp:
                    rc = self.r.post(rc.url, {'_eventId': 'submit', 'codeType': 'APP'})
                    code = pyotp.TOTP(totp).now()
                elif sms:
                    rc = self.r.post(rc.url, {'_eventId': 'submit', 'codeType': 'SMS'})
                else:  # email
                    rc = self.r.post(rc.url, {'_eventId': 'submit', 'codeType': 'EMAIL'})

            # if 'We sent a security code to your' in rc.text or 'Your security code was sent to' in rc.text or 'Enter the 6-digit verification code' in rc.text or 'We have sent a security code' in rc.text:  # post code
            if 'Enter your security code' in rc.text:
                # TODO: 'We sent a security code to your email' / 'We sent a security code to your ?'
                # TODO: pick code from codes.txt?
                if not code:
                    # self.saveSession()
                    # raise FutError(reason='Error during login process - code is required.')
                    code = input('Enter code: ')
                self.r.headers['Referer'] = url = rc.url
                # self.r.headers['Upgrade-Insecure-Requests'] = '1'  # ?
                # self.r.headers['Origin'] = 'https://signin.ea.com'
                rc = self.r.post(url.replace('s3', 's4'), {'oneTimeCode': code, '_trustThisDevice': 'on', 'trustThisDevice': 'on', '_eventId': 'submit'}, timeout=self.timeout)
                # rc = rc.text
                if 'Incorrect code entered' in rc.text or 'Please enter a valid security code' in rc.text:
                    raise FutError(reason='Error during login process - provided code is incorrect.')
                if 'Set Up an App Authenticator' in rc.text:  # may we drop this?
                    rc = self.r.post(url.replace('s3', 's4'), {'_eventId': 'cancel', 'appDevice': 'IPHONE'}, timeout=self.timeout)
                    # rc = rc.text

            rc = re.match('https://www.easports.com/fifa/ultimate-team/web-app/auth.html#access_token=(.+?)&token_type=(.+?)&expires_in=[0-9]+', rc.url)
            self.access_token = rc.group(1)
            self.token_type = rc.group(2)
            # TODO?: refresh after expires_in

            self.saveSession()

    def __launch__(self, email, passwd, secret_answer, platform='pc', code=None, totp=None, sms=False, emulate=None, proxies=None):
        """Launch futweb

        :params email: Email.
        :params passwd: Password.
        :params secret_answer: Answer for secret question.
        :params platform: (optional) [pc/xbox/xbox360/ps3/ps4] Platform.
        :params code: (optional) Security code generated in origin or sent via mail/sms.
        :params emulate: (optional) [and/ios] Emulate mobile device.
        :params proxies: (optional) [dict] http/socks proxies in requests's format. http://docs.python-requests.org/en/master/user/advanced/#proxies
        """
        # TODO: split into smaller methods
        # TODO: check first if login is needed (https://www.easports.com/fifa/api/isUserLoggedIn)
        # TODO: get gamesku, url from shards !!

        self.emulate = emulate
        secret_answer_hash = EAHashingAlgorithm().EAHash(secret_answer)
        # create session
        self.r = requests.Session()  # init/reset requests session object
        if proxies is not None:
            self.r.proxies = proxies
        # load saved cookies/session
        if self.cookies_file:
            self.r.cookies = LWPCookieJar(self.cookies_file)
            try:
                with open(self.token_file, 'r') as f:
                    self.token_type, self.access_token = f.readline().replace('\n', '').replace('\r', '').split(' ')  # removing \n \r just to make sure
            except FileNotFoundError:
                self.__login__(email=email, passwd=passwd, code=code, totp=totp, sms=sms)
            try:
                self.r.cookies.load(ignore_discard=True)  # is it good idea to load discarded cookies after long time?
            except IOError:
                pass
                # self.r.cookies.save(ignore_discard=True)  # create empty file for cookies
        if emulate == 'and':
            raise FutError(reason='Emulate feature is currently disabled duo latest changes in login process, need more info')
            self.r.headers = headers_and.copy()  # i'm android now ;-)
        elif emulate == 'ios':
            raise FutError(reason='Emulate feature is currently disabled duo latest changes in login process, need more info')
            self.r.headers = headers_ios.copy()  # i'm ios phone now ;-)
        else:
            self.r.headers = headers.copy()  # i'm chrome browser now ;-)
        if platform == 'pc':  # TODO: get this from shards
            game_sku = 'FFA18PCC'
        elif platform == 'xbox':
            game_sku = 'FFA18XBO'
        elif platform == 'xbox360':
            game_sku = 'FFA18XBX'
        elif platform == 'ps3':
            game_sku = 'FFA18PS3'  # not tested
        elif platform == 'ps4':
            game_sku = 'FFA18PS4'
            # platform = 'ps3'  # ps4 not available in shards
        else:
            raise FutError(reason='Wrong platform. (Valid ones are pc/xbox/xbox360/ps3/ps4)')
        # if self.r.get(self.urls['main_site']+'/fifa/api/isUserLoggedIn', timeout=self.timeout).json()['isLoggedIn']:
        #    return True  # no need to log in again
        # emulate
        if emulate == 'ios':
            sku = 'FUT18IOS'
            clientVersion = 21
        elif emulate == 'and':
            sku = 'FUT18AND'
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
            sku = 'FUT18WEB'
            clientVersion = 1
        else:
            raise FutError(reason='Invalid emulate parameter. (Valid ones are and/ios).')  # pc/ps3/xbox/
        self.sku = sku  # TODO: use self.sku in all class
        self.sku_a = 'FFT18'

        # === launch futweb
        params = {'accessToken': self.access_token,
                  'client_id': 'FIFA-18-WEBCLIENT',
                  'response_type': 'token',
                  'display': 'web2/login',
                  'locale': 'en_US',
                  'redirect_uri': 'https://www.easports.com/fifa/ultimate-team/web-app/auth.html',
                  'scope': 'basic.identity offline signin'}
        rc = self.r.get('https://accounts.ea.com/connect/auth', params=params)
        rc = re.match('https://www.easports.com/fifa/ultimate-team/web-app/auth.html#access_token=(.+?)&token_type=(.+?)&expires_in=[0-9]+', rc.url)
        self.access_token = rc.group(1)
        self.token_type = rc.group(2)

        # self.r.headers['Referer'] = 'https://www.easports.com/fifa/ultimate-team/web-app/auth.html'
        rc = self.r.get('https://www.easports.com/fifa/ultimate-team/web-app/', timeout=self.timeout).text
        # year = re.search('fut_year = "([0-9]{4}])"', rc).group(1)  # use this to construct urls, sku etc.
        # guid = re.search('fut_guid = "(.+?)"', rc).group(1)
        # TODO: config
        self.r.headers['Referer'] = 'https://www.easports.com/fifa/ultimate-team/web-app/'
        self.r.headers['Accept'] = 'application/json'
        self.r.headers['Authorization'] = '%s %s' % (self.token_type, self.access_token)
        rc = self.r.get('https://gateway.ea.com/proxy/identity/pids/me').json()  # TODO: validate response
        if rc.get('error') == 'invalid_access_token':
            print('invalid token')
            self.__login__(email=email, passwd=passwd, totp=totp, sms=sms)
            return self.__launch__(email=email, passwd=passwd, secret_answer=secret_answer, platform=platform, code=code, totp=totp, sms=sms, emulate=emulate, proxies=proxies)
        self.nucleus_id = rc['pid']['externalRefValue']  # or pidId
        self.dob = rc['pid']['dob']
        # tos_version = rc['tosVersion']
        # authentication_source = rc['authenticationSource']
        # password_signature = rc['passwordSignature']
        # TODO: various checks (validation)
        del self.r.headers['Authorization']
        self.r.headers['Easw-Session-Data-Nucleus-Id'] = self.nucleus_id

        # shards
        self._ = int(time.time() * 1000)
        rc = self.r.get('https://%s/ut/shards/v2' % auth_url, data={'_': self._}).json()  # TODO: parse this
        self._ += 1
        self.fut_host = {
            'pc': 'utas.external.s2.fut.ea.com:443',
            'ps3': 'utas.external.s2.fut.ea.com:443',
            'ps4': 'utas.external.s2.fut.ea.com:443',
            'xbox': 'utas.external.s3.fut.ea.com:443',
            # 'ios': 'utas.external.fut.ea.com:443',
            # 'and': 'utas.external.fut.ea.com:443'
        }
        self.fut_host = self.fut_host[platform]

        # personas
        data = {'filterConsoleLogin': 'true',
                'sku': sku,
                'returningUserGameYear': '2017',  # allways year-1?
                '_': self._}
        rc = self.r.get('https://%s/ut/game/fifa18/user/accountinfo' % self.fut_host, params=data).json()
        self._ += 1
        # pick persona (first valid for given game_sku)
        personas = rc['userAccountInfo']['personas']
        for p in personas:
            # self.clubs = [i for i in p['userClubList']]
            # sort clubs by lastAccessTime (latest first but looks like ea is doing this for us(?))
            # self.clubs.sort(key=lambda i: i['lastAccessTime'], reverse=True)
            for c in p['userClubList']:
                if c['skuAccessList'] and game_sku in c['skuAccessList']:
                    self.persona_id = p['personaId']
                    break
        if not hasattr(self, 'persona_id'):
            raise FutError(reason='Error during login process (no persona found).')

        # authorization
        # TODO?: with proper saved session we might start here
        del self.r.headers['Easw-Session-Data-Nucleus-Id']
        self.r.headers['Origin'] = 'http://www.easports.com'
        params = {'client_id': 'FOS-SERVER',  # i've seen in some js/json response but cannot find now
                  'redirect_uri': 'nucleus:rest',
                  'response_type': 'code',
                  'access_token': self.access_token}
        rc = self.r.get('https://accounts.ea.com/connect/auth', params=params).json()
        auth_code = rc['code']

        self.r.headers['Content-Type'] = 'application/json'
        data = {'isReadOnly': 'false',
                'sku': sku,
                'clientVersion': clientVersion,
                'nucleusPersonaId': self.persona_id,
                'gameSku': game_sku,
                'locale': 'en-US',
                'method': 'authcode',
                'priorityLevel': 4,
                'identification': {'authCode': auth_code,
                                   'redirectUrl': 'nucleus:rest'}}
        params = {'sku_a': self.sku_a,
                  '': int(time.time() * 1000)}
        rc = self.r.post('https://%s/ut/auth' % self.fut_host, data=json.dumps(data), params=params, timeout=self.timeout)
        if rc.status_code == 401:  # and rc.text == 'multiple session'
            raise FutError('multiple session')
        if rc.status_code == 500:
            raise InternalServerError('Servers are probably temporary down.')
        rc = rc.json()
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
        self.r.headers['Easw-Session-Data-Nucleus-Id'] = self.nucleus_id
        rc = self.r.get('https://%s/ut/game/fifa18/phishing/question' % self.fut_host, params={'_': self._}, timeout=self.timeout).json()
        self._ += 1
        if rc.get('code') == '458':
            raise Captcha()
        elif rc.get('string') != 'Already answered question':
            params = {'answer': secret_answer_hash}
            rc = self.r.post('https://%s/ut/game/fifa18/phishing/validate' % self.fut_host, params=params, timeout=self.timeout).json()
            if rc['string'] != 'OK':  # we've got an error
                # Known reasons:
                # * invalid secret answer
                # * No remaining attempt
                raise FutError(reason='Error during login process (%s).' % (rc['reason']))
            self.r.headers['X-UT-PHISHING-TOKEN'] = self.token = rc['token']
            # ask again for question to refresh(?) token, i'm just doing what webapp is doing
            rc = self.r.get('https://%s/ut/game/fifa18/phishing/question' % self.fut_host, params={'_': self._}, timeout=self.timeout).json()
            self._ += 1
        self.r.headers['X-UT-PHISHING-TOKEN'] = self.token = rc['token']

        # init pin
        self.pin = Pin(sid=self.sid, nucleus_id=self.nucleus_id, persona_id=self.persona_id, dob=self.dob[:-3], platform=platform)
        events = [self.pin.event('login', status='success')]
        self.pin.send(events)

        # get basic user info
        # TODO: parse usermassinfo and change _usermassinfo to userinfo
        # TODO?: usermassinfo as separate method && ability to refresh piles etc.
        self._usermassinfo = self.r.get('https://%s/ut/game/fifa18/usermassinfo' % self.fut_host, params={'_': self._}, timeout=self.timeout).json()
        self._ += 1
        if self._usermassinfo['settings']['configs'][2]['value'] == 0:
            raise FutError(reason='Transfer market is probably disabled on this account.')  # if tradingEnabled = 0

        # size of piles
        piles = self.pileSize()
        self.tradepile_size = piles['tradepile']
        self.watchlist_size = piles['watchlist']

        # refresh token
        # params = {'response_type': 'token',
        #           'redirect_uri': 'nucleus:rest',
        #           'prompt': 'none',
        #           'client_id': 'ORIGIN_JS_SDK'}
        # rc = self.r.get('https://accounts.ea.com/connect/auth', params=params).json()
        # self.access_token = rc['access_token']
        # self.token_type = rc['token_type']
        # expired_in

        self.saveSession()

        # pinEvents - home screen
        events = [self.pin.event('page_view', 'Hub - Home')]
        self.pin.send(events)

        # pinEvents - boot_end
        events = [self.pin.event('connection'),
                  self.pin.event('boot_end', end_reason='normal')]
        self.pin.send(events)

        self.keepalive()  # credits

#    def __shards__(self):
#        """Returns shards info."""
#        # TODO: headers
#        self.r.headers['X-UT-Route'] = self.urls['fut_base']
#        return self.r.get(self.urls['shards'], params={'_': int(time.time()*1000)}, timeout=self.timeout).json()
#        # self.r.headers['X-UT-Route'] = self.urls['fut_pc']

    def __request__(self, method, url, data={}, params={}, fast=False):
        """Prepare headers and sends request. Returns response as a json object.

        :params method: Rest method.
        :params url: Url.
        """
        # TODO: update credtis?
        url = 'https://%s/ut/game/fifa18/%s' % (self.fut_host, url)

        self.logger.debug("request: {0} data={1};  params={2}".format(url, data, params))
        if method.upper() == 'GET':
            params['_'] = self._  # only for get(?)
            self._ += 1
        if not fast:  # TODO: refactorization
            time.sleep(max(self.request_time - time.time() + random.randrange(self.delay[0], self.delay[1] + 1), 0))  # respect minimum delay
            self.r.options(url, params=params)
        else:
            time.sleep(max(self.request_time - time.time() + 1.4, 0))  # respect 1s minimum delay between requests
        self.request_time = time.time()  # save request time for delay calculations
        if method.upper() == 'GET':
            rc = self.r.get(url, data=data, params=params, timeout=self.timeout)
        elif method.upper() == 'POST':
            rc = self.r.post(url, data=data, params=params, timeout=self.timeout)
        elif method.upper() == 'PUT':
            rc = self.r.put(url, data=data, params=params, timeout=self.timeout)
        elif method.upper() == 'DELETE':
            rc = self.r.delete(url, data=data, params=params, timeout=self.timeout)
        self.logger.debug("response: {0}".format(rc.content))
        if not rc.ok:  # status != 200
            if rc.status_code == 401:
                # TODO?: send pinEvent https://gist.github.com/oczkers/7e5de70915b87262ddea961c49180fd6
                print(rc.content)
                raise ExpiredSession()
            elif rc.status_code == 426:
                raise FutError('426 Too many requests')
            elif rc.status_code == 429:
                raise FutError('429 Too many requests')
            elif rc.status_code == 458:
                print(rc.headers)
                print(rc.status_code)
                print(rc.cookies)
                print(rc.content)
                # pinEvents
                events = [self.pin.event('error')]
                self.pin.send(events)
                raise Captcha()
            elif rc.status_code == 460:
                raise PermissionDenied(460)
            elif rc.status_code == 461:
                raise PermissionDenied(461)  # You are not allowed to bid on this trade TODO: add code, reason etc
            elif rc.status_code == 494:
                raise MarketLocked()
            elif rc.status_code in (512, 521):
                raise FutError('512/521 Temporary ban or just too many requests.')
            # it makes sense to print headers, status_code, etc. only when we don't know what happened
            print(rc.headers)
            print(rc.status_code)
            print(rc.cookies)
            print(rc.content)
            raise UnknownError(rc.content)
        if rc.text == '':
            rc = {}
        else:
            rc = rc.json()
            if 'credits' in rc and rc['credits']:
                self.credits = rc['credits']
            if 'duplicateItemIdList' in rc:
                self.duplicates = [i['itemId'] for i in rc['duplicateItemIdList']]
        self.saveSession()
        return rc

    def __sendToPile__(self, pile, trade_id=None, item_id=None):
        """Send to pile.

        :params trade_id: Trade id.
        :params item_id: (optional) Iteam id.
        """
        method = 'PUT'
        url = 'item'

        # TODO: accept multiple trade_ids (just extend list below)
        # if pile == 'watchlist':
        #     params = {'tradeId': trade_id}
        #     data = {'auctionInfo': [{'id': trade_id}]}
        #     self.__put__(self.urls['fut']['WatchList'], params=params, data=json.dumps(data))
        #     return True

        # if trade_id > 0:
        #     # won item
        #     data = {"itemData": [{"tradeId": trade_id, "pile": pile, "id": str(item_id)}]}
        # else:
        #     # unassigned item
        #     data = {"itemData": [{"pile": pile, "id": str(item_id)}]}
        data = {"itemData": [{"pile": pile, "id": str(item_id)}]}

        rc = self.__request__(method, url, data=json.dumps(data))
        if rc['itemData'][0]['success']:
            self.logger.info("{0} (itemId: {1}) moved to {2} Pile".format(trade_id, item_id, pile))
        else:
            self.logger.error("{0} (itemId: {1}) NOT MOVED to {2} Pile. REASON: {3}".format(trade_id, item_id, pile, rc['itemData'][0]['reason']))
            # if rc['itemData'][0]['reason'] == 'Duplicate Item Type' and rc['itemData'][0]['errorCode'] == 472:  # errorCode check is enought?
        return rc['itemData'][0]['success']

    def logout(self, save=True):
        """Log out nicely (like clicking on logout button).

        :params save: False if You don't want to save cookies.
        """
        self.r.delete('https://%s/ut/auth' % self.fut_host, timeout=self.timeout)
        if save:
            self.saveSession()
        # needed? https://accounts.ea.com/connect/logout?client_id=FIFA-18-WEBCLIENT&redirect_uri=https://www.easports.com/fifa/ultimate-team/web-app/auth.html
        return True

    @property
    def players(self):
        """Return all players in dict {id: c, f, l, n, r}."""
        if not self._players:
            self._players = players()
        return self._players

    @property
    def playstyles(self, year=2018):
        """Return all playstyles in dict {id0: playstyle0, id1: playstyle1}.

        :params year: Year.
        """
        if not self._playstyles:
            self._playstyles = playstyles()
        return self._playstyles

    @property
    def nations(self):
        """Return all nations in dict {id0: nation0, id1: nation1}.

        :params year: Year.
        """
        if not self._nations:
            self._nations = nations()
        return self._nations

    @property
    def leagues(self, year=2018):
        """Return all leagues in dict {id0: league0, id1: league1}.

        :params year: Year.
        """
        if year not in self._leagues:
            self._leagues[year] = leagues(year)
        return self._leagues[year]

    @property
    def teams(self, year=2018):
        """Return all teams in dict {id0: team0, id1: team1}.

        :params year: Year.
        """
        if year not in self._teams:
            self._teams[year] = teams(year)
        return self._teams[year]

    @property
    def stadiums(self):
        """Return all stadiums in dict {id0: stadium0, id1: stadium1}.

        :params year: Year.
        """
        if not self._stadiums:
            self._stadiums = stadiums()
        return self._stadiums

    def saveSession(self):
        """Save cookies/session."""
        if self.cookies_file:
            self.r.cookies.save(ignore_discard=True)
            with open(self.token_file, 'w') as f:
                f.write('%s %s' % (self.token_type, self.access_token))

    def baseId(self, *args, **kwargs):
        """Calculate base id and version from a resource id."""
        return baseId(*args, **kwargs)

    def cardInfo(self, resource_id):
        """Return card info.

        :params resource_id: Resource id.
        """
        # TODO: add referer to headers (futweb)
        base_id = baseId(resource_id)
        if base_id in self.players:
            return self.players[base_id]
        else:  # not a player?
            url = '{0}{1}.json'.format(card_info_url, base_id)
            return requests.get(url, timeout=self.timeout).json()

    def searchDefinition(self, asset_id, start=0, count=46):
        """Return variations of the given asset id, e.g. IF cards.

        :param asset_id: Asset id / Definition id.
        :param start: (optional) Start page.
        :param count: (optional) Number of definitions you want to request.
        """
        method = 'GET'
        url = 'defid'

        base_id = baseId(asset_id)
        if base_id not in self.players:
            raise FutError(reason='Invalid player asset/definition id.')

        params = {
            'defId': base_id,
            'start': start,
            'type': 'player',
            'count': count
        }

        rc = self.__request__(method, url, params=params)

        try:
            return [itemParse({'itemData': i}) for i in rc['itemData']]
        except:
            raise UnknownError('Invalid definition response')

    def search(self, ctype, level=None, category=None, assetId=None, defId=None,
               min_price=None, max_price=None, min_buy=None, max_buy=None,
               league=None, club=None, position=None, zone=None, nationality=None,
               rare=False, playStyle=None, start=0, page_size=16,
               fast=False):
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
        :param nationality: (optional) Nation id.
        :param rare: (optional) [boolean] True for searching special cards.
        :param playStyle: (optional) Play style.
        :param start: (optional) Start page sent to server so it supposed to be 12/15, 24/30 etc. (default platform page_size*n)
        :param page_size: (optional) Page size (items per page).
        """
        # TODO: add "search" alias
        # TODO: generator
        method = 'GET'
        url = 'transfermarket'

        # pinEvents
        if start == 0:
            events = [self.pin.event('page_view', 'Transfer Market Search')]
            self.pin.send(events, fast=fast)

        # if start > 0 and page_size == 16:
        #     if not self.emulate:  # wbeapp
        #         page_size = 12
        #         if start == 16:  # second page
        #             start = 12
        #     elif self.emulate and start == 16:  # emulating android/ios
        #         start = 15
        # elif page_size > 50:  # server restriction
        #     page_size = 50
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
        if zone:        params['zone'] = zone
        if nationality: params['nat'] = nationality
        if rare:        params['rare'] = 'SP'
        if playStyle:   params['playStyle'] = playStyle

        rc = self.__request__(method, url, params=params, fast=fast)

        # pinEvents
        if start == 0:
            events = [self.pin.event('page_view', 'Transfer Market Results - List View')]
            self.pin.send(events, fast=fast)

        return [itemParse(i) for i in rc.get('auctionInfo', ())]

    def searchAuctions(self, *args, **kwargs):
        """Alias for search method, just to keep compatibility."""
        return self.search(*args, **kwargs)

    def bid(self, trade_id, bid, fast=False):
        """Make a bid.

        :params trade_id: Trade id.
        :params bid: Amount of credits You want to spend.
        :params fast: True for fastest bidding (skips trade status & credits check).
        """
        method = 'PUT'
        url = 'trade/%s/bid' % trade_id

        if not fast:
            rc = self.tradeStatus(trade_id)[0]
            # don't bid if current bid is equal or greater than our max bid
            if rc['currentBid'] >= bid or self.credits < bid:
                return False  # TODO: add exceptions
        data = {'bid': bid}
        try:
            rc = self.__request__(method, url, data=json.dumps(data), params={'sku_a': self.sku_a}, fast=fast)['auctionInfo'][0]
        except PermissionDenied:  # too slow, somebody took it already :-(
            return False
        if rc['bidState'] == 'highest' or (rc['tradeState'] == 'closed' and rc['bidState'] == 'buyNow'):  # checking 'tradeState' is required?
            return True
        else:
            return False

    def club(self, sort='desc', ctype='player', defId='', start=0, count=91, level=None):
        """Return items in your club, excluding consumables."""
        method = 'GET'
        url = 'club'

        params = {'sort': sort, 'type': ctype, 'defId': defId, 'start': start, 'count': count}
        if level:
            params['level'] = level
        rc = self.__request__(method, url, params=params)

        # pinEvent
        if start == 0:
            if ctype == 'player':
                pgid = 'Club - Players - List View'
            elif ctype == 'staff':
                pgid = 'Club - Staff - List View'
            elif ctype in ('item', 'kit', 'ball', 'badge', 'stadium'):
                pgid = 'Club - Club Items - List View'
            # else:  # TODO: THIS IS probably WRONG, detect all ctypes
            #     pgid = 'Club - Club Items - List View'
            events = [self.pin.event('page_view', pgid)]
            self.pin.send(events)

        return [itemParse({'itemData': i}) for i in rc['itemData']]

    def clubStaff(self):
        """Return staff in your club."""
        method = 'GET'
        url = 'club/stats/staff'

        rc = self.__request__(method, url)
        return rc  # TODO?: parse

    def clubConsumables(self, fast=False):
        """Return all consumables from club."""
        method = 'GET'
        url = 'club/consumables/development'

        rc = self.__request__(method, url)

        events = [self.pin.event('page_view', 'Hub - Club')]
        self.pin.send(events, fast=fast)
        events = [self.pin.event('page_view', 'Club - Consumables')]
        self.pin.send(events, fast=fast)
        events = [self.pin.event('page_view', 'Club - Consumables - List View')]
        self.pin.send(events, fast=fast)

        return [{itemParse(i) for i in rc.get('itemData', ())}]

    def squad(self, squad_id=0, persona_id=None):
        """Return a squad.

        :params squad_id: Squad id.
        """
        method = 'GET'
        url = 'squad/%s/user/%s' % (squad_id, persona_id or self.persona_id)

        # pinEvents
        events = [self.pin.event('page_view', 'Hub - Squads')]
        self.pin.send(events)

        # TODO: ability to return other info than players only
        rc = self.__request__(method, url)

        # pinEvents
        events = [self.pin.event('page_view', 'Squads - Squad Overview')]
        self.pin.send(events)

        return [itemParse(i) for i in rc.get('players', ())]

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
        method = 'GET'
        url = 'trade/status'

        if not isinstance(trade_id, (list, tuple)):
            trade_id = (trade_id,)
        trade_id = (str(i) for i in trade_id)
        params = {'tradeIds': ','.join(trade_id)}  # multiple trade_ids not tested
        rc = self.__request__(method, url, params=params)
        return [itemParse(i, full=False) for i in rc['auctionInfo']]

    def tradepile(self):
        """Return items in tradepile."""
        method = 'GET'
        url = 'tradepile'

        rc = self.__request__(method, url)

        # pinEvents
        events = [self.pin.event('page_view', 'Transfer List - List View')]
        self.pin.send(events)

        return [itemParse(i) for i in rc.get('auctionInfo', ())]

    def watchlist(self):
        """Return items in watchlist."""
        method = 'GET'
        url = 'watchlist'

        rc = self.__request__(method, url)

        # pinEvents
        events = [self.pin.event('page_view', 'Transfer Targets - List View')]
        self.pin.send(events)

        return [itemParse(i) for i in rc.get('auctionInfo', ())]

    def unassigned(self):
        """Return Unassigned items (i.e. buyNow items)."""
        method = 'GET'
        url = 'purchased/items'

        rc = self.__request__(method, url)

        # pinEvents
        events = [self.pin.event('page_view', 'Unassigned Items - List View')]
        self.pin.send(events)

        return [itemParse({'itemData': i}) for i in rc.get('itemData', ())]

    def sell(self, item_id, bid, buy_now, duration=3600, fast=False):
        """Start auction. Returns trade_id.

        :params item_id: Item id.
        :params bid: Stard bid.
        :params buy_now: Buy now price.
        :params duration: Auction duration in seconds (Default: 3600).
        """
        method = 'POST'
        url = 'auctionhouse'

        # TODO: auto send to tradepile
        data = {'buyNowPrice': buy_now, 'startingBid': bid, 'duration': duration, 'itemData': {'id': item_id}}
        rc = self.__request__(method, url, data=json.dumps(data), params={'sku_a': self.sku_a})
        if not fast:  # tradeStatus check like webapp do
            self.tradeStatus(rc['id'])
        return rc['id']

    def quickSell(self, item_id):
        """Quick sell.

        :params item_id: Item id.
        """
        method = 'DELETE'
        url = 'item/%s' % item_id

        if not isinstance(item_id, (list, tuple)):
            item_id = (item_id,)
        item_id = (str(i) for i in item_id)
        params = {'itemIds': ','.join(item_id)}
        self.__request__(method, url, params=params)  # {"items":[{"id":280607437106}],"totalCredits":18136}
        return True

    def watchlistDelete(self, trade_id):
        """Remove cards from watchlist.

        :params trade_id: Trade id.
        """
        method = 'DELETE'
        url = 'watchlist'

        if not isinstance(trade_id, (list, tuple)):
            trade_id = (trade_id,)
        trade_id = (str(i) for i in trade_id)
        params = {'tradeId': ','.join(trade_id)}
        self.__request__(method, url, params=params)  # returns nothing
        return True

    def tradepileDelete(self, trade_id):  # item_id instead of trade_id?
        """Remove card from tradepile.

        :params trade_id: Trade id.
        """
        method = 'DELETE'
        url = 'trade/%s' % trade_id

        self.__request__(method, url)  # returns nothing
        # TODO: validate status code
        return True

    def tradepileClear(self):
        """Removes all sold items from tradepile."""
        method = 'DELETE'
        url = 'trade/sold'

        self.__request__(method, url)
        # return True

    def sendToTradepile(self, item_id, safe=True):
        """Send to tradepile (alias for __sendToPile__).

        :params item_id: Item id.
        :params safe: (optional) False to disable tradepile free space check.
        """
        if safe and len(self.tradepile()) >= self.tradepile_size:  # TODO?: optimization (don't parse items in tradepile)
            return False
        return self.__sendToPile__('trade', item_id=item_id)

    def sendToClub(self, item_id):
        """Send to club (alias for __sendToPile__).

        :params item_id: Item id.
        """
        return self.__sendToPile__('club', item_id=item_id)

    def sendToWatchlist(self, trade_id):
        """Send to watchlist.

        :params trade_id: Trade id.
        """
        method = 'PUT'
        url = 'watchlist'

        data = {'auctionInfo': [{'id': trade_id}]}
        return self.__request__(method, url, data=json.dumps(data))

    def sendToSbs(self, challenge_id, item_id):
        """Send card FROM CLUB to first free slot in sbs squad."""
        # TODO?: multiple item_ids
        method = 'PUT'
        url = 'sbs/challenge/%s/squad' % challenge_id

        squad = self.sbsSquad(challenge_id)
        players = []
        moved = False
        n = 0
        for i in squad['squad']['players']:
            if i['itemData']['id'] == item_id:  # item already in sbs  # TODO?: report reason
                return False
            if i['itemData']['id'] == 0 and not moved:
                i['itemData']['id'] = item_id
                moved = True
            players.append({"index": n,
                            "itemData": {"id": i['itemData']['id'],
                                         "dream": False}})
            n += 1
        data = {'players': players}

        if not moved:
            return False
        else:
            self.__request__(method, url, data=json.dumps(data))
            return True

    # def relist(self, clean=False):
    #     """Relist all tradepile. Returns True or number of deleted (sold) if clean was set.
    #
    #     :params clean: (optional) True if You want to purge pile from sold cards.
    #     """
    #     # TODO: return relisted ids
    #     self.__put__(self.urls['fut']['SearchAuctionsReListItem'])
    #     # {"tradeIdList":[{"id":139632781208},{"id":139632796467}]}
    #     if clean:  # remove sold cards
    #         sold = 0
    #         for i in self.tradepile():
    #             if i['tradeState'] == 'closed':
    #                 self.tradepileDelete(i['tradeId'])
    #                 sold += 1
    #         return sold
    #     return True

    def relist(self):
        """ReList all cards in tradepile. EA method - might(?) change prices."""
        method = 'PUT'
        url = 'auctionhouse/relist'

        return self.__request__(method, url)

    def applyConsumable(self, item_id, resource_id):
        """Apply consumable on player.

        :params item_id: Item id of player.
        :params resource_id: Resource id of consumable.
        """
        # TODO: catch exception when consumable is not found etc.
        # TODO: multiple players like in quickSell
        method = 'POST'
        url = 'item/resource/%s' % resource_id

        data = {'apply': [{'id': item_id}]}
        self.__request__(method, url, data=json.dumps(data))

    def keepalive(self):
        """Refresh credit amount to let know that we're still online. Returns credit amount."""
        method = 'GET'
        url = 'user/credits'

        return self.__request__(method, url)['credits']

    def pileSize(self):
        """Return size of tradepile and watchlist."""
        rc = self._usermassinfo['pileSizeClientData']['entries']
        return {'tradepile': rc[0]['value'],
                'watchlist': rc[2]['value']}
    #
    # def stats(self):
    #     """Return all stats."""
    #     # TODO: add self.urls['fut']['Stats']
    #     # won-draw-loss
    #     rc = self.__get__(self.urls['fut']['user'])
    #     data = {
    #         'won': rc['won'],
    #         'draw': rc['draw'],
    #         'loss': rc['loss'],
    #         'matchUnfinishedTime': rc['reliability']['matchUnfinishedTime'],
    #         'finishedMatches': rc['reliability']['finishedMatches'],
    #         'reliability': rc['reliability']['reliability'],
    #         'startedMatches': rc['reliability']['startedMatches'],
    #     }
    #     # leaderboard
    #     url = '{0}/alltime/user/{1}'.format(self.urls['fut']['LeaderboardEntry'], self.persona_id)
    #     rc = self.__get__(url)
    #     data.update({
    #         'earnings': rc['category'][0]['score']['value'],    # competitor
    #         'transfer': rc['category'][1]['score']['value'],    # trader
    #         'club_value': rc['category'][2]['score']['value'],  # collector
    #         'top_squad': rc['category'][3]['score']['value']    # builder
    #     })
    #     return data
    #
    # def clubInfo(self):
    #     """Return getReliability."""
    #     # TODO?: return specific club
    #     rc = self.__get__(self.urls['fut']['user'])
    #     return {
    #         'personaName': rc['personaName'],
    #         'clubName': rc['clubName'],
    #         'clubAbbr': rc['clubAbbr'],
    #         'established': rc['established'],
    #         'divisionOffline': rc['divisionOffline'],
    #         'divisionOnline': rc['divisionOnline'],
    #         'trophies': rc['trophies'],
    #         'seasonTicket': rc['seasonTicket']
    #     }

    def messages(self):
        """Return active messages."""
        method = 'GET'
        url = 'activeMessage'

        rc = self.__request__(method, url)
        try:
            return rc['activeMessage']
        except:
            raise UnknownError('Invalid activeMessage response')  # is it even possible?
    #
    # def messageDelete(self, message_id):
    #     """Delete the specified message, by id.
    #
    #     :params message_id: Message id.
    #     """
    #     url = '{0}/{1}'.format(self.urls['fut']['ActiveMessage'], message_id)
    #     self.__delete__(url)

    def buyPack(self, pack_id, currency='COINS'):
        # TODO: merge with openPack
        method = 'POST'
        url = 'purchased/items'

        # pinEvents
        events = [self.pin.event('page_view', 'Hub - Store')]
        self.pin.send(events)

        data = {'packId': pack_id,
                'currency': currency}
        rc = self.__request__(method, url, data=json.dumps(data))

        # pinEvents
        # events = [self.pin.event('page_view', 'Unassigned Items - List View')]
        # self.pin.send(events)

        return rc  # TODO: parse response

    def openPack(self, pack_id):
        method = 'POST'
        url = 'purchased/items'

        data = {"packId": pack_id,
                "currency": 0,  # what is it?
                "usePreOrder": True}
        rc = self.__request__(method, url, data=json.dumps(data))
        return rc  # TODO: parse response

    def sbsSets(self):
        method = 'GET'
        url = 'sbs/sets'

        rc = self.__request__(method, url)

        # pinEvents
        events = [self.pin.event('page_view', 'Hub - SBC')]
        self.pin.send(events)

        return rc  # TODO?: parse

    def sbsSetChallenges(self, set_id):
        method = 'GET'
        url = 'sbs/setId/%s/challenges' % set_id

        rc = self.__request__(method, url)

        # pinEvents
        events = [self.pin.event('page_view', 'SBC - Challenges')]
        self.pin.send(events)

        return rc  # TODO?: parse

    def sbsSquad(self, challenge_id):
        method = 'GET'
        url = 'sbs/challenge/%s/squad' % challenge_id

        rc = self.__request__(method, url)

        # pinEvents
        events = [self.pin.event('page_view', 'SBC - Squad')]
        self.pin.send(events)

        return rc

    def objectives(self, scope='all'):
        method = 'GET'
        url = 'user/dynamicobjectives'

        params = {'scope': scope}
        rc = self.__request__(method, url, params=params)
        return rc
