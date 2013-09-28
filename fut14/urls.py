# -*- coding: utf-8 -*-

from time import time

urls = {

    'main_site':    'https://www.easports.com',
    'login':        'https://www.easports.com/services/authenticate/login',
    'home':         'https://utas.fut.ea.com',
    'home_pc':      'https://utas.s2.fut.ea.com:443',
    'shards':       'http://www.easports.com/iframe/fut/p/ut/shards?_=%s' % time(),
    'acc_info':     'http://www.easports.com/iframe/fut/p/ut/game/fifa14/user/accountinfo?_=%s' % time(),
    #'home_ut':     '',

}
