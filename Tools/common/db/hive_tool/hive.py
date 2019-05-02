# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/8/31

from subprocess import Popen, PIPE,STDOUT
from Tools.common.db.db_conn import DbConn
from Model.util.logger import info,error,warn
import os

# from pyhive import hive
# from TCLIService.ttypes import TOperationState
# cursor = hive.connect('localhost').cursor()
# cursor.execute('SELECT * FROM my_awesome_data LIMIT 10', async=True)
#
# status = cursor.poll().operationState
# while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
#     logs = cursor.fetch_logs()
#     for message in logs:
#         print(message)
#
#     # If needed, an asynchronous query can be cancelled at any time with:
#     # cursor.cancel()
#
#     status = cursor.poll().operationState
#
# print(cursor.fetchall())



class HiveTool(DbConn):
    """
    mongo 存储工具
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


    def get_connection(self):
        pass

    def select_data(self,find=None,filter=None,table=None):
        if os.path.exists(find):
            script = 'hive -f ' + find
        else:
            script = 'hive -e "' + find + '"'
        data = []
        p = Popen(script, shell=True, stdout=PIPE, stderr=STDOUT)
        for line in p.stdout:
            v= line.decode()
            #适用队列
            data.append(v)
        p.wait()
        if p.returncode != 0:
            error('run_script:::',script)
            raise Exception('ERROR')
        else:
            info('run_script:::',script,'secceed')
            self.cache_context = None
            return data


    def drop_table(self,table_name):
        pass
