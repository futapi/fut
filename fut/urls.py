import requests

from .exceptions import FutError

# config
rc = requests.get('https://www.easports.com/fifa/ultimate-team/web-app/config/config.json').json()
auth_url = rc['authURL']
pin_url = rc['pinURL']  # TODO: urls in dict?
client_id = rc['eadpClientId']
fun_captcha_public_key = rc['funCaptchaPublicKey']


# remote config - should be refresh every x seconds
rc = requests.get('https://www.easports.com/fifa/ultimate-team/web-app/content/B1BA185F-AD7C-4128-8A64-746DE4EC5A82/2018/fut/config/companion/remoteConfig.json').json()

if rc['pin'] != {"b": True, "bf": 500, "bs": 10, "e": True, "r": 3, "rf": 300}:
    print('>>> WARNING: ping variables changed: %s' % rc['pin'])

if rc['patch']['f'] != 1800000:  # this is probably dead value
    print('>>> WARNING: patch version changed: %s' % rc['patch']['f'])

if rc['futweb_maintenance']:
    raise FutError('Futweb maintenance, please retry in few minutes.')

# TODO: parse itemsPerPage
# "itemsPerPage": {
# 	"club" : 45,
# 	"transferMarket" : 15
# },


card_info_url = 'https://fifa18.content.easports.com/fifa/fltOnlineAssets/B1BA185F-AD7C-4128-8A64-746DE4EC5A82/2018/fut/items/web/'  # TODO: get hash from somewhere, dynamic year
messages_url = 'https://www.easports.com/fifa/ultimate-team/web-app/loc/en_US.json'
