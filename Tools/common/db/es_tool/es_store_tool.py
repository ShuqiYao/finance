# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/12/6

from datetime import datetime
from elasticsearch import helpers
from elasticsearch import Elasticsearch
from Tools.common.db.es_tool.es_tool import EsClient
import traceback


from Tools.common.db.db_conn import DbConn

class EsStoreTool(DbConn):

    def get_connection(self):
        #print 'connction:',self.db_host, self.db_port
        self.client= EsClient(ip=self.db_host,port=self.db_port,index=self.db_name,doc_type=self.table_name)
        #admin 数据库有帐号，连接-认证-切换库

    def re_connection(self):
        self.get_connection()

    def select_data(self,find=None,filter=None,table=None):
        try:
            return self.client.search(query=find)
        except Exception as e :
            traceback.print_exc()
            self.re_connection()
            return []
