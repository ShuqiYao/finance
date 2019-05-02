# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/9/27

import settings
from Tools.common.reflect import ProcessInput

class Setting:

    def __init__(self):
        self.sett = ProcessInput(settings.project_dir+'/settings.py')
        pass

    def __getitem__(self, item):
        return self.sett[item]

    def __setitem__(self, key, value):
        self.sett.set_attr(key,value)

    def get(self,item):
        return self.sett[item]

    def set(self,key,value):
        self.__setitem__(key,value)


