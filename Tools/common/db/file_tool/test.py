# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/7/25

import urllib
import urllib2
import cookielib
import json
import os
import sys
import StringIO
import gzip

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from PIL import Image


def persist_file(path, buf, meta=None, headers=None):
    absolute_path = _get_filesystem_path(path)
    # self._mkdir(os.path.dirname(absolute_path), info)
    with open(absolute_path, 'wb') as f:
        f.write(buf.getvalue())

def _get_filesystem_path(path):
    # path_comps = path.split('/')
    return os.path.join(path)

# url="http://www.baidu.com/s"
# url="http://avatar.csdn.net/D/D/B/1_deqingguo.jpg"
# url ="http://pdf.dfcfw.com/pdf/H3_AP201607250016724856_1.pdf"
# url = "http://news.gtimg.cn/more.php?q=usJD&page=1"
# url = 'http://n.sinaimg.cn/finance/a3465db7/20161025/109958538365484335.png'
url = "http://inews.gtimg.com/newsapp_match/0/902571813/0"
header ={'Accept-Language': ['en'], 'User-Agent': ['Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1']}
request=urllib2.Request(url,headers=header)
data = urllib2.urlopen(request).read()
# print data
dir ="H:\\test2\\ant_test"
# # #
# # # table_name = "xxxx.jpg"
table_name ="test2.jpg"
path = os.path.join(dir,os.path.basename(table_name))
print 'path:',path
# # print data.decode('gbk')
# # dir = "h"
#
# # 图片
#
# orig_image = Image.open(BytesIO(data))

# width, height = orig_image.size
# # orig_image = orig_image.convert('RGB')
# persist_file(path,BytesIO(data))
# orig_image.save(path,'jpg')

def gzdecode(data) :
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read()   # 读取解压缩后数据
    return data2
#orig_image = Image.open(BytesIO(gzdecode(data)))
orig_image = Image.open(BytesIO(data))
orig_image.save(path)
# 其他文件
from fdfs_client.client import *
# #加载配置文件
client = Fdfs_client(conf_path ='h://py_git/spider_fj2/SpiderWonder/SpiderWonder/client.conf')
#提交文件
ret = client.upload_by_filename(path)
print ret
print 'http://fsbd.fengjr.com/'+'/'+ret['Remote file_id'].replace("\\","/")

# persist_file(path,BytesIO(data))


# url = 'http://www.news.cn/fortune/titlepic/111989/1119892660_1478829228286_title0h.jpg'
# # url = 'http://static.criteo.net/design/dt/19037/161110/29bd3a0b746647049fd9e7148b0033ff_cpn_640x90_1.jpg'
# # url = 'http://news.xinhuanet.com/fortune/2016-11/04/1119846490_14782147913291n.jpg'
#
# # url = 'http://cms-bucket.nosdn.127.net/catchpic/e/ef/ef24e61afc9adfef574ac37f79574bfc.jpg?imageView&thumbnail=550x0'
#
# opener = urllib2.build_opener()
# header = {}
# request2 = urllib2.Request(url,headers=header,data=None)
# # print 'getUrl:',request.url
# response = opener.open(request2)
# response.headers['Transfer-Encoding'] = 'no chunked'
# body = response.read()
# print body
#
# from SpiderWonder.common.db.file_tool.file_tool import FieldObjectStoreTool
# # file_client = FieldObjectStoreTool('./')
# # file_client.default_encode = 'jpg'
# # print file_client.insert_data(body,url)
#
# persist_file('h://test/image/1119846490_14782147913291n.jpg',BytesIO(body))
# import StringIO, gzip
#
# def gzdecode(data) :
#     compressedstream = StringIO.StringIO(data)
#     gziper = gzip.GzipFile(fileobj=compressedstream)
#     data2 = gziper.read()   # 读取解压缩后数据
#     return data2
#
# print gzdecode(body)
# orig_image = Image.open(BytesIO(gzdecode(body)))
# width, height = orig_image.size
# orig_image.save('h://test/image/'+ 'a.jpg')

def persist_file(file_name, buf, meta=None, headers=None):
    absolute_path = file_name
    # self._mkdir(os.path.dirname(absolute_path), info)
    with open(absolute_path, 'wb') as f:
        f.write(buf.getvalue())


# import uuid
# for i in range(100):
#     print uuid.uuid1()