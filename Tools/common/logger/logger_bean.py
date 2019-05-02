# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/10/31

import time
import json
import logging
logger_tool = logging.getLogger("django")

from ModelServer.control.http.response_v import ResponseDecode
import logging


class LoggerBean():

    def __init__(self,model_name=None):
        """
        日志结果
        :param model_name:
        :return:
        """
        #对应 0 1 ，0成功 1 失败
        self.succeed = 1
        #a,b,c测试值
        #默认0 为 自然通过 1为操作 model1 2为model2等等，默认1为线上model
        self.flow_type = '0'
        self.request_host = "127.0.0.1"
        self.request_data = None
        self.response_data = None
        self.msg = None
        self.model_name= model_name
        self.run_time = 0
        self.start_time = time.clock()



    def start(self,request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            self.request_host =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            self.request_host = request.META['REMOTE_ADDR']
        self.request_data = str(request.body, encoding = "utf-8")

    def end(self,succeed=1,response_data=None,msg=None,flow_type=None):
        self.succeed=succeed
        self.msg = msg
        self.response_data = str(response_data)
        if flow_type is not None:
            self.flow_type = str(flow_type)
        self.run_time = int((time.clock() - self.start_time)*1000)
        if self.succeed ==1:
            logger_tool.info("MODEL_REQUET:\u0001"+str(self.model_name)+'\u0001'+self.__str__())
        else:
            logger_tool.error("MODEL_REQUET:\u0001"+str(self.model_name)+'\u0001'+self.__str__())


    def __str__(self):
        return json.dumps(self.get_dict(),ensure_ascii=False,cls=ResponseDecode)

    def get_dict(self):
        return {"succeed":self.succeed,
                "request_host":self.request_host,
                "msg":self.msg,
                "request_data":self.request_data,"response_data":self.response_data,
                "flow_type":self.flow_type,
                "run_time":self.run_time}



