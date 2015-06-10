#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'

from UserClassMain import *
import socket

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


def ftp_client(user):
    n = '语法:\nput e:/abc.txt\nget 123.txt\nls'
    m_list = ['ls 查看目录下的文件','put 上传','get 下载']
    host = '127.0.0.1'
    port = 9999
    print('=====%s 欢迎登陆ftp服务=====\n您可有以下命令操作:'%user)
    print('+'*19)
    for i in m_list:
        print i
    print('+'*19)
    time.sleep(2)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.sendall(user)
    data = s.recv(1024)
    print data
    #s.close()
    print(n)
    while True:
        info = raw_input('请输入指令:').strip()
        if info == 'ls':
            s.sendall(info)
            data = s.recv(1024)
            print('+++++文件列表+++++')
            print data
            print('+'*18)









def ftp_login():
    while True:
        info = raw_input('请输入账号(输入exit返回到上级):').strip()
        if info == 'exit':
            break
        u = UserClass(info, 'xxx')
        if u.check_user() == False:
            print('输入的账号不存在，请输入正确的账号。\n')
            continue
        if u.lock_status() == 1:
            print('%s 账号已被锁定，请联系管理员。'%info)
            break
        else:
            status = False
            count = 3
            print('-'*35)
            while True:
                passwd = raw_input('请输入密码(输入exit返回到上级):').strip()
                if passwd == 'exit':
                    break
                if u.check_md5(passwd) == u.find_passwd():
                    #调ftp接口
                    print('Login')
                    break
                else:
                    count -= 1
                    print('密码输入错误，您还可尝试%s次'%count)
                if count == 0:
                    u.lock_user()
                    print('对不起，%s账号已锁定，请联系管理员解锁。'%info)
                    status = True
                    break
        if status:break




ftp_client('liyiliang')

