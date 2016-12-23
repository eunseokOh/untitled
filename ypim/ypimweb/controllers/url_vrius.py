#-*- encoding:utf-8 -*-

import requests, time, random, math

def Url_virus(url):
    appkey = ['fe24c81680b5bf5d850e84ce64de8529d9e67379e9f4431f3327427cc1530609',
              'f2481931110c4c832bd9344f5e8753d07b226118dabb5450e77657885c2c060b',
              'ff0f9d5a2fa172e0ad30f53e7eece3abd1e188f877fd47d13b34cf60bf6a3651',
              '8c5ef04280c63b6b4a63dd7a9223b2d3bed744dcc5a3c2b569d6203af1c253ca',
              'a7ee9941675d45902d39d4172d44905483ae4e7dec37df85f633409488d06c14']

    appkey_rannum = int(math.ceil(random.random() * 5)-1)

    headers = {
      "Accept-Encoding": "gzip, deflate",
      "User-Agent" : "gzip,  eunseokOh"
      }
    params = {'apikey': appkey[appkey_rannum], 'resource':url, 'scan' :1}
    try:
        response = requests.post('https://www.virustotal.com/vtapi/v2/url/report', params=params, headers=headers)
        if (len(response.json()) > 8):
            pass
        else:
            time.sleep(7)
            response = requests.post('https://www.virustotal.com/vtapi/v2/url/report', params=params, headers=headers)

        return response.json()
    except Exception as e:
        print e
        return "Virus total app key Error"