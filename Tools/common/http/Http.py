# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/9/1

from urllib import request as url_request
import traceback

import http.client,urllib.parse
import json

class Http():
    def __init__(self):
        pass

    def get(self,url=None,headers={}):
        try:
            # print('GET',url)
            request=url_request.Request(url,headers=headers)
            html = url_request.urlopen(request,timeout=2)
            load_data  = html.read()
            return str(load_data,encoding='utf8'),html.getcode()
        except Exception as e:
            # traceback.print_exc()
            pass
        return '',400

    def post(self,url=None,headers={},data=None):
        try:
            # print('POST',url,data)
            request=url_request.Request(url,data=data.encode(encoding='UTF8'))
            html = url_request.urlopen(request,timeout=2)
            load_data  = html.read()
            return str(load_data,encoding='utf8'),html.getcode()
        except Exception as e:
            # print('error',url,data)
            # traceback.print_exc()
            pass
        return '',400

    def postJson(self,url=None,data=None):
        try:
            str = json.dumps(data)
            headers ={'Content-Type':'application/json'}
            conn = http.client.HTTPConnection("10.100.34.19",19996)
            conn.request('POST', '/api/pub', str, headers)
            response = conn.getresponse()
            print(response.status, response.reason)
            data = response.read().decode('utf-8')
            conn.close()
            return data,response.status
        except Exception as e:
            # print('error',url,data)
            # traceback.print_exc()
            pass
        return '',400
