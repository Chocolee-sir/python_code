#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'

from UserClassMain import *

def meu():
    dic = {
        '1': '注册FTP会员',
        '2': 'FTP会员登录',
        '3': '退出'
    }
    print('=====欢迎登录FTP服务系统=====')
    for k,v in sorted(dic.items() ,key = lambda x:x[0] ,reverse=False):
        print k,v



def register_user():
    while True:
        info = raw_input('请输入新会员账号(输入exit返回到上级):').strip()
        if info == 'exit':
            break
        u = UserClass(info, 'xxx')
        if u.check_user():
            print('输入的会员账号已存在，请输入其他的账号。\n')
            continue
        else:
            status = False
            while True:
                passwd_01 = raw_input('请输入密码(输入exit返回到上级):').strip()
                if passwd_01 == 'exit':
                    status = True
                    break
                passwd_02 = raw_input('请再次输入密码(输入exit返回到上级):').strip()
                if passwd_02 == 'exit':
                    status = True
                    break
                if passwd_01 == passwd_02:
                    u = UserClass(info, passwd_02)
                    u.add_user()
                    return
                else:
                    print('两次密码输入不相同，请重新输入。\n')
        if status:break

