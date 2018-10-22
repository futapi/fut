# -*- coding: utf-8 -*-

"""
fut.pin
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut's pinEvents methods.

"""

import json
import re
import time
from datetime import datetime
from random import random

import requests

from .config import headers
from .exceptions import FutError
from .urls import pin_url, release_type


class Pin(object):
    def __init__(self, sku=None, sid='', nucleus_id=0, persona_id='', dob=False, platform=False):
        self.sid = sid
        self.nucleus_id = nucleus_id
        self.persona_id = persona_id
        self.dob = dob
        self.platform = platform
        rc = requests.get('https://www.easports.com/fifa/ultimate-team/web-app/js/compiled_1.js').text

        self.taxv = re.search('taxv:"(.+?)"', rc).group(1)
        self.tidt = re.search('tidt:"(.+?)"', rc).group(1)

        self.sku = sku or re.search('enums.SKU.FUT="(.+?)"', rc).group(1)
        self.rel = release_type
        self.gid = re.search('gid:([0-9]+?)', rc).group(1)
        self.plat = 'web'  # where is it? WEB:?
        self.et = re.search('et:"(.+?)"', rc).group(1)
        self.pidt = re.search('pidt:"(.+?)"', rc).group(1)
        self.v = re.search('APP_VERSION="([0-9\.]+)"', rc).group(1)

        self.r = requests.Session()
        self.r.headers = headers
        self.r.headers['Origin'] = 'https://www.easports.com'
        self.r.headers['Referer'] = 'https://www.easports.com/fifa/ultimate-team/web-app/'
        self.r.headers['x-ea-game-id'] = self.sku
        self.r.headers['x-ea-game-id-type'] = self.tidt
        self.r.headers['x-ea-taxv'] = self.taxv

        self.custom = {"networkAccess": "G"}  # wifi?
        # TODO?: full boot process when there is no session (boot start)

        self.custom['service_plat'] = platform[:3]
        self.s = 2  # event id  |  before "was sent" without session/persona/nucleus id so we can probably omit

    def __ts(self):
        # TODO: add ability to random something
        ts = datetime.utcnow()
        ts = ts.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        return ts

    def event(self, en, pgid=False, status=False, source=False, end_reason=False):  # type=False
        data = {
            "core": {
                "en": en,
                "pid": self.persona_id,
                "pidm": {"nucleus": self.nucleus_id},
                "pidt": self.pidt,
                "s": self.s,
                "ts_event": self.__ts()
            }
        }
        if self.dob:  # date of birth yyyy-mm
            data['core']['dob'] = self.dob
        if pgid:
            data['pgid'] = pgid
            # if pgid[:3] == 'Hub':
            #     data['type'] = 'menu'
        # if type:  # yeah i know we're overwriting default namespace but why not?
        #     data['type'] = type
        if status:
            data['status'] = status
        if source:
            data['source'] = source
        if end_reason:
            data['end_reason'] = end_reason

        if en == 'login':
            data['type'] = 'utas'
            data['userid'] = self.persona_id
        elif en == 'page_view':
            data['type'] = 'menu'
        elif en == 'error':
            data['server_type'] = 'utas'
            data['errid'] = 'server_error'
            data['type'] = 'disconnect'
            data['sid'] = self.sid

        self.s += 1  # bump event id

        return data

    def send(self, events, fast=False):
        time.sleep(0.5 + random() / 50)
        data = {
            "custom": self.custom,
            "et": self.et,
            "events": events,
            "gid": self.gid,  # convert to int?
            "is_sess": self.sid != '',
            "loc": "en_US",
            "plat": self.plat,
            "rel": self.rel,
            "sid": self.sid,
            "taxv": self.taxv,  # convert to float?
            "tid": self.sku,
            "tidt": self.tidt,
            "ts_post": self.__ts(),
            "v": self.v
        }
        # print(data)  # DEBUG
        if not fast:
            self.r.options(pin_url)
        rc = self.r.post(pin_url, data=json.dumps(data)).json()
        if rc['status'] != 'ok':
            raise FutError('PinEvent is NOT OK, probably they changed something.')
        return True
