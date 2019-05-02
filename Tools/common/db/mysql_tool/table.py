# -*- coding: utf-8 -*-
# __author__ = 'lie.tian'
# create date = 2016/7/15

class column():
    def __init__(self,column_name,column_class,colmun_comment):
        self.column_name=column_name
        self.column_class=column_class
        self.column_comment=colmun_comment

    def __str__(self):
        return "`" +self.column_name+"` "+self.column_class+" COMMENT '"+self.column_comment +"'"


class table():
    def __init__(self,table_name,table_common):
        self.table_name=table_name
        self.table_common=table_common
        self.columns=[]
        self.columns_val=-1
        self.index=[]
        self.index_val=-1
        self.tail=' ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8'

    def add_column(self,column):
        '''添加列'''
        self.columns_val+=1
        self.columns.append(column)

    def add_index(self,index):
        self.index_val +=1
        self.index.append(index)

    def update_tail(self,var):
        self.tail=var

    def get_create_table_sql(self):
        sql ='CREATE TABLE ' + self.table_name +"("
        for i in range(0,self.columns.__len__(),1):
            if(i!=0):
                sql+=','
            sql += self.columns[i].__str__()
        for i in self.index:
            sql +=','
            sql +=i.__str__()
        sql +=")"+self.tail +" COMMENT '"+self.table_common+"';"
        return sql

if __name__=='__main__':
    table_name="test2"
    table =table(table_name,"test")
    table.add_column(column.column("id","int(11)","id"))
    table.add_column(column.column("age","int(11)","nianling"))
    # table.add_column(column.column("name","varchar(22)","xingming"))
    # table.add_index(index.index(table_name,True,"id"))
    # table.add_index(index.index(table_name,False,"age","name"))
    print(table.get_create_table_sql())
