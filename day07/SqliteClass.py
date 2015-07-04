#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import sqlite3

class SqliteClass(object):

    def __init__(self,dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def query(self,sql):
        try:
            n=self.cur.execute(sql)
            return n
        except sqlite3.Error,e:
            print "sqlite Error:%s\nSQL:%s" %(e,sql)

    def queryRow(self,sql):
        self.query(sql)
        result = self.cur.fetchone()
        return result

    def queryAll(self,sql):
        self.query(sql)
        result=self.cur.fetchall()
        desc =self.cur.description
        n = 1
        _d = {}
        for inv in result:
             for i in range(0,len(inv)):
                 _d[n] = inv[i].split(';')
                 n += 1
        return _d

    def queryLog(self,sql):
        self.query(sql)
        result = self.cur.fetchall()
        print('ip地址 | 操作时间 | 登录堡垒机用户 | 登录远程机用户 | 操作命令')
        for i in result:
            print '%s | %s | %s | %s | %s' %(i[0],i[1],i[2],i[3],i[4])

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
