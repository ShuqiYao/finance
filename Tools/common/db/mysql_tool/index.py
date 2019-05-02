# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/7/15


class index():

    def __init__(self,table_name,is_pari,*columns):
        self.is_pari=is_pari;
        self.table_name=table_name
        if(columns.__len__()>0):
            self.isUnion=True
        else:
            self.isUnion=False
        self.columns=columns


    def __str__(self):
        if(self.is_pari):
            var = "PRIMARY KEY (`"+self.columns[0]+"`)"
            return var
        else:
            if(self.isUnion):
                var = "UNION KEY `idx_"+self.table_name+"_"
                for column in self.columns:
                    var += "_" + column[0:4]
                var +="("
                for i in range(0,self.columns.__len__(),1):
                    if(i!=0):
                        var +=','
                    var +="`" + self.columns[i] + "`"
                var +=") USING BTREE"
                return var
            else:
                var = "KEY `idx_" +self.table_name+"_" +self.columns[0][0:4]+" (`"+self.columns[0]+"`) USING BTREE"
                return var
