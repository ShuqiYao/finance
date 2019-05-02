# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/8/24


import json
import sys

from Tools.common.enum.enums import DB_STORE_ENUM
import traceback
from Tools.common.db.db_code import code_al



class DBRPC():

    def __init__(self,json_str=None,query=None,driver = None,table_name=None,db_name=None,db_host=None,db_port=None,username=None,password=None,is_pw_encode=False):
        """
        :param json_str: 如果传入为json_str则需要转化为对应的DBRPC
        :param query: 如果是 本地文件则对应为 目录或文件的[] 或者为 sql
        :return:
        """
        # print 'json_str',json_str
        # print 'setting',setting
        # print 'driver',driver
        self.query = query
        self.table_name = None
        self.db_name =None
        self.db_host =None
        self.db_port = None
        self.username = None
        self.password = None
        self.driver = DB_STORE_ENUM.MONGODB
        if(json_str is not None and len(json_str)>2):
            js = json_str
            self.table_name = js['table_name']
            self.driver_bak = js['driver']
            if(self.driver_bak =='DB_STORE_ENUM.MYSQL'):
                self.driver = DB_STORE_ENUM.MYSQL
                self.db_name = js['db_name']
                self.db_host = js['db_host']
                self.db_port = js['db_port']
                self.username = js['username']
                self.password = js['password']
                if(self.password is not None):
                    if is_pw_encode is not None and is_pw_encode:
                        self.password = code_al.decrypt(self.password)
            elif(self.driver_bak =='DB_STORE_ENUM.MONGODB'):
                self.driver = DB_STORE_ENUM.MONGODB
                self.db_name = js['db_name']
                self.db_host = js['db_host']
                self.db_port = js['db_port']
                if(js['username'] is None):
                    self.username = None
                else:
                    self.username = js['username']
                if(js['password'] is None):
                    self.password = None
                else:
                    self.password = js['password']
                if(self.password is not None):
                    if is_pw_encode is not None and is_pw_encode:
                        self.password = code_al.decrypt(self.password)
            elif(self.driver_bak == 'DB_STORE_ENUM.LOCAL_FILE'):
                self.driver = DB_STORE_ENUM.LOCAL_FILE
            elif(self.driver_bak == 'DB_STORE_ENUM.FILE_OBJCT'):
                self.driver = DB_STORE_ENUM.FILE_OBJCT
            elif(self.driver_bak == 'DB_STORE_ENUM.ELASTICSEARCH'):
                self.driver = DB_STORE_ENUM.ELASTICSEARCH
                self.db_host = js['db_host']
                self.db_port = js['db_port']
                self.db_name = js['db_name']
                self.username = js['username']
                self.password = js['password']
            else:
                self.driver = None

        else:
            if(db_name is not None and db_host is not None and db_port is not None):
                self.db_name=db_name
                self.db_host = db_host
                self.db_port = db_port
                self.username = username
                self.password = password
                self.table_name = table_name
                self.driver = driver


    # print 'dict-------------------------------',.dict()



    def dict(self):
        return {'driver':str(self.driver),'db_name':self.db_name,'db_host':self.db_host,
                'db_port':self.db_port,'username':self.username,
                # 'password':self.password,
                'table_name':self.table_name}

    def __str__(self):
        return json.dumps(dict(),ensure_ascii=False)



