#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
from UserMDBClass import UserInfo
from ParamikoClass import ParamikoClass
import multiprocessing
import time

def UserLogin():
    while True:
        username = raw_input('请输入用户名(exit退出):').strip()
        if username == 'exit':
            break
        U = UserInfo(username)
        if U.find_user() is None:
            print('输入的用户不存在，请输入正确！！')
            continue
        if U.user_lockstatus() == 1:
            print('%s用户已锁定，请联系管理员解锁。'%username)
            break
        for i in range(3):
            password = raw_input('请输入密码(exit退出):').strip()
            if password == 'exit':
                break
            if U.find_pass() == U.change_md5(password):
                return U.ip_info()
            else:
                print('密码输入错误，您还可尝试%s次'%(2 - i))
                if i == 2:
                    U.lock_user()
                    print('密码输入错误3次，已锁定，请联系管理员解锁.')
                    return False


def paramiko_cmdrun(info,cmd):
    run = ParamikoClass(info[0],int(info[1]),info[2],info[3])
    try:
        run.cmd_run(cmd)
    except:
        print('%s连接失败，请检查~~~~'%info[0])



def cmd_run(ipinfo,iplist,cmd):
    info_list =[]
    tmp_list = []
    last_list = []
    for k,v in ipinfo.items():
        info_list.append(v)
    for i in info_list:
        tmp_list.append(i[0])
    if iplist[0] == 'all':
        last_list = info_list
    else:
        for n in iplist:
            if n not in tmp_list:
                print('%s不在列表中，请输入列表中的ip地址.'%n)
                return
            else:
                for i in info_list:
                    if n in i:
                        last_list.append(i)
    pool = multiprocessing.Pool(processes=2)
    for i in last_list:
        pool.apply_async(paramiko_cmdrun,(i,cmd,))
    pool.close()
    pool.join()


def run():
    ip_info = UserLogin()
    if ip_info != False:
        while True:
            print('~欢迎登陆~')
            print('++++++您可操作如下主机++++++')
            for k,v in ip_info.items():
                print(v[0])
            print('all')
            print('++++++++++++++++++++++++++++')
            print '支持批量远程执行命令，分发文件，从远端下载文件.\n' \
                  "语法:\n" \
                  "执行命令 cmd.run '8.8.8.8,192.168.1.1' 'cmd'\n" \
                  "分发文件 put.run 'all' 'localfilepath' 'remotepath'\n"
            break

        while True:
            cmd = raw_input('ipnut(exit退出):').strip().split("'")
            while '' in cmd:
                cmd.remove('')
            while ' ' in cmd:
                cmd.remove(' ')
            if cmd[0] == 'exit':
                break
            if cmd[0].strip() == 'cmd.run':
                if len(cmd) != 3:
                    print('输入错误，请输入正确的语法.')
                    continue
                cmd_run(ip_info,cmd[1].strip().split(','),cmd[2])


if __name__ == '__main__':
    run()