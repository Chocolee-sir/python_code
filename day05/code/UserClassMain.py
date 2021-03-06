#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import hashlib,time
from DBClassMain import *
from hashlib import md5

#文件md5函数
def md5_file(name):
    m = md5()
    a_file = open(name, 'rb')    #需要使用二进制格式读取文件内容
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()


#用户逻辑类
class UserClass(object):
    s = DbInterface('10.10.206.193','chocolee','123456','chocolee')  #连接数据库信息

    def __init__(self,user,passwd):
        self.user = user
        self.passwd = passwd

    def check_md5(self, password):
        m = hashlib.md5()
        m.update(password)
        return m.hexdigest()

    def check_user(self):
        sql = "select 1 from user where username = '%s' limit 1" %self.user
        if self.s.query(sql) == 1:
            return True
        else:
            return False

    def find_passwd(self):
        sql = "select passwd from user where username = '%s'" %self.user
        return self.s.queryRow(sql)[0]

    def add_user(self):
        user_info = {'username': '%s'%self.user, 'passwd': '%s'%self.check_md5(self.passwd)}
        self.s.insert('user',user_info)
        self.s.commit()
        print('恭喜%s~~注册会员成功~~~'%self.user)
        return True

    def lock_status(self):
        if self.check_user():
            sql = "select flag from user where username = '%s'" %self.user
            return self.s.queryRow(sql)[0]
        else:
            return False

    def lock_user(self):
        if self.check_user():
            sql = "update user set flag = 1 where username = '%s'" %self.user
            self.s.query(sql)
            self.s.commit()
        else:
            return False

    def login_user(self):
        if self.lock_status() == 0:
            sql = "select passwd from user where username ='%s'" %self.user
            if self.check_md5(self.passwd) == self.s.queryRow(sql)[0]:
                return True
            else:
                return False
        else:
            return 'lock'

    def super_user(self):
        if self.user != 'admin':
            return
        print('----进入管理员解锁系统----\n')
        while True:
            tmp_list = []
            display_sql = 'select username from user where flag =1'
            lock_list = self.s.queryAll(display_sql)
            if lock_list != []:
                print('*****目前锁定的账号如下*****')
                for i in lock_list:
                    print i['username']
                    tmp_list.append(i['username'])
                print('*'*28)
                info = raw_input('请输入要解锁的账号(输入quit退出):').strip()
                if info == 'quit':
                    return
                if info not in tmp_list:
                    print('不要测BUG！！！请输入列表中账号~~~~')
                else:
                    unlock_sql = "update user set flag = 0 where username = '%s' " %info
                    self.s.query(unlock_sql)
                    self.s.commit()
                    print('%s已解锁'%info)
                    time.sleep(1)
            else:
                print('目前没有锁定的账号，输入quit退出~~')
                while True:
                    info = raw_input('input:').strip()
                    if info == 'quit':
                        return
                    else:
                        print('请输入正确！！！！')






