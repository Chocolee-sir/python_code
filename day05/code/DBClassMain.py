#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import MySQLdb

#数据库接口类
class DbInterface(object):

    def __init__(self,host,user,password,dbname,charset="utf8"):
        self.host=host
        self.user=user
        self.password=password
        self.dbname = dbname
        self.charset=charset

        try:
            self.conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.password)
            self.conn.select_db(dbname)
            self.conn.set_character_set(self.charset)
            self.cur=self.conn.cursor()
        except MySQLdb.Error,e:
            print "MySQLdb Error",e

    def query(self,sql):
        try:
           n=self.cur.execute(sql)
           return n
        except MySQLdb.Error,e:
           print "Mysql Error:%s\nSQL:%s" %(e,sql)

    def queryRow(self,sql):
        self.query(sql)
        result = self.cur.fetchone()
        return result

    def queryAll(self,sql):
        self.query(sql)
        result=self.cur.fetchall()
        desc =self.cur.description
        d = []
        for inv in result:
             _d = {}
             for i in range(0,len(inv)):
                 _d[desc[i][0]] = str(inv[i])
             d.append(_d)
        return d

    def insert(self,p_table_name,p_data):
        for key in p_data:
            p_data[key] = "'"+str(p_data[key])+"'"
        key = ','.join(p_data.keys())
        value = ','.join(p_data.values())
        real_sql = "INSERT INTO " + p_table_name + "(" + key + ") VALUES (" + value + ")"
        return self.query(real_sql)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

