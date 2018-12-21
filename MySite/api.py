from urllib.parse import quote
from hashlib import md5
from http import client
import random
import json


appapi = '20181219000250051'
secret_key = 'CGdPIHU85U94OJTw6KwH'


def get_sign(salt, query):
    sign = appapi + query + str(salt) + secret_key
    m = md5()
    m.update(sign.encode('utf-8'))
    return m.hexdigest()


def trans(query, from_lang='zh', to_lang='en'):
    http_client = None
    salt = random.randint(12345,78901)
    sign = get_sign(salt, query)
    mysurl = '/api/trans/vip/translate'+'?appid='+appapi +'&q='+quote(query)+'&from='+from_lang+ \
             '&to='+to_lang+'&salt='+str(salt)+'&sign='+sign
    try:
        http_client = client.HTTPConnection('api.fanyi.baidu.com')
        http_client.request('GET', mysurl)
        response = http_client.getresponse()
        content = json.loads(response.read())
        return content['trans_result'][0]['dst']
    except Exception as e:
        print('Error: '+ str(e))
    finally:
        if http_client:
            http_client.close()