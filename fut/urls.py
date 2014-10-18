# -*- coding: utf-8 -*-

import requests
import xmltodict
from time import time

from .exceptions import FutError

# TODO: add timestamp dynamic (just right before every request)

def __updateUrls__(urls, cl):
        """Gets services urls."""
        urls['fut_config'] = '%s?cl=%s' %(urls['fut_config'], cl)
        rc = xmltodict.parse(requests.get(urls['fut_config']).content)
        services = rc['main']['services']['prod']
        path = '{0}{1}game/fifa/'.format(urls['fut_host'], rc['main']['directHttpServiceDestination'])
        path_auth = '{0}/iframe/fut15{1}'.format(urls['main_site'].replace('https', 'http'),  # it's not working with ssl...
                                                 rc['main']['httpServiceDestination'])
        for i in services:
            if i == 'authentication':
                urls['fut'][i] = path_auth+services[i]
            else:
                urls['fut'][i] = path+services[i]
        return urls



def urls(platform, cl=None):
    """Returns services urls."""
    urls = {
        'main_site':     'https://www.easports.com',
        'futweb':        'https://www.easports.com/iframe/fut15/?baseShowoffUrl=https%3A%2F%2Fwww.easports.com%2Ffifa%2Fultimate-team%2Fweb-app%2Fshow-off&guest_app_uri=http%3A%2F%2Fwww.easports.com%2Ffifa%2Fultimate-team%2Fweb-app&locale=en_US',
        'fut_config':    'http://www.easports.com/iframe/fut15/bundles/futweb/web/flash/xml/site_config.xml',
        'fut_home':      'http://www.easports.com/uk/fifa/football-club/ultimate-team',
        'fut':           {},  # it's updated dynamicly (based on fut_config)
        'fut_question':  'http://www.easports.com/iframe/fut15/p/ut/game/fifa15/phishing/question?_=%s' % time(),
        'fut_validate':  'http://www.easports.com/iframe/fut15/p/ut/game/fifa15/phishing/validate',

        'fut_host':      {'pc':   'https://utas.s2.fut.ea.com:443',
                          'ps3':  'https://utas.s2.fut.ea.com:443',
                          'xbox': 'https://utas.fut.ea.com:443',
                          'ios':  'https://utas.fut.ea.com:443',
                          'and':  'https://utas.fut.ea.com:443',
                         },

        'shards':        'http://www.easports.com/iframe/fut15/p/ut/shards?_=%s' % time(),
        'acc_info':      'http://www.easports.com/iframe/fut15/p/ut/game/fifa15/user/accountinfo?_=%s' % time(),
        'card_info':     'https://fifa15.content.easports.com/fifa/fltOnlineAssets/8D941B48-51BB-4B87-960A-06A61A62EBC0/2015/fut/items/web/',
    }
    #urls['login'] = requests.get(urls['fut_home']).url

    if platform in urls['fut_host']:
        urls['fut_host'] = urls['fut_host'][platform]
    else:
        raise FutError('Invalid platform. (Valid ones are pc/ps3/xbox/and/ios).')

    if cl:
        return __updateUrls__(urls, cl)
    else:
        return urls
