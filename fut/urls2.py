import requests

rc = requests.get('https://www.easports.com/fifa/ultimate-team/web-app/config/config.json').json()
auth_url = rc['authURL']
pin_url = rc['pinURL']  # TODO: urls in dict?
client_id = rc['eadpClientId']
fun_captcha_public_key = rc['funCaptchaPublicKey']
