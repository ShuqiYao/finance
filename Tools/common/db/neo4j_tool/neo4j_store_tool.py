# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/7/15

from neo4j.v1 import GraphDatabase, basic_auth

from Tools.common.db.db_conn import DbConn

import traceback
import sys
import time
import traceback

class Neo4jStoreTool(DbConn):
    """
    neo4j 存储工具 class Neo4jStoreTool(DbConn):
    """

    def get_connection(self):
        """
        建立 链接
        :return:
        """
        self.clientGraph = GraphDatabase.driver("bolt://" + self.db_host + ":" + str(self.db_port), auth=basic_auth(self.username, self.password), encrypted=False)

    def re_connection(self):
        try:
            if self.clientGraph.closed():
                self.get_connection()
        except Exception as e :
            traceback.print_exc()
            time.sleep(600)

    def close(self):
        """
        关闭连接
        :return:
        """
        self.clientGraph.close()

    def create_table(self,table):
        """
        创建表
        :param table: 表名
        :return:
        """
        pass

    def update_data(self,json_data,parkey=None,up_vals=None,table_name=None):
        pass


    def drop_table(self,table_name):
        """
        删除表
        :param table_name: 表名
        :return:
        """
        pass

    def sql(self,sql=None):
        # self.client.run(sql)
        pass

    def select_data(self,find=None,filter=None,table=None):
        """
        select
        :param sql: sql
        :return:
        """
        try:
            print('cypher',find)
            client = self.clientGraph.session()
            vals = client.run(find)
            return vals
        except Exception as e:
            traceback.print_exc()
            self.re_connection()
            client = self.clientGraph.session()
            vals = client.run(find)
            return vals


    def insert_data(self,dict,table_name=None,flag=True):
        # print 1
        """
        插入表数据
        :param table_name: 表
        :param data: 对应jsondata
        :return:
        """
        # mutex = threading.Lock()
        # mutex.acquire()
        #print 'dict',dict
        pass

        # mutex.release()

if __name__== "__main__":

    # neo4j = Neo4jStoreTool(db_name="None",table_name="None",db_host="10.100.22.94",db_port=9687,username="neo4j",password="neo4j0fcredithc")
    # neo4j.get_connection()
    # vals = neo4j.select_data(find="match(p:PERSON) return p limit 5")
    # for v in vals:
    #     print(v)
    neo4j = Neo4jStoreTool(db_name="None",table_name="None",db_host="10.100.22.93",db_port=8687,username="neo4j",password="neo4j0fcredithc")
    neo4j.get_connection()
    vals = neo4j.select_data(find="match(p:Person) return p limit 5")
    for v in vals:
        print(v)
