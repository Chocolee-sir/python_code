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
    time.sleep(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.sendall(user)
    data = s.recv(1024)
    print data
    print(n)
    while True:
        info = raw_input('请输入指令(exit返回上级):').strip()
        if info == '':
            print('不能为空~~~~')
            continue
        if info == 'exit':
            s.close()
            break
        if info == 'ls':
            s.sendall(info)
            data = s.recv(1024)
            print('+++++文件列表+++++')
            print data
            print('+'*18)
        else:
            info = info.split()
            recv_size = 0
            send_size = 0
            flag = True
            b = '%'
            if info[0] == 'put' or info[0] == 'get':
                if info[0] == 'put' and len(info) == 2:
                    if os.path.exists(info[1]):
                        file_name = os.path.basename(info[1])
                        file_size =os.stat(info[1]).st_size
                        s.send(info[0]+"|"+file_name+'|'+str(file_size))
                        f = file(info[1],'rb')
                        while flag:
                            if send_size + 1024 >file_size:
                                data = f.read(file_size - send_size)
                                flag  = False
                                sys.stdout.write("\r上传文件'%s': 100%s"%(file_name,b))
                            else:
                                data = f.read(1024)
                                send_size += 1024
                                com = int(round(send_size/file_size*100))
                                sys.stdout.write("\r上传文件'%s': %d%s"%(file_name,com,b))
                            sys.stdout.flush()
                            s.send(data)
                        f.close()
                        md5_num = s.recv(1024)
                        time.sleep(1)
                        if md5_num == md5_file('%s'%info[1]):
                            print(' MD5校验通过，传输成功....')
                            continue
                        else:
                            print(' MD5校验失败，传输失败....')
                            continue
                        print('\n')
                    else:
                        print('%s 不存在,请重新输入'%info[1])
                    continue

                elif info[0] == 'get' and len(info) == 3:
                    s.send('ls')
                    data = s.recv(1024)
                    tmp_list = data.split()
                    if info[1] in tmp_list:
                        if os.path.exists(info[2]):
                            path_file = '%s/%s' %(info[2],info[1])
                            s.send(info[0]+"|"+info[1])
                            data = s.recv(1024)
                            file_size = int(data)
                            f = file(path_file,'wb')
                            while flag:
                                if recv_size + 1024> file_size:
                                    recv_data = s.recv(file_size - recv_size)
                                    flag = False
                                    sys.stdout.write("\r下载文件'%s'至%s: 100%s"%(info[1],info[2],b))
                                else:
                                    recv_data = s.recv(1024)
                                    recv_size += 1024
                                    com = int(round(recv_size/file_size*100))
                                    sys.stdout.write("\r下载文件'%s'至%s: %s%s"%(info[1],info[2],com,b))
                                sys.stdout.flush()
                                f.write(recv_data)
                            f.close()
                            md5_num = s.recv(1024)
                            time.sleep(1)
                            if md5_num == md5_file(path_file):
                                print(' MD5校验通过，传输成功....')
                                continue
                            else:
                                print(' MD5校验失败，传输失败....')
                                continue
                            print('\n')
                        else:
                            print('输入的路径不存在，请输入正确的路径.')
                            continue
                    else:
                        print('%s文件在远端目录不存在，请输入ls, 查看存在的文件..'%info[1])
                        continue
                else:
                    print('语法错误~~请输入正确的语法！！')
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
                    ftp_client(info)
                    status = True
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


def running():
    while True:
        meu()
        choice = raw_input('请选择:').strip()
        if choice == '1':
            register_user()
        elif choice == '2':
            ftp_login()
        elif choice == '3':
            break
        else:
            print('请输入正确的选项。')


if __name__ == '__main__':
    running()



