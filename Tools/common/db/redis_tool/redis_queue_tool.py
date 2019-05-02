# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/7/15


import redis

#r=redis.StrictRedis(host='192.168.17.128',port=6379,db=0)

#r.set('test','test123')

#print r.get('test')

#r.delete("test")

#print r.config_get("maxmemory")

#r.config_set("timeout",1)

#r.config_get("timeout")



import traceback
import json
import sys



class RedisQueueTool():
    """redis 作为队列工具使用
    """
    def __init__(self,setting,redis_ip =None,redis_port = None,redis_db = None):
        self.setting = setting
        self.redis_ip = redis_ip
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.r = None
        self.connection()


    def connection(self):
        try:
            if self.r is not None:
                self.close()
            if(self.setting is not None):
                print('redis:',self.setting["QUEUE_REDIS_HOST"],self.setting["QUEUE_REDIS_PORT"],self.setting["QUEUE_REDIS_DBNAME"])
                # self.r=redis.StrictRedis(host=setting["QUEUE_REDIS_HOST"],port=setting["QUEUE_REDIS_PORT"],db=setting["QUEUE_REDIS_DBNAME"])setting["QUEUE_REDIS_DBNAME"]
                pool = redis.ConnectionPool(host=self.setting["QUEUE_REDIS_HOST"],port=self.setting["QUEUE_REDIS_PORT"],db=self.setting["QUEUE_REDIS_DBNAME"])#

                self.r = redis.Redis(connection_pool=pool)
                # print self.r.info()
                self.redis_ip = self.setting["QUEUE_REDIS_HOST"]
                self.redis_port = self.setting["QUEUE_REDIS_PORT"]
                self.redis_db = self.setting["QUEUE_REDIS_DBNAME"]
            else:
                print('redis:',str(self.redis_ip),str(self.redis_port),str(self.redis_db))
                pool = redis.ConnectionPool(host=self.redis_ip,port=self.redis_port,db=self.redis_db)
                self.r = redis.Redis(connection_pool=pool)
        except Exception as e:
            traceback.print_exc()

    def add_queue(self,queue_name,value):
        """
        加入队列
        """
        try:
            return self.r.rpush(queue_name,value)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def inserts(self,jss,name=None):
        """
        批量插入json数据集
        :param jss:
        :param name:
        :return:
        """
        for js in jss:
            v = self.add_queue(name,json.dumps(js,ensure_ascii=False))
            #异常处理先不处理了

    def get_more_js(self,name=None,size=None):
        """
        批量获取队列
        :param name:
        :return:
        """
        li = []
        for i in range(0,size):
            v = self.get_queue_and_pop(name)
            if v is None or v[0] != '{' is False:
                break
            else:
                li.append(json.loads(str(v,encoding='utf-8')))
        return li



    def add_queue_first(self,queue_name,value):
        """
        添加到队列头
        """
        try:
            return self.r.lpush(queue_name,value)
        except Exception as  e:
            traceback.print_exc()
            self.connection()
        return None

    def info(self):
        """
        获取信息
        :return:
        """
        try:
            var = self.r.info()
            var['host'] = self.redis_ip
            var['port'] = self.redis_port
            var['db'] = self.redis_db
            return var
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def get_queue_and_pop(self,queue_name):
        """
        获取并剔除
        """
        try:
            return self.r.lpop(queue_name)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None


    def get_queue_name_from_job_name(self,job_name):
        return 'spider_'+job_name

    def llen(self,queue_name):
        """
        查看队列长度
        :param queue_name:
        :return:
        """
        try:
            return self.r.llen(queue_name)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None


    def get_queue(self,queue_name,len=1):
        """
        获取多个数据
        """
        try:
            return self.r.lrange(queue_name,0,len-1)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def lrange(self,queue_name,start,end):
        try:
            return self.r.lrange(queue_name,start,end)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def get_queue_size(self,queue_name):
        """
        获取队列长度
        """
        try:
            return self.r.llen(queue_name)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def get_zscore(self,key,field):
        try:
            return self.r.zscore(key,field)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def zrange(self,zset_name,start=0,end=-1):
        try:
            return self.r.zrange(zset_name,start=start,end=end)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def zinc(self,zset_name,zfile,val):
        try:
            return self.r.zincrby(zset_name,zfile,val)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def zrange_withscore(self,zset_name,start=0,end=-1):
        try:
            return self.r.zrange(zset_name,start=start,end=end,withscores=True)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def zincrby(self,zset_name,zfiled_name,num):
        """
        用于状态的更新
        :param zset_name: zset value
        :param zfiled_name: zfile value
        :param num: 添加的值
        :return:
        """
        try:
            if(num!=0):
                self.r.zincrby(zset_name,zfiled_name,num)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def sismemeber(self,key,val):
        try:
            return self.r.sismember(key,val)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def sadd(self,key,val):
        try:
            return self.r.sadd(key,val)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def hget(self,key,field):
        try:
            return self.r.hget(key,field)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def hset(self,key,field,value):
        try:
            return self.r.hset(key,field,value)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def hgetall(self,key):
        try:
            return self.r.hgetall(key)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None

    def hdel(self,key,field):
        try:
            return self.r.hdel(key,field)
        except Exception as e:
            traceback.print_exc()
            self.connection()
        return None



    def close(self):
        pass

if __name__=="__main__":
    pass
    sett ={}
    sett['QUEUE_REDIS_HOST']='10.10.202.24'
    sett['QUEUE_REDIS_PORT']= 6379
    sett['QUEUE_REDIS_DBNAME']= 7
    redis=RedisQueueTool(setting=sett)
    # print redis.sismemeber('aaa','a')
    # redis.sadd('aaa','a')
    print(redis.sismemeber('spider_member_news_search_baiducyc_news_search_baiducyc_key','http://business.sohu.com/20170120/n479250722.shtml'))