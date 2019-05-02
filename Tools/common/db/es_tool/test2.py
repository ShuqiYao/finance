# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2018/1/2

from Tools.common.db.es_tool.es_store_tool import EsClient


js = {'status': 'DEBUG', 'info': 'H:\\Python27\\lib\\site-packages\\scrapy\\core\\scraper.pyscraper.py:_itemproc_finished: Scraped from ', 'code': '200', 'http': 'http://finance.ifeng.com/a/20161115/15007893_0.shtml', 'happend_time': '2016-11-17 16:34:31', 'ip': '10.254.56.2', 'http_type': 'http://finance.ifeng.com', 'job_name': 'ifeng_desc_news'}
es = EsClient(ip="10.100.31.48,10.100.31.46,10.100.31.51",port=9200,index="kg_model_logger",doc_type="model")
#es.inserts([js])
# print(es.search_test())

query = {

    "query": {
        "bool": {
            "must": [
                {
                    "term": {
                        "model_name": "团伙欺诈识别"
                    }
                }
                ,
                {
                    "term": {
                        "happend_date": "2018-01-02"
                    }
                }
            ],
            "must_not": [ ],
            "should": [ ]
        }
    },
    "from": 0,
    "size": 10000,
    "sort": [ ],
    "aggs": { }

}
field=["response_data","request_host","res"]
#print(es.search_test3())
data =es.search(query=query)
import json
file = open("./data.txt","w")
for v in data['hits']['hits']:
    d = json.loads(v['_source']['response_data'])
    res = d['res']
    if len(res) >0 and d['score']>0.6:
        print(v)
        print(d['score'])
        file.write(str(d['score']))
        file.write('\n')
# print(data)