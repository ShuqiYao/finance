# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/9/27




# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/10/24




#running系统
import os
import imp

class ProcessInput():


    def __init__(self,file_path):
        #执行的实际文件
        self.module_name = None
        #模块
        self.module = None

        self.file_path = file_path
        self.module_name,ext = os.path.splitext(os.path.basename(file_path))
        self.module = imp.load_source("m",self.file_path)

    def get_init_func(self):
        """
        调用文件初始化函数
        :return:
        """
        # self.module = __import__(self.module_name)
        # fp, pathname, description = imp.find_module(self.file_path)

        init_ = getattr(self.module,'init')
        return init_

    def get_attr(self,attribute):
        """
        获取属性
        :param attribute:
        :return:
        """
        return getattr(self.module,attribute)

    def has_attr(self,attribute):
        """
        判断是否存在
        :param attribute:
        :return:
        """
        return hasattr(self.module,attribute)

    def set_attr(self, key, value):
        """
        设置属性
        :param key:
        :param value:
        :return:
        """
        setattr(self.module,key,value)

    def __getitem__(self, item):
        return self.get_attr(item)

# test = ProcessInput("test.py")
# init = test.get_init_func()
# init()
#
#
# handle = test.get_handle_one_day()
# handle()