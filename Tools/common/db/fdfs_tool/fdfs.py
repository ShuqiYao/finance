# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/9/27
from fdfs_client.client import *
import traceback
import sys
from fdfs_client.client import *

class FdfsTool():

    def __init__(self,conf_path=None,ip_port='http://10.100.34.19:1281'):
        """
        加载配置文件
        :param conf_path:  地址在 项目路径的 client.conf
        :param ip_port: 默认ip 及 端口
        :return:
        """
        #上传文件
        self.client = Fdfs_client(conf_path =conf_path)
        self.ip_port = ip_port


    def upload_file(self,file_path=None):
        """
        上传文件
        :param file_path: 文件地址
        :return: 对应的fdfs 绝对地址
        """
        print('upload file',file_path)
        ret = self.client.upload_by_filename(file_path)
        #print( self.ip_port +'/' + ret['Remote file_id'].replace('\\','/'))
        return self.ip_port +'/' + ret['Remote file_id'].replace('\\','/')
