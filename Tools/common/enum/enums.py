# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/8/31

from enum import Enum


class DB_STORE_ENUM(Enum):
    # mysql
    MYSQL = 'MYSQL'
    MONGODB = 'MONGODB'
    LOCAL_FILE = 'LOCAL_FILE'
    KAFKA = 'KAFKA'
    HDFS_FILE = 'HEFS_FILE'
    FAST_DB = 'FAST_DB'
    HBASE = 'HBASE'
    # 存储地址为 文件 如 jpg,pdf 等
    FILE_OBJCT = 'FILE_OBJCT'
    ELASTICSEARCH = 'ELASTICSEARCH'

class QUEUE_TYPE(Enum):
    """
    队列属性
    """
    QUEUE = 'QUEUE' #先入先出
    PRIORITY_QUEUE = 'PRIORITY_QUEUE' #优先队列
    LIFO_QUEUE = 'LIFO_QUEUE' #先入后出

class SYSTEM_PLATFORM(Enum):
    WINDOWS = 'WINDOWS'
    LINUX = 'LINUX'
    MAC = 'MAC'



