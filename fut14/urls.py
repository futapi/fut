# -*- coding: utf-8 -*-

import requests
import xmltodict
from time import time

from .exceptions import Fut14Error

# TODO: add timestamp dynamic (just right before every request)

def __updateUrls__(urls):
        """Gets services urls."""
        rc = xmltodict.parse(requests.get(urls['fut_config']).content)
        services = rc['main']['services']['prod']
        path = '{0}{1}game/fifa14/'.format(urls['fut_host'], rc['main']['directHttpServiceDestination'])
        path_auth = '{0}/iframe/fut{1}'.format(urls['main_site'].replace('https', 'http'),  # it's not working with ssl...
                                                  rc['main']['httpServiceDestination'])
        for i in services:
            if i == 'authentication':
                urls['fut'][i] = path_auth+services[i]
            else:
                urls['fut'][i] = path+services[i]
        return urls



def urls(platform):
    """Returns services urls."""
    urls = {
        'main_site':     'https://www.easports.com',
        'futweb':        'http://www.easports.com/iframe/fut/?locale=en_US&baseShowoffUrl=http%3A%2F%2Fwww.easports.com%2Fuk%2Ffifa%2Ffootball-club%2Fultimate-team%2Fshow-off&guest_app_uri=http%3A%2F%2Fwww.easports.com%2Fuk%2Ffifa%2Ffootball-club%2Fultimate-team',
        'fut_config':    'http://www.easports.com/iframe/fut/bundles/futweb/web/flash/xml/site_config.xml',
        'fut_home':      'http://www.easports.com/uk/fifa/football-club/ultimate-team',
        'fut':           {},  # it's updated dynamicly (based on fut_config)
        'fut_question':  'http://www.easports.com/iframe/fut/p/ut/game/fifa14/phishing/question?_=%s' % time(),
        'fut_validate':  'http://www.easports.com/iframe/fut/p/ut/game/fifa14/phishing/validate',

        'fut_host':      {'pc':   'https://utas.s2.fut.ea.com:443',  # PC - different on other platforms
                          'ps3':  'https://utas.s2.fut.ea.com:443',
                          'xbox': 'https://utas.fut.ea.com:443',
                          'ios':  'https://utas.fut.ea.com:443',
                          'and':  'https://utas.fut.ea.com:443',
                         },

        'shards':        'http://www.easports.com/iframe/fut/p/ut/shards?_=%s' % time(),
        'acc_info':      'http://www.easports.com/iframe/fut/p/ut/game/fifa14/user/accountinfo?_=%s' % time(),
        'card_info':     'http://cdn.content.easports.com/fifa/fltOnlineAssets/C74DDF38-0B11-49b0-B199-2E2A11D1CC13/2014/fut/items/web/',
    }

    if platform in urls['fut_host']:
        urls['fut_host'] = urls['fut_host'][platform]
    else:
        raise Fut14Error('Invalid platform. (Valid ones are pc/ps3/xbox/and/ios).')

    return __updateUrls__(urls)
