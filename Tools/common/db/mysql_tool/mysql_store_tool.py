# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/7/15

import pymysql
# import MySQLdb, cPickle

from Tools.common.db.db_conn import DbConn
from pymysql import IntegrityError

import traceback
import sys

class MysqlStoreTool(DbConn):
    """
    mysql 存储工具 class MysqlTool(DbConn):
    """
    #
    #
    # def __init__(self,db_name,db_host,db_port,username=None,password=None,table_name='test'):
    #     self.db_name = db_name
    #     self.db_host = db_host
    #     self.db_port = db_port
    #     self.username = username
    #     self.password = password
    #     self.table_name = table_name
    #     #self.count=0
    #     __debug__


    def get_connection(self):
        """
        建立 链接
        :return:
        """
        self.client = pymysql.connect(host=self.db_host, user=self.username, passwd=self.password, db=self.db_name,
                                      port=self.db_port,charset="utf8")

    def close(self):
        """
        关闭连接
        :return:
        """
        self.client.close()

    def create_table(self,table):
        """
        创建表
        :param table: 表名
        :return:
        """
        cur= self.client.cursor()
        # cur.execute('set names \'utf8\'')
        cur.execute('drop table if exists '+table.table_name)
        # print "create_table:",table.get_create_table_sql()
        cur.execute(table.get_create_table_sql())
        cur.close()
        self.client.commit()

    def update_data(self,json_data,parkey=None,up_vals=None,table_name=None):
        con = 0
        if(parkey is None or up_vals is None):
            return
        if(table_name is None):
            sql = "UPDATE "+self.table_name
        else:
            sql = "UPDATE "+table_name
        sql2 = " SET "
        for key in up_vals:
            con += 1
            if(con > 1 ):
                sql2 += ","
            sql2 += key + " = "
            if(json_data.has_key(key)):

                if(isinstance(json_data[key],str)):
                    if json_data[key].startswith('func:'):
                        sql2 += json_data[key].replace('func:','')
                    else:
                        sql2 += "'" + json_data[key].replace('\'','') + "'"
                else:
                    if(json_data[key] is None):
                        sql2 += 'null'
                    else:
                        sql2 += str(json_data[key])
            else:
                sql2 += 'null'
        sql += sql2
        sql3 = ' WHERE '
        con = 0
        for key in parkey:
            if con >0:
                sql3 +=' AND '
            con += 1
            if json_data[key] is None:
                sql3 += key + ' is null '
            else:
                sql3 += key + ' = '
                if(isinstance(json_data[key],str)):
                    sql3 +=  "'" + json_data[key].replace('\'','') + "'"
                else:
                    sql3 +=  str(json_data[key])

        sql += sql3
        sql = sql.encode('utf-8')
        # print sql
        try:
            cur= self.client.cursor()
            #print "insert:"+sql
            cur.execute(sql)
            cur.close()
            self.client.commit()
        except Exception as e:
            traceback.print_exc()
            # var = traceback.format_exc()
            if(isinstance(e,IntegrityError)):
                raise e
            elif('MySQL server has gone away' in str(e)):
                try:
                    self.client.close()
                except Exception  as e2:
                    pass
                self.get_connection()
                cur= self.client.cursor()
                #print "insert:"+sql
                cur.execute(sql.encode('utf-8'))
                cur.close()
                self.client.commit()
            else:
                try:
                    self.client.close()
                    self.get_connection()
                    cur= self.client.cursor()
                    #print "insert:"+sql
                    cur.execute(sql.encode('utf-8'))
                    cur.close()
                    self.client.commit()
                except Exception  as e2:
                    raise e2
                    pass


        pass


    def drop_table(self,table_name):
        """
        删除表
        :param table_name: 表名
        :return:
        """
        cur= self.client.cursor()
        cur.execute('DROP TABLE IF EXISTS ' + table_name)
        cur.close()
        self.client.commit()

    def sql(self,sql=None):
        cur= self.client.cursor()
        cur.execute(sql)
        cur.close()
        self.client.commit()

    def select_data(self,find=None,filter=None,table=None):
        """
        select
        :param sql: sql
        :return:
        """
        try:
            print('sql',find)
            cur =self.client.cursor()
            count=cur.execute(find)
            # cur.scroll(0,mode='absolute')
            results=cur.fetchall()
            index = cur.description
            self.client.commit()
            cur.close()
            return results,index
        except Exception as e:
            traceback.print_exc()
            try:
                self.get_connection()
                cur =self.client.cursor()
                count=cur.execute(find)
                # cur.scroll(0,mode='absolute')
                results=cur.fetchall()
                index = cur.description
                self.client.commit()
                cur.close()
                return results,index
            except Exception as e:
                traceback.print_exc()
            return [],[]



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
        con = 0
        if(table_name is None):
            sql = "INSERT INTO "+self.table_name+"("
        else:
            sql = "INSERT INTO "+table_name+"("
        sql2 = " VALUES("
        for key in dict.keys():
            con += 1
            if(con > 1 ):
                sql += ","
                sql2 += ","
            if(isinstance(dict[key],str)):
                if dict[key].startswith('func:'):
                    sql2 += dict[key].replace('func:','')
                else:
                    sql2 += "'"+dict[key].replace('\'','')+"'"
            else:
                if(dict[key] is None):
                    sql2 += 'null'
                else:
                    sql2 += str(dict[key])
            sql += key
        sql += ")"
        sql2 += ")"
        sql += sql2
        # print sql
        try:
            cur= self.client.cursor()
            #print "insert:"+sql
            cur.execute(sql.encode('utf-8'))
            cur.close()
            self.client.commit()
        except Exception as e:
            traceback.print_exc()
            # var = traceback.format_exc()
            if(isinstance(e,IntegrityError)):
                raise e
            elif('MySQL server has gone away' in str(e)):
                try:
                    self.client.close()
                except Exception  as e2:
                    pass
                self.get_connection()
                cur= self.client.cursor()
                #print "insert:"+sql
                cur.execute(sql.encode('utf-8'))
                cur.close()
                self.client.commit()
            else:
                raise e

        # mutex.release()

if __name__== "__main__":
    # mysql=MysqlStoreTool('dim_bak','10.10.202.16',3306,'root','1234abcd','test')
    # mysql.get_connection()
    # #mysql.select_data("select * from lablesystem_warehouse_databases_table");
    # mysql.create_table_by_data("test",'asdflasdjf','id','int(11)','主键','name','varchar(30)','姓名')
    # data={'id':1,'name':'lie.tian'}
    # mysql.insert_data(data)
    # mysql.insert_data(data)
    # mysql.insert_data(data)
    # mysql.insert_data(data)
    #
    # mysql.close()
    json_in ={}
    json_in['id'] = 232432
    json_in['id_2'] = 'asdf'
    json_in['name'] = 'asdfasdf'
    json_in['va'] = 3
    par = ['id','id_2']
    up  = ['name','va']
    # update_data(json_data=json_in,parkey=par,up_vals=up,table_name='test')
