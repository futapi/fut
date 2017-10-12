# -*- coding: utf-8 -*-

"""
fut.pin
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut's pinEvents methods.

"""

import requests
import re
import json
from datetime import datetime

from fut.config import headers
from fut.exceptions import FutError


class Pin(object):
    def __init__(self, sku='FIFA18WEB', sid='', nucleus_id=0, persona_id='', dob=False, platform=False):
        self.sku = sku
        self.sid = sid
        self.nucleus_id = nucleus_id
        self.persona_id = persona_id
        self.dob = dob
        self.platform = platform
        rc = requests.get('https://www.easports.com/fifa/ultimate-team/web-app/config/config.json').text
        self.url = re.search('"pinURL": "(.+?)",', rc).group(1)
        rc = requests.get('https://www.easports.com/fifa/ultimate-team/web-app/js/compiled_1.js').text
        self.taxv = re.search('PinManager.TAXONOMY_VERSION=([0-9\.]+?)', rc).group(1)
        self.tidt = re.search('PinManager.TITLE_ID_TYPE="(.+?)"', rc).group(1)
        self.rel = re.search('rel:"(.+?)"', rc).group(1)
        self.gid = re.search('gid:([0-9]+?)', rc).group(1)
        self.plat = re.search('plat:"(.+?)"', rc).group(1)
        self.et = re.search('et:"(.+?)"', rc).group(1)
        self.pidt = re.search('pidt:"(.+?)"', rc).group(1)

        self.r = requests.Session()
        self.r.headers = headers
        self.r.headers['Origin'] = 'https://www.easports.com'
        self.r.headers['Referer'] = 'https://www.easports.com/fifa/ultimate-team/web-app/'
        self.r.headers['x-ea-game-id'] = self.sku
        self.r.headers['x-ea-game-id-type'] = self.tidt
        self.r.headers['x-ea-taxv'] = self.taxv

        self.custom = {"networkAccess": "W"}  # wifi?
        # TODO?: full boot process when there is no session (boot start)

        self.custom['service_plat'] = platform
        self.s = 4  # event id  |  3 before "was sent" without session/persona/nucleus id so we can probably omit

    def __ts(self):
        # TODO: add ability to random something
        ts = datetime.now()
        ts = ts.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        return ts

    def event(self, en, pgid=False, status=False, source=False, end_reason=False):  # type=False
        data = {"core": {"s": self.s,
                         "pidt": self.pidt,
                         "pid": self.persona_id,
                         "pidm": {"nucleus": self.nucleus_id},
                         "didm": {"uuid": "0"},  # what is it?
                         "ts_event": self.__ts(),
                         "en": en},
                'userid': self.persona_id,  # not needed before session?
                'type': 'utas'}  # not needed before session?
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

        if en == 'page_view':
            data['type'] = 'menu'

        self.s += 1  # bump event id

        return data

    def send(self, events):
        data = {"taxv": self.taxv,  # convert to float?
                "tidt": self.tidt,
                "tid": self.sku,
                "rel": self.rel,
                "v": "18.0.0",  # TODO: where is it from?
                "ts_post": self.__ts(),  # TODO: random delay between event and post (0.5-2s?)
                "sid": self.sid,
                "gid": self.gid,  # convert to int?
                "plat": self.plat,
                "et": self.et,
                "loc": "en_US",
                "is_sess": self.sid != '',
                "custom": self.custom,
                "events": events}
        rc = self.r.post(self.url, data=json.dumps(data)).json()
        if rc['status'] != 'ok':
            raise FutError('PinEvent is NOT OK, probably they changed something.')
        return True
