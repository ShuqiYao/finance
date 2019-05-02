# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2017/11/27



from pyspark import SparkContext
from pyspark.sql import HiveContext,Row,SQLContext
logFile = "/user/spark/text.dat"

sc = SparkContext("local", "Simple App")
# logData = sc.textFile(logFile).cache()
# numAs = logData.filter(lambda s: 'a' in s).count()
# numBs = logData.filter(lambda s: 'b' in s).count()
# print("Lines with a: %i, lines with b: %i" % (numAs, numBs))
hiveCtx = HiveContext(sc)
vals = hiveCtx.sql("show databases")
print(vals)

