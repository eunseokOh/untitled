#-*- encoding:utf-8 -*-

import requests, time, random, math
def Url_virus(url):
    appkey = ['fe24c81680b5bf5d850e84ce64de8529d9e67379e9f4431f3327427cc1530609',
              'f2481931110c4c832bd9344f5e8753d07b226118dabb5450e77657885c2c060b',
              'ff0f9d5a2fa172e0ad30f53e7eece3abd1e188f877fd47d13b34cf60bf6a3651',
              '8c5ef04280c63b6b4a63dd7a9223b2d3bed744dcc5a3c2b569d6203af1c253ca',
              'a7ee9941675d45902d39d4172d44905483ae4e7dec37df85f633409488d06c14',
              '460cf47ddb2b5e1ef4a55d74e30dc21ab4e5286a05af6fae54427dedbdd552e7',
              'edf424672bb30ec913a159067014fc7b5f795afc0b9bc9c2eb9c7e790c4dbb3b',
              'f46d44bb4684eb6dba4e0075892c7b675ed68cbc9bfdd6ee26af781b9357bbdc',
              'b70a8ceec83715b2cfadf54392ae84ea0570f5ab2cc107a4a1c45c135df93005',
              '569e7ea7dbac45e960b814482d8d07eae23484d7c1000cbc72ba25a40ce6af48',
              '4a76ccfeb9b5489121c07afb30754964fcc87242d29dfd370bddc6fbe2bdecc8']

    headers = {
      "Accept-Encoding": "gzip, deflate",
      "User-Agent" : "gzip,  eunseokOh"
      }

    check = True
    while(check):
        try:
            appkey_rannum = int(math.ceil(random.random() * len(appkey)) - 1)
            params = {'apikey': appkey[appkey_rannum], 'resource': url, 'scan': 1}

            response = requests.post('https://www.virustotal.com/vtapi/v2/url/report', params=params, headers=headers)
            if (len(response.json()) > 8):
                pass
            else:
                time.sleep(7)
                response = requests.post('https://www.virustotal.com/vtapi/v2/url/report', params=params, headers=headers)
            check = False
            return response.json()

        except Exception as e:
            print e
            continue