# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/9/1


from Tools.common.db.db_conn import DbConn
from Tools.common.db.mysql_tool.mysql_store_tool import MysqlStoreTool
from Tools.common.db.mongo_tool.mongo_store_tool import MongoStoreTool
from Tools.common.db.file_tool.file_tool import FileStoreTool

# from Tools.common.db.redis_tool.redis_queue_tool import RedisQueueTool
from Tools.common.enum.enums import DB_STORE_ENUM
from Tools.common.db.file_tool.file_tool import FieldObjectStoreTool
from Tools.common.db.es_tool.es_store_tool import EsStoreTool
from Tools.common.db.db_rpc import DBRPC

class DBCONN():

    setting = None
    #对应的入库工具箱
    driver= None #DB_STORE_ENUM.LOCAL_FILE
    #工程名
    name = "test"
    table_name = 'test'
    dbrpc = None

    #远程存储地址信息
    db_name = None
    db_host = None
    db_port = None
    username = None
    password = None


    def __init__(self,setting=None,driver=None,dbrpc=None):
        self.setting= setting
        self.dbrpc=dbrpc
        if driver is not None:
            self.driver =driver
        pass

    def init_db(self):
        """
        初始化job
        :return:
        """
        #统计工具组件#如果为传参修改的地址则使用这个
        if self.dbrpc is None:
            self.dbrpc = DBRPC(driver=self.driver,table_name = self.table_name,db_name=self.db_name,db_host=self.db_host,db_port=self.db_port,username=self.username,password=self.password)
        self.client=DbConn()
        if(self.dbrpc.driver == DB_STORE_ENUM.MYSQL):
            #self.client = MysqlStoreTool(self.setting["mysql_database"],self.setting["mysql_ip"],self.setting["mysql_port"],self.setting["mysql_user"],self.setting["mysql_pwd"])#'dim_bak','10.10.202.16',3306,'root','1234abcd')
            self.client = MysqlStoreTool( self.dbrpc)
        elif(self.dbrpc.driver == DB_STORE_ENUM.MONGODB):
            #self.client = MongoStoreTool(self.setting["mongo_database",self.table_name,
                                                    #self.setting["mongo_ip"],self.setting["mongo_port"],
                                                    #self.setting["mongo_user"],self.setting["mongo_pwd"],])#MongoStoreTool("test","test","192.168.17.128",27017)
            self.client = MongoStoreTool( self.dbrpc)
        elif(self.dbrpc.driver == DB_STORE_ENUM.LOCAL_FILE):
            if "LOCAL_STORE" in self.setting:
                self.client = FileStoreTool(is_write=True,
                                            dir=self.setting["LOCAL_STORE"],name=self.setting["LOCAL_STORE_FILE"])
            else:
                self.client = FileStoreTool(is_write=False,
                                            dir=None,name=None)#本地文件
        elif(self.dbrpc.driver == DB_STORE_ENUM.HDFS_FILE):#hdfs目录
            self.client = None
        elif(self.dbrpc.driver == DB_STORE_ENUM.KAFKA):#kafka
            self.client = None
        elif(self.dbrpc.driver == DB_STORE_ENUM.HBASE):#hbase
            self.client = None
        elif(self.dbrpc.driver == DB_STORE_ENUM.FILE_OBJCT):
            self.client = FieldObjectStoreTool(self.setting["LOCAL_STORE"])
        elif(self.dbrpc.driver == DB_STORE_ENUM.ELASTICSEARCH):
            self.client = EsStoreTool(self.dbrpc)
        else:
            print('self.driver : 配置错误')
        self.client.get_connection()

    def change_table(self,table_name=None):
        return self.client.change_table(table_name=table_name)

    def find(self,table_name,count):
        return self.client.find(table_name,count)

    def select_data(self,find=None,filter=None,table=None):
        return self.client.select_data(find=find,filter=filter,table=table)



    def insert_data(self,data,table_name):
        self.client.insert_data(data,table_name=table_name)
        pass

    def update_data(self,json_data,parkey=None,up_vals=None,table_name=None):
        self.client.update_data(json_data,parkey=parkey,up_vals=up_vals,table_name=table_name)
        pass