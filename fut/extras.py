# -*- coding: utf-8 -*-

"""
fut.extras
~~~~~~~~~~~~~~~~~~~~~

This module implements the fut's additional methods.

"""

import requests
from simplejson.scanner import JSONDecodeError


def futheadPrice(item_id, year=18, platform=None):
    params = {'year': year,
              'id': item_id}
    rc = requests.get('http://www.futhead.com/prices/api/', params=params).json()
    if not rc:
        return 0
    rc = rc[str(item_id)]
    xbox = rc['xbLowFive'][0]
    ps = rc['psLowFive'][0]

    if platform == 'xbox':
        price = xbox
    elif platform == 'ps':
        price = ps
    else:
        price = max([xbox, ps])

    return price


def futbinPrice(item_id, platform=None):
    rc = requests.get('https://www.futbin.com/18/playerPrices', params={'player': str(item_id)})
    try:
        rc = rc.json()
    except JSONDecodeError:
        print('futbin response is not valid')
        print(rc.status_code)
        print(rc.url)
        print(rc.content)
        rc = {}
    if not rc:
        return 0
    rc = rc[str(item_id)]['prices']
    if isinstance(rc['xbox']['LCPrice'], str):
        rc['xbox']['LCPrice'] = rc['xbox']['LCPrice'].replace(',', '')
    if isinstance(rc['ps']['LCPrice'], str):
        rc['ps']['LCPrice'] = rc['ps']['LCPrice'].replace(',', '')
    if isinstance(rc['pc']['LCPrice'], str):
        rc['pc']['LCPrice'] = rc['pc']['LCPrice'].replace(',', '')
    xbox = int(rc['xbox']['LCPrice'])
    ps = int(rc['ps']['LCPrice'])
    pc = int(rc['pc']['LCPrice'])

    if platform == 'pc':
        price = pc
    elif platform == 'xbox':
        price = xbox
    elif platform == 'ps':
        price = ps
    else:
        price = max([xbox, ps, pc])

    return price
