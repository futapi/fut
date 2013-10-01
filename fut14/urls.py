# -*- coding: utf-8 -*-

from time import time

# TODO: add timestamp dynamic (just right before every request)

urls = {
    'main_site':    'https://www.easports.com',
    'futweb':       'http://www.easports.com/iframe/fut/?locale=en_GB&baseShowoffUrl=http%3A%2F%2Fwww.easports.com%2Fuk%2Ffifa%2Ffootball-club%2Fultimate-team%2Fshow-off&guest_app_uri=http%3A%2F%2Fwww.easports.com%2Fuk%2Ffifa%2Ffootball-club%2Fultimate-team',
    'fut_config':   'http://www.easports.com/iframe/fut/bundles/futweb/web/flash/xml/site_config.xml',
    'fut_home':     'http://www.easports.com/uk/fifa/football-club/ultimate-team',
    'fut_host':     'https://utas.s2.fut.ea.com:443',  # PC - different on other platforms
    'fut':          {},  # it's updated dynamicly (based on fut_config)
    'fut_question': 'http://www.easports.com/iframe/fut/p/ut/game/fifa14/phishing/question?_=%s' % time(),
    'fut_validate': 'http://www.easports.com/iframe/fut/p/ut/game/fifa14/phishing/validate',

    'shards':       'http://www.easports.com/iframe/fut/p/ut/shards?_=%s' % time(),
    'acc_info':     'http://www.easports.com/iframe/fut/p/ut/game/fifa14/user/accountinfo?_=%s' % time(),
}
