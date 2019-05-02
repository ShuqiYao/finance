# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/11/17

from datetime import datetime
from elasticsearch import helpers
from elasticsearch import Elasticsearch

#http://elasticsearch-py.readthedocs.io/en/master/

#es 工具
class EsClient:


    def __init__(self,ip = '10.10.202.119',port=9200,index="spider_status_index",doc_type="spider",bulk_count =1000,user=None,pwd=None):
        """
        :param ip:
        :param port:
        :param index:
        :param doc_type:
        :param bulk_count:
        :return:
        """
        self.ip =  ip
        self.port = port
        self.index = index
        self.doc_type = doc_type
        self.bulk_count = bulk_count
        hosts = []
        for ip2 in ip.split(","):
            hosts.append({"host":ip2,"port":self.port})
        if user is None:

            self.client = Elasticsearch(hosts=hosts,
                                        sniff_on_start=True,
                                        sniff_on_connection_fail=True,
                                        sniffer_timeout=60,
                                        maxsize=5)
            # self.client= Elasticsearch(hosts=self.ip)
        else:
            self.client = Elasticsearch(hosts=hosts,
                                        sniff_on_start=True,
                                        sniff_on_connection_fail=True,
                                        sniffer_timeout=60,
                                        maxsize=5,
                                        use_ssl=True,
                                        http_auth=(user,pwd))

            pass


    def search_test(self):
        query_json = {
            "bool": {
                "must": {
                    "term": {
                        "user_id": 'E691821B-0C6A-4950-9CA1-55538AE60894'
                    }
                }
                }
        }
        source_arr = ['user_id','user_id_md5']
        res = self.client.search(index="v2",doc_type="bigdata",body={"query": query_json, "_source": source_arr})  # 获取所有数据

        # 获取第一条数据，得分最高。
        top_10_recodes = res['hits']['hits']
        # print json.dumps(top_10_recodes)
        return [top_10_recodes]

    def search_test2(self):
        query_json = {
            "bool":{
                "must":[{
                    "match_all":{}
                }]
            }
        }
        res = self.client.search(index="kg_model_logger",doc_type="model",body={"query": query_json})  # 获取所有数据

        # 获取第一条数据，得分最高。
        top_10_recodes = res['hits']['hits']
        print(top_10_recodes)


    def search_test3(self):

        res = self.client.get(index=self.index,doc_type=self.doc_type,id="110498678782185008")  # 获取所有数据

        # 获取第一条数据，得分最高。
        print(res)

    def search(self,index=None,type=None,query=None,field=None):
        """
        查询语句
        :param index: 索引
        :param type: 类型
        :param query: 查询语句
        :param field: 类型
        :return:
        """
        source_arr = field
        if index is None and type is None:
            if isinstance(query,dict) or query.startswith('{'):
                res = self.client.search(index=self.index,doc_type=self.doc_type,body=query)
            else:
                res = [self.client.get(index=self.index,doc_type=self.doc_type,id=query)]
        else:
            if  isinstance(query,dict) or query.startswith('{'):
                res = self.client.search(index=index,doc_type=type,body={"query": query, "_source": source_arr})  # 获取所有数据
            else:
                res = [self.client.get(index=index,doc_type=type,id=query)]
        return res




    def inserts(self,lists):
        """

        :param lists:
        :return:
        """
        count = 0
        actions = []
        for li in lists:
            count +=1
            actions.append({
                "_index":self.index,
                "_type" :self.doc_type,
                "_source":li
            })
            if count%self.bulk_count == 0:
                helpers.bulk(self.client,actions)
                actions = []
        if len(actions) >0:
            helpers.bulk(self.client,actions)


if __name__ == '__main__':
    js = {'status': 'DEBUG', 'info': 'H:\\Python27\\lib\\site-packages\\scrapy\\core\\scraper.pyscraper.py:_itemproc_finished: Scraped from ', 'code': '200', 'http': 'http://finance.ifeng.com/a/20161115/15007893_0.shtml', 'happend_time': '2016-11-17 16:34:31', 'ip': '10.254.56.2', 'http_type': 'http://finance.ifeng.com', 'job_name': 'ifeng_desc_news'}
    es = EsClient(ip="10.100.31.48,10.100.31.46,10.100.31.51",port=9200,index="kg_common_feature",doc_type="feature")
    #es.inserts([js])
    # print(es.search_test())
    print(es.search_test3())
