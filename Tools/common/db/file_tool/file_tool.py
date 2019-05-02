# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/7/18
import uuid

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os
import sys
import json
import datetime
import re
import logging
import urllib
from Tools.common.db.db_conn import DbConn
from Tools.common.logger.logger import info,error,warn
import sys
import traceback
import  gzip
from io import StringIO


class FileStoreTool(DbConn):

    """
    文件 存储工具
    支持 按照天滚动
    """
    def __init__(self,is_write=None,dir=None,name=None):
        """

        :param files_or_dir:
        :param is_write:
        :param dir:
        :param name:
        :return:
        """
        #目录
        self.is_write = is_write
        self.client = None
        self.dir = dir
        self.file_bak = name
        pass

    def get_connection(self):
        # self.before_day=datetime.date.today()
        if self.is_write:
            if(self.file_param is None):
                m=re.search('\{([^\}]*?)\}',self.file_bak)
                self.file_param=str(m.group(1))
                if(self.file_param is None):
                    self.file=self.file_bak
                else:
                    self.before_day=str(datetime.datetime.now().strftime(self.file_param))
                    # print '######################'
                    # print self.file_bak,type(self.file_bak)
                    # print self.file_param,type(self.file_param)
                    # print self.before_day,type(self.before_day)
                    # print '######################'
                    self.file= self.dir+"/"+self.file_bak.replace("{"+self.file_param+"}",self.before_day)
            else:
                self.before_day=str(datetime.datetime.now().strftime(self.file_param))
                self.file= self.dir+"/"+self.file_bak.replace("{"+self.file_param+"}",self.before_day)
            #print 'create file:' + self.file,logging.INFO
            self.client=open(self.file,'a')
        #建立数据库连接

    def close(self):
        if self.client is not None:
            self.client.close()
        pass

    def create_table(self,table):
        pass

    def select_data(self,find=None,filter=None,table=None):
        """
        加载数据
        :return:
        """
        #加载本地文件
        data = []
        if isinstance(find,list):
            for one in find:
                if os.path.isdir(one):
                    files = os.listdir(one)
                    for one2 in files:
                        self.load_one_file(one2,data)
                else:
                    self.load_one_file(one,data)
        else:
            self.load_one_file(find,data)
        return data

    def load_one_file(self,file,data):
        """
        读取一个文件
        :param file:
        :return:
        """
        info('load file',file)
        filev = open(file,'r')
        for v in filev:
            if len(v)>0:
                data.append(re.split('[\t, \n]*',v.replace("\n",'')))
        filev.close()



    def drop_table(self,table_name):
        pass

    def update_data(self,json_data,parkey=None,up_vals=None,table_name=None):
        pass

    def insert_data(self,dict,table_name=None,flag=False):
        """
        传入参数为字符串
        :param data:
        :return:
        """
        if(self.file_param is not None):
            var =datetime.datetime.now().strftime(self.file_param)
            if(self.before_day != var):
                self.close()
                #重建连接
                self.get_connection()
                self.client.write(json.dumps(dict,ensure_ascii=False))
            else:
                self.client.write(json.dumps(dict,ensure_ascii=False))
            self.client.write('\n')
            self.client.flush()
        else:
            self.client.write('\n')
            self.client.flush()
        # print '插入完成'


