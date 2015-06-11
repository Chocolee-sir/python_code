#!/usr/bin/env python
# encoding:utf-8
from __future__ import division
from UserClassMain import *
import socket,os,sys,time
__author__ = 'Chocolee'

def meu():
    dic = {
        '1': '注册FTP会员',
        '2': 'FTP会员登录',
        '3': '退出'
    }
    print('=====欢迎登录FTP服务系统=====')
    for k,v in sorted(dic.items() ,key = lambda x:x[0] ,reverse=False):
        print k,v


def progress_test(transfer_time):
    bar_length=20
    for percent in xrange(0, 101):
        hashes = '#' * int(percent/100.0 * bar_length)
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rPercent: [%s] %d%%"%(hashes + spaces, percent))
        sys.stdout.flush()
        time.sleep(transfer_time)


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
    n = '语法:\nput e:/abc.txt\nget 123.txt d:/\nls'
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
        info = raw_input('请输入指令(exit返回上级):').strip()
        if info == '':
            print('不能为空~~~~')
            continue
        if info == 'exit':
            break
        if info == 'ls':
            s.sendall(info)
            data = s.recv(1024)
            print('+++++文件列表+++++')
            print data
            print('+'*18)
        else:
            info = info.split()
            #print info
            if info[0] == 'put' or info[0] == 'get':
                if info[0] == 'put' and len(info) == 2:
                    if os.path.exists(info[1]):
                        file_name = os.path.basename(info[1])
                        file_size =os.stat(info[1]).st_size
                        s.send(info[0]+"|"+file_name+'|'+str(file_size))
                        #print(file_size)
                        send_size = 0
                        b= '%'
                        f = file(info[1],'rb')
                        flag = True
                        while flag:
                            if send_size + 4096 >file_size:
                                data = f.read()
                                flag  = False
                            else:
                                data = f.read(4096)
                                send_size += 4096
                                com = int(round(send_size/file_size*100))
                                sys.stdout.write("\r上传文件'%s': %d%s"%(file_name,com,b))
                                sys.stdout.flush()
                            s.send(data)
                        f.close()

                        print('\n')

                    else:
                        print('%s 不存在,请重新输入'%info[1])
                        continue
            else:
                print('语法错误~~请输入正确的语法！！')
                continue












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

