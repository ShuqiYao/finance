# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/11/23

from io import StringIO


from fdfs_client.client import *
#上传文件
client = Fdfs_client(conf_path ='h://hc_project/kg-model-server/client.conf')
#提交文件
file_name = 'h://test/test.txt'
ret = client.upload_by_filename(file_name)
print('http://10.100.34.19:1281' +'/' + ret['Remote file_id'].replace('\\','/'))
# # print client.tracker_query_storage_stor_without_group()
#
#
# tc = Tracker_client(client.tracker_pool)
# # store_serv = tc.tracker_query_storage_stor_without_group('newsimg')
# # store_serv = tc.tracker_query_storage_stor_with_group('newsimg')
# store_serv = tc.tracker_query_storage_stor_with_group('group1')
# print store_serv.group_name