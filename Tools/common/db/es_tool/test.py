# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/2/14




# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/11/17

from datetime import datetime
from elasticsearch import helpers
from elasticsearch import Elasticsearch
es = Elasticsearch('10.10.202.119')

es.create(index="spider_status_index", doc_type="spider", id=1,
  body={"any":"data", "timestamp": datetime.now()})
#{u'acknowledged':True}
j = 0
count = 100
actions = []
while (j < count):
   action = {
        "_index": "tickets-index",
        "_type": "tickets",
        "_id": j + 1,
        "_source": {
              "crawaldate":j,
              "flight":j,
              "timestamp": datetime.now()}
        }
   actions.append(action)
   j += 1

if (len(actions) == 500000):
    helpers.bulk(es, actions)
    del actions[0:len(actions)]

if (len(actions) > 0):
  helpers.bulk(es, actions)
  del actions[0:len(actions)]

#插入数据,(这里省略插入其他两条数据，后面用)
es.index(index="my-index",doc_type="test-type",id=1,body={"any":"data01","timestamp":datetime.now()})
#{u'_type':u'test-type',u'created':True,u'_shards':{u'successful':1,u'failed':0,u'total':2},u'_version':1,u'_index':u'my-index',u'_id':u'1}
#也可以，在插入数据的时候再创建索引test-index
es.index(index="test-index",doc_type="test-type",id=42,body={"any":"data","timestamp":datetime.now()})


#查询数据，两种get and search
#get获取
res = es.get(index="my-index", doc_type="test-type", id=1)
print(res)
#{u'_type': u'test-type', u'_source': {u'timestamp': u'2016-01-20T10:53:36.997000', u'any': u'data01'}, u'_index': u'my-index', u'_version': 1, u'found': True, u'_id': u'1'}
print(res['_source'])
#{u'timestamp': u'2016-01-20T10:53:36.997000', u'any': u'data01'}

#search获取
res = es.search(index="test-index", body={"query":{"match_all":{}}})  #获取所有数据
print(res)
#{u'hits':
#    {
#    u'hits': [
#        {u'_score': 1.0, u'_type': u'test-type', u'_id': u'2', u'_source': {u'timestamp': u'2016-01-20T10:53:58.562000', u'any': u'data02'}, u'_index': u'my-index'},
#        {u'_score': 1.0, u'_type': u'test-type', u'_id': u'1', u'_source': {u'timestamp': u'2016-01-20T10:53:36.997000', u'any': u'data01'}, u'_index': u'my-index'},
#        {u'_score': 1.0, u'_type': u'test-type', u'_id': u'3', u'_source': {u'timestamp': u'2016-01-20T11:09:19.403000', u'any': u'data033'}, u'_index': u'my-index'}
#    ],
#    u'total': 5,
#    u'max_score': 1.0
#    },
#u'_shards': {u'successful': 5, u'failed': 0, u'total':5},
#u'took': 1,
#u'timed_out': False
#}
for hit in res['hits']['hits']:
    print(hit["_source"])
res = es.search(index="test-index", body={'query':{'match':{'any':'data'}}}) #获取any=data的所有值
print(res)

