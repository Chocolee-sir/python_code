#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
from UserClass import UserInfo

def UserLogin():
    while True:
        username = raw_input('请输入用户名:').strip()
        U = UserInfo(username)
        if U.find_user() is None:
            print('输入的用户不存在，请输入正确！！')
            continue
        if U.user_lockstatus() == 1:
            print('%s用户已锁定，请联系管理员解锁。'%username)
            break
        for i in range(3):
            password = raw_input('请输入密码:').strip()
            if U.find_pass() == U.change_md5(password):
                print('login')
                return True
            else:
                print('密码输入错误，您还可尝试%s次'%(2 - i))
                if i == 2:
                    U.lock_user()
                    print('密码输入错误3次，已锁定，请联系管理员解锁.')
                    return False



UserLogin()