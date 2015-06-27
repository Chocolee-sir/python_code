#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import hashlib
from DBClass import *

class UserInfo(object):
    s = DbInterface('10.10.206.193','chocolee','123456','chocolee')
    b = '%'

    def __init__(self,username):
        self.username = username

    def change_md5(self, password):
        m = hashlib.md5()
        m.update(password)
        return m.hexdigest()

    def find_user(self):
        sql = "SELECT 1 FROM user WHERE username = '%s' limit 1;" %self.username
        return self.s.queryRow(sql)


    def find_pass(self):
        sql = "SELECT passwd FROM user WHERE username = '%s';" %self.username
        return self.s.queryRow(sql)[0]

    def user_lockstatus(self):
        sql = "SELECT flag FROM user WHERE username = '%s';" %self.username
        return self.s.queryRow(sql)[0]

    def lock_userlist(self):
        sql = "SELECT username FROM user WHERE flag = '1';"
        return self.s.queryAll(sql)

    def unlock_user(self,user):
        sql = "UPDATE user SET flag = 0 WHERE username = '%s';" %user
        self.s.query(sql)
        self.s.commit()

    def lock_user(self):
        sql = "UPDATE user SET flag = 1 WHERE username = '%s';" %self.username
        self.s.query(sql)
        self.s.commit()

    def groupname(self):
        sql = "SELECT groupname FROM user WHERE username = '%s';" %self.username
        return self.s.queryRow(sql)[0]

    def ip_list(self):
        sql = "SELECT b.hostinfo FROM user a,host b \
        WHERE a.groupname = '%s' AND a.groupname = b.groupname;" %self.groupname()
        info_dic = self.s.queryAll(sql)
        for k,v in info_dic.items():
            print '%s:%s' %(k,v[0])

    def ip_info(self):
        sql = "SELECT b.hostinfo FROM user a,host b \
        WHERE a.groupname = '%s' AND a.groupname = b.groupname;" %self.groupname()
        info_dic = self.s.queryAll(sql)
        return info_dic

    def admin_info(self):
        sql = "SELECT hostinfo,groupname FROM host;"
        info_dic = self.s.queryAll(sql)
        return info_dic

    def user_info(self):
        sql = "SELECT username FROM user;"
        info_dic = self.s.queryAll(sql)
        return info_dic

    def create_user(self,user_info):
        self.s.insert('user',user_info)
        self.s.commit()

    def create_host(self,host_info):
        self.s.insert('host',host_info)
        self.s.commit()

    def del_host(self,info):
        sql = "DELETE FROM host WHERE hostinfo LIKE '%s%s'" %(info,self.b)
        self.s.query(sql)
        self.s.commit()

    def del_user(self,info):
        sql = "DELETE FROM user WHERE username = '%s'" %info
        self.s.query(sql)
        self.s.commit()

    def modify_host(self,host,group):
        sql = "UPDATE host SET groupname = '%s' WHERE hostinfo LIKE '%s%s' " %(group,host,self.b)
        self.s.query(sql)
        self.s.commit()

