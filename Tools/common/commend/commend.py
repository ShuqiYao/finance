# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/10/31



import platform
from Tools.common.enum.enums import SYSTEM_PLATFORM
import os
import threading
import re
import time
import socket


import sys
import re

import subprocess


class Commend():

    def __init__(self):
        self.plat = SYSTEM_PLATFORM.WINDOWS
        if('Windows' in platform.system()):
            self.plat = SYSTEM_PLATFORM.WINDOWS
        elif('Linux' in platform.system()):
            self.plat = SYSTEM_PLATFORM.LINUX
        elif('Darwin' in platform.system()):
            self.plat = SYSTEM_PLATFORM.MAC

    def check_port_is_used(self,port):
        """
        检查端口是否占用
        :param port:
        :return:
        """
        if(self.plat == SYSTEM_PLATFORM.WINDOWS):
            # var = os.popen('netstat  -aon|findstr "'+ str(port)+'"').read()
            # print 'value',var ,len(var)
            if len(os.popen('netstat  -aon|findstr "'+ str(port)+'"').read()) ==0:
                return False
        elif(self.plat == SYSTEM_PLATFORM.LINUX):
            if len(os.popen('netstat -tln | grep '+ str(port)).read()) ==0:
                return False
        elif(self.plat == SYSTEM_PLATFORM.MAC):
            if len(os.popen(' lsof -i tcp:'+ str(port)).read()) ==0:
                return False
        return True

    def copy_dir_to(self,host,dir,to_dir):
        print('from',dir,' to ',host,to_dir)
        val2 = os.popen('scp -r ' +dir +' root@' + host + ':'+to_dir)
        val = val2.read()
        val2.close()
        print(val)

    def run_commend(self,com):
        print(com)
        val = os.popen(com)
        val.read()
        val.close()

    def run_commend_by_host(self,host,com):
        print('ssh root@'+host+' "'+com+'"')
        val = os.popen('ssh -v root@'+host+' "'+com+'"')
        val.read()
        val.close()

    def run_commend_and_val(self,com):
        print(com)
        val = os.popen(com)
        return val.read()

    def run_commend_by_host_and_val(self,host,com):
        print('ssh -v root@'+host+' << EOF \n'+com+ '\nEOF')
        val = os.popen('ssh -v root@'+host+' << EOF \n'+com+ '\nEOF')
        return val.read()

    def run_commend_by_host_eof(self,host,com):
        print('ssh root@'+host +' << EOF \n'+com+'\nEOF')
        val = os.popen('ssh -T root@'+host +' << EOF \n'+com+'\nEOF')
        val.close()

    def run_commend_get_pid(self,com):
        vals = self.run_commend_and_val(com)
        list_pid = []
        if vals is None:
            return list_pid
        datas = vals.split('\n')
        # print datas
        for d in datas:
            v = re.split('\s*',d)
            if len(v)>7 and v[0] =='root':
                list_pid.append(v[1])
        return list_pid
        return datas

    def run_commend_by_host_eof_get_pid(self,host,com):
        vals = self.run_commend_by_host_and_val(host,com)
        list_pid = []
        if vals is None:
            return list_pid
        datas = vals.split('\n')
        for d in datas:
            v = re.split('\s*',d)
            if len(v)>7 and v[0] == 'root':
                list_pid.append(v[1])
        return list_pid

    def start_scrapy_crawl(self,name,params):

        """
        启动爬虫
        :param name:
        :return:
        """
        #将新建爬虫添加入队列中
        return True


    def start_scrapy_cralw_asny(self,name,params):
        """
        异步启动程序
        :return:
        """
        print('start job',name,params)
        timel = 0.5
        if(self.plat == SYSTEM_PLATFORM.WINDOWS):
            var = None
            if(params is not None):
                var = "start /b python scrapy_commend.py scrapy crawl " + name + ' "'+params.replace('"','\\"')+'"'
            else:
                var = "start /b python scrapy_commend.py scrapy crawl " + name
            print('commend',var)
            p = os.popen(var)
            #threading._sleep(timel)
            time.sleep(timel)
            p.close()
            return True
        elif(self.plat == SYSTEM_PLATFORM.LINUX):
            var = None
            dir = os.getcwd()
            if(params is not None):
                var ="nohup python -u scrapy_commend.py scrapy crawl " + name +' \''+params +'\'' +" >>" +dir+'/logs/'+ name +".log 2>&1 &"
            else:
                var = "nohup python -u scrapy_commend.py scrapy crawl " + name +" >>" +dir+'/logs/'+ name +".log 2>&1 &"
            p = os.popen(var)
            #threading._sleep(timel)
            time.sleep(timel)
            p.close()
            return True
        elif(self.plat == SYSTEM_PLATFORM.MAC):
            var = None
            if(params is not None):
                var = "python scrapy_commend.py scrapy crawl " + name +' "'+params.replace('"','\\"')+'"'+" &"
            else:
                var = "python scrapy_commend.py scrapy crawl " + name +" &"
            p = os.popen(var)
            #threading._sleep(timel)
            time.sleep(timel)
            p.close()
            return True
        return False

    def kill_pid(self,list_pid):
        if(self.plat == SYSTEM_PLATFORM.WINDOWS):
            for po in list_pid:
                p = os.popen('taskkill /PID "' +str(po)+'" /F')
                print(u'杀死子进程pid',po,p.readlines())
                p.close()
        elif(self.plat == SYSTEM_PLATFORM.LINUX):
            for po in list_pid:
                p = os.popen('kill -9 ' +str(po)+'')
                print(u'杀死子进程pid',po,p.readlines())
                p.close()

    def kill_pid_by_host(self,host,pid):
        if(self.plat == SYSTEM_PLATFORM.WINDOWS):
            if(host == '127.0.0.1'):
                p = os.popen('taskkill /PID "' +str(pid)+'" /F')
                # print u'杀死子进程pid',pid,p.readlines()
                p.close()
            else:
                pass
        elif(self.plat == SYSTEM_PLATFORM.LINUX):
            if(host == '127.0.0.1'):
                p = os.popen('kill -9 ' +str(pid)+'')
                # print u'杀死子进程pid',po,p.readlines()
                p.close()
            else:
                p = os.popen('ssh -v root@'+host+' "kill -9 '+str(pid)+'')
                # print u'杀死子进程pid',po,p.readlines()
                p.close()


    def kill_listening_all_by_port(self,port,list_port):
        """
        杀死某个端口对应的全部进程 包括 子进程
        :param port:
        :return:
        """
        if(self.plat == SYSTEM_PLATFORM.WINDOWS):
            for po in list_port:
                var = 'netstat -ano |findstr "' +str(po)+ '"'
                p = os .popen(var)
                list = p.readlines()
                lis_pid = 0
                for k in list:
                    ll = re.split("[\s]*",k.strip(' '))
                    # print 'll',ll
                    if(ll[3] == 'LISTENING'):
                        lis_pid =int(ll[4])
                        break
                if(lis_pid >0):
                    p = os.popen('taskkill /PID "' +str(lis_pid)+'" /F')
                    print(u'杀死子进程端口',po,p.readlines())
            # if(len(list_port)>0):
            #     time.sleep(2)

            var = 'netstat -ano |findstr "' +str(port)+ '"'
            p = os.popen(var)
            list = p.readlines()
            lis_pid = 0
            # print 'list',list
            for k in list:
                ll = re.split("[\s]*",k.strip(' '))
                # print 'll',ll
                if(ll[3] == 'LISTENING'):
                    lis_pid =int(ll[4])
                    break
                # else:
                #     pid =int(ll[4])
                #     if(lis_pid == pid):
                #         continue
                #     #p = os.popen('ntsd -c q -p "' +str(pid)+'"')
                #     p = os.popen('taskkill /PID "' +str(pid)+'"')
                #     print 'pid',pid,p.readlines()
            # print 'pid',lis_pid
            # taskill /PID lis_pid
            if(lis_pid > 0):
                #p = os.popen('ntsd -c q -p "' +str(lis_pid)+'"')
                p = os.popen('taskkill /PID "' +str(lis_pid)+'" /F')
                print(u'杀死监听进程',lis_pid,p.readlines())
            return True
        elif(self.plat == SYSTEM_PLATFORM.LINUX):
            pass
        elif(self.plat == SYSTEM_PLATFORM.MAC):
            pass
        return False

    def get_ip_address(self,network_name=None):
        if network_name is not None:
            if(self.plat == SYSTEM_PLATFORM.WINDOWS):
                return '127.0.0.1'
            elif(self.plat == SYSTEM_PLATFORM.LINUX):
                import fcntl
                import struct
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                return socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', network_name.encode('utf-8'))
                )[20:24])
            return '127.0.0.1'
        else:
            ips = self.find_all_ip()
            if ips is not None and len(ips) >0:
                return ips[0]
            else:
                return '127.0.0.1'


    def find_all_ip(self):
        ipstr = '([0-9]{1,3}\.){3}[0-9]{1,3}'
        if self.plat == SYSTEM_PLATFORM.MAC or self.plat == SYSTEM_PLATFORM.LINUX:
            ipconfig_process = subprocess.Popen("ifconfig", stdout=subprocess.PIPE)
            output = ipconfig_process.stdout.read()
            ip_pattern = re.compile('(inet %s)' % ipstr)
            if self.plat == SYSTEM_PLATFORM.LINUX:
                ip_pattern = re.compile('(inet addr:%s)' % ipstr)
            pattern = re.compile(ipstr)
            iplist = []
            for ipaddr in re.finditer(ip_pattern, str(output)):
                ip = pattern.search(ipaddr.group())
                if ip.group() != "127.0.0.1":
                    iplist.append(ip.group())
            return iplist
        elif self.plat == SYSTEM_PLATFORM.WINDOWS:
            ipconfig_process = subprocess.Popen("ipconfig", stdout=subprocess.PIPE)
            output = ipconfig_process.stdout.read()
            ip_pattern = re.compile("IPv4 Address(\. )*: %s" % ipstr)
            pattern = re.compile(ipstr)
            iplist = []
            for ipaddr in re.finditer(ip_pattern, str(output)):
                ip = pattern.search(ipaddr.group())
                if ip.group() != "127.0.0.1":
                    iplist.append(ip.group())
            return iplist