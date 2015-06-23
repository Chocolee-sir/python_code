#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import hashlib
from DBClassMain import *

class UserInfo(object):
    s = DbInterface('10.10.206.193','chocolee','123456','chocolee')

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
        sql = "SELECT flag FROM user where username = '%s';" %self.username
        return self.s.queryRow(sql)[0]

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

    def create_user(self,user_info):
        self.s.insert('user',user_info)
        self.s.commit()

    def create_host(self,host_info):
        self.s.insert('host',host_info)
        self.s.commit()

