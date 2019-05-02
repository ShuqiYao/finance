# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/7/15


from abc import abstractmethod
from Tools.common.db.mysql_tool.table import table,column


class DbConn():
    """
    中的
    """
    def __init__(self,DBRPC=None,db_name=None,table_name=None,db_host=None,db_port=None,username=None,password=None):
        if(db_name is not None):
            self.db_name=db_name
            self.db_host=db_host
            self.db_port=db_port
            self.username=username
            self.password=password
            self.table_name=table_name
        else:
            if(DBRPC is not None):
                self.db_name = DBRPC.db_name
                self.db_host = DBRPC.db_host
                self.db_port = DBRPC.db_port
                self.username = DBRPC.username
                self.password = DBRPC.password
                self.table_name = DBRPC.table_name
        self.client = None

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def change_table(self,table_name=None):
        pass

    def find(self,table_name,count):
        pass

    def create_table_by_data(self,table_name,table_comm,*args):
        table_obj = table.table(table_name,table_comm)
        for key in range(0,args.__len__()-1,3):
            # print 'key:',args[key]
            name=args[key]
            cla=args[key+1]
            com=args[key+2]
            table_obj.add_column(column.column(name,cla,com))
        self.create_table(table_obj)

    def __del__(self):
        if self.client is not None:
            self.close()


    @abstractmethod
    def create_table(self,table):
        pass

    @abstractmethod
    def select_data(self,find=None,filter=None,table=None):
        pass

    @abstractmethod
    def drop_table(self,table_name):
        pass

    @abstractmethod
    def insert_data(self,data,table_name):
        pass
    @abstractmethod
    def update_data(self,json_data,parkey=None,up_vals=None,table_name=None):
        pass
