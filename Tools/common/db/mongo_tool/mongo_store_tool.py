# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/7/15

import pymongo

from Tools.common.db.db_conn import DbConn

import traceback


#conn = pymongo.Connection('127.0.0.1', port=27017)
import sys

class MongoStoreTool(DbConn):
    


    def get_connection(self):
        #print 'connction:',self.db_host, self.db_port
        self.client= pymongo.MongoClient(host=self.db_host, port=self.db_port)
        #admin 数据库有帐号，连接-认证-切换库
        db_auth = self.client[self.db_name]
        # print 'auth:',self.username, self.password
        if(self.username is not None):
            # print 'user,pwd,',self.username,self.password
            db_auth.authenticate(self.username,self.password)
        #建立数据库连接
        self.db=self.client[self.db_name]

        self.db.collection_names()
        self.table = None
        if(self.table_name is not None):
            self.table=self.db[self.table_name]

    def re_connection(self):
        self.get_connection()

    def change_table(self,table_name):
        self.table = self.db[table_name]
        self.table_name = table_name

    def update_data(self,json_data,parkey=None,up_vals=None,table_name=None):
        #只更新1个
        if(len(parkey)==1):
            parkey_s={}
            for k in parkey:
                #主键不能为空
                parkey_s[k] =  json_data[k]
            up_s = {}
            for k in up_vals:
                if(json_data.has_key(k)):
                    up_s[k] = json_data[k]
                else:
                    pass
            self.table.update(parkey_s,{'$set':up_s}, False,False)
        else:
            parkey_s =[]
            for k in parkey:
                parkey_s.append({k:json_data[k]})
            up_s = {}
            for k in up_vals:
                if(json_data.has_key(k)):
                    up_s[k] = json_data[k]
                else:
                    pass
                    #up_s[k] = ''
            # print 'parkey_s',parkey_s
            #print 'up_s',up_s
            self.table.update({'$and':parkey_s},{'$set':up_s}, False,False)
        pass

    def find(self,table_name,count):
        return list(self.db[table_name].find().limit(count))

    def get_table(self,table_name):
        return self.db[table_name]

    def info(self):
        """
        获取db的属性
        :return:
        """
        # print self.client.server_info()
        # print self.client.database_names()

        info_l ={}
        re =[]
        info_l['collections']=re
        info_l['db_name'] =self.db_name
        info_l['version'] =self.client.server_info()['version']
        info_l['db_status'] =self.db.command({'dbstats':1})
        list =self.db.collection_names()
        for li in list:
            if(li =='system.indexes'):
                continue
            re.append({'name':li,'count':self.db[li].count()})
        return info_l

    def close(self):
        if self.client is not None:
            self.client.close()
        pass

    def remove(self,find=None):
        self.table.remove(find)

    def create_table(self,table):
        pass

    def select_data(self,find=None,filter=None,table=None):
        try:
            if table == self.table_name:
                return self.db[table].find(find,filter)
            else:
                return self.table.find(find,filter)
            pass
        except Exception as e :
            traceback.print_exc()
            self.re_connection()
            return []

    def query(self,find= None,filter=None,count = None):
        if find is None:
            find1= {}
        else:
            find1 = find
        if filter is None:
            filter1 = {}
        else:
            filter1 = filter

        if count is None:
            return self.table.find(find1,filter1)
        else:
            return self.table.find(find1,filter1).limit(count)
        pass

    def drop_table(self,table_name):
        pass

    def insert_data(self,dict,table_name=None,flag=True):
        #print 'val1:',data
        if isinstance(dict,list):
            self.table.insert(dict)
        else:
            self.table.insert([dict])
        # ll = {}
        # for key in dict.keys():
        #     if key == 'par_key':
        #         continue
        #     if key == 'up_vals':
        #         continue
        #     ll[key] = dict[key]
        #
        # self.table.insert(ll)
        #print 'val2:',data

    def insert_all_data(self,dict,table_name=None,flag=True):
        self.table.insert(dict)

import json
if __name__=="__main__":
    mongo= MongoStoreTool(db_name="kg_db",table_name='kg_finc_stock_company',db_host="10.100.34.19",db_port=9017)
    mongo.get_connection()
    # mongo.insert_data({"name":"tianlie","address":"china","val":22.3})
    # print mongo.select_data({});
    print(json.dumps(mongo.info(),ensure_ascii=False))
    print(mongo.find('wangyi',10))