# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/11/1

from Tools.common.setting import  Setting


settings = Setting()
print(settings['LOGGER_IP'])

import time

v = time.clock()

time.sleep(2)
print(time.clock() - v)