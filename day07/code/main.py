#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
from LogicSQLClass import *
from DemoClass import *
u = LSqlClass()


def userLogin():
    while True:
        user = raw_input('请输入用户名(exit退出):').strip()
        if user == 'exit':
            break
        flag = u.findFuserName(user)
        if flag == None:
            print('用户名不存在，请重新输入。')
            continue
        else:
            while True:
                passwd = raw_input('请输入密码(exit退出):').strip()
                if passwd == 'exit':
                    return
                if u.changeMd5(passwd) == u.findFuserPass(user):
                   # print('login')
                    return user
                else:
                    print('密码输入不正确，请重新输入.')


def mainRun():
    user = userLogin()
    if user != None:
        print('++++%s 欢迎登陆堡垒机系统++++\n'%user)
        while True:
            tmp_list = []
            print('您可操作以下主机组:')
            for k,v in u.UserGroupInfo(user).items():
                print(v[0])
                tmp_list.append(v[0])
            info = raw_input('请选择主机组(exit退出):').strip()
            if info == 'exit':
                print('byebye~~~')
                break
            if info not in tmp_list:
                print('Error!!!请输入正确的主机组名称....\n')
                continue
            while True:
                ip_list = []
                print('%s组有以下ip列表:'%info)
                for k,v in u.findGroupHosts(info).items():
                    print(v[0])
                    ip_list.append(v[0])
                ipinfo =raw_input('请输入远程连接的地址(exit返回):').strip()
                if ipinfo == 'exit':
                    break
                if ipinfo not in ip_list:
                    print('Error!!!请输入列表中的ip地址！！！')
                    continue
                host_list = []
                host_info = u.findHostInfo(ipinfo)
                for k,v in host_info.items():
                    host_list.append(str(v[0]))
                s = DemoSimple(host_list[0],int(host_list[1]),user,host_list[2],host_list[3])
                s.connect()



if __name__ == '__main__':
    mainRun()