class FieldObjectStoreTool(DbConn):
    """
    文件实体存储工具
    """
    def __init__(self,dir):
        self.default_encode = None
        self.dir = dir
        pass

    def get_connection(self):
        pass
        #建立数据库连接

    def close(self):
        pass

    def create_table(self,table):
        pass

    def select_data(self,find=None,filter=None,table=None):
        pass

    def drop_table(self,table_name):
        pass

    def update_data(self,json_data,parkey=None,up_vals=None,table_name=None):
        pass

    def insert_data(self,data,table_name=None,flag=True,type_val=None):
        """

        :param data: 实际的 url response_body
        :param table_name: 对应的文件地址,或者实际存储的图片地址
        :return:
        """
        #解析文件格式
        m = re.search('\.([^\.]*?)$',table_name)
        if m:
            type = m.group(1)
        else:
            type = None
        table_name_bak = os.path.basename(table_name)
        # table_name_bak = 'tmp'+str(table_name_bak.__hash__()) + str()
        table_name_bak = str(uuid.uuid1())

        # print table_name,table_name_bak
        if type is not None and (type.find('?')>=0 or type.find('&')>=0):
            type = None

        if(type_val is None):
            return self.save_obj(data,table_name_bak,type = type)
        else:
            if(type is None):
                pass
            else:
                table_name_bak +='.' + type
            if type_val.find('image') >=0:
                if type is None:
                    if self.default_encode is None:
                        table_name_bak += '.jpg'
                        type = 'jpg'
                    else:
                        table_name_bak += '.'+ self.default_encode
                    # print table_name_bak
                    return self.save_obj(data,table_name_bak,type = self.default_encode)
                else:
                    return self.save_obj(data,table_name_bak,type = type)
            elif type_val.find('pdf') >=0:
                return self.save_obj(data,table_name_bak,type = type)

        #print '存储完成'

    def save_obj(self,data,table_name,type =None):
        if type is None:
            self.persist_file(table_name,BytesIO(data))
        if(type == 'pdf'):
            # urllib.urlretrieve(everyURL, table_name)
            self.persist_file(table_name,BytesIO(data))
            pass
        elif(self.is_image(type)):
            # url = 'http://pdf.dfcfw.com/pdf/H3_AP201607050016383683_1.pdf'
            # path = 'test.pdf'
            # f = open(path, 'wb')
            # urllib.urlretrieve(url, path)
            try:
                orig_image = Image.open(BytesIO(data))
            except Exception  as e:
                traceback.print_exc()
                if 'cannot identify image file' in str(e):
                    try:
                        orig_image = Image.open(BytesIO(self.gzdecode(data)))
                    except Exception as e2:
                        traceback.print_exc()
                        raise  Exception(traceback.format_exc())

            width, height = orig_image.size

            ######## 判断图片大小 #####################
            # 如果图片小于图片的长小于50，那么就不入库
            longside_length = 50
            if max(orig_image.size) <= longside_length:
                return None
                # 从obj中去掉这个URL
            if width == height:
                return None

            if(self.default_encode is None):
                try:
                    orig_image.save(os.path.join(self.dir,os.path.basename(table_name)))
                except Exception as e:
                    traceback.print_exc()
                    self.persist_file(os.path.join(self.dir,os.path.basename(table_name)),BytesIO(data))
            else:
                if(type is None):
                    orig_image.save(os.path.join(self.dir,os.path.basename(table_name+'.'+self.default_encode)),self.default_encode)
                    return os.path.basename(table_name+'.'+self.default_encode)
                else:
                    try:
                        orig_image.save(os.path.join(self.dir,os.path.basename(table_name)),self.default_encode)
                    except Exception as e:
                        traceback.print_exc()
                        self.persist_file(os.path.join(self.dir,os.path.basename(table_name)),BytesIO(data))
            pass
        elif(self.is_vedio(type)):
            #print '不支持vedio 类型'
            pass
        else:
            self.persist_file(table_name,BytesIO(data))
            pass
        return table_name

    def gzdecode(self,data) :
        compressedstream = StringIO.StringIO(data)
        gziper = gzip.GzipFile(fileobj=compressedstream)
        data2 = gziper.read()   # 读取解压缩后数据
        return data2


    def translate(self,source_data,target_data):
        """
        图片格式转换方法 如果需要将jpg等转化为 bmp这类需要重写该方法
        :param source_data:
        :param target_data:
        :return:
        """
        return source_data

    def persist_file(self, file_name, buf, meta=None, headers=None):
        absolute_path = self._get_filesystem_path(file_name)
        # self._mkdir(os.path.dirname(absolute_path), info)
        with open(absolute_path, 'wb') as f:
            f.write(buf.getvalue())

    def _get_filesystem_path(self, file_name):
        # path_comps = path.split('/')
        return os.path.join(self.dir,os.path.basename(file_name))

    def is_image(self,type):
        if(type == 'jpg' or type == 'bmp' or type == 'jpge' or type == 'png' or type == 'gif'):
            return True
        elif(self.default_encode == 'jpg' or self.default_encode == 'bmp' or self.default_encode == 'jpge' or self.default_encode == 'png' or self.default_encode == 'gif'):
            return True
        else:
            return False

    def is_vedio(self,type):
        if(type == 'rm' or type == 'avi' or type == 'rbm' or type == 'mp4'):
            return True
        else:
            return False

# if __name__=="__main__":
    # mongo=FileStoreTool("test.json")
    # mongo.insert_data(json.load({"name":"tianlie","address":"china","val":22.3}))
    # print mongo.select_data({});
    # file_param = 'yyyy-mm-dd'
    # file_param = '%Y-%m-%d'
    # print datetime.datetime.now().strftime(file_param)
    # list = [u'\u722c\u866b\u7cfb\u7edf\u76d1\u63a7\u65e5\u62a5', u'\u6d4b\u8bd5\u6570\u636e\u96c6']
    # for v in list:
    #     print v.encode('utf-8')

# if __name__ == "__main__":
#     dic ={}
#     dic['name']='中国'
#     data = json.dumps(dic,ensure_ascii=False)
#     print BytesIO(data.encode('utf-8')).read()