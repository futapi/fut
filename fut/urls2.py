import requests

rc = requests.get('https://www.easports.com/fifa/ultimate-team/web-app/config/config.json').json()
auth_url = rc['authURL']
pin_url = rc['pinURL']  # TODO: urls in dict?
client_id = rc['eadpClientId']
fun_captcha_public_key = rc['funCaptchaPublicKey']

card_info_url = 'https://fifa18.content.easports.com/fifa/fltOnlineAssets/B1BA185F-AD7C-4128-8A64-746DE4EC5A82/2018/fut/items/web/'  # TODO: get hash from config/remoteconfig, dynamic year
messages_url = 'https://www.easports.com/iframe/fut18/bundles/futweb/web/flash/xml/localization/messages.en_US.xml'  # TODO: dynamic year
