#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
from LogicSQLClass import *
import time
u = LSqlClass()

def meu(dic):
    for k,v in sorted(dic.items() ,key = lambda x:x[0] ,reverse=False):
        print k,v

#简单实现有BUG
def addFuser():
    while True:
        user = raw_input('请输入用户名(exit返回上级):').strip()
        if user == 'exit':
            break
        passwd = raw_input('请为用户创建密码(exit返回上级):').strip()
        if passwd == 'exit':
            break
        if u.addFloginUser(user,passwd) == False:
            print('用户已存在，请重新输入。')
            continue
        else:
            print('创建用户%s成功，请牢记密码.'%user)
            time.sleep(1)
            break

#简单实现有BUG
def addHosts():
    while True:
        host = raw_input('请输入主机ip:').strip()
        port = raw_input('请输入主机端口:').strip()
        user = raw_input('请输入主机登陆用户:').strip()
        if user == "":
            user == 'root'
        passwd = raw_input('请输入主机登陆密码:').strip()
        u.addHost(host,port,user,passwd)
        print('创建主机 %s 成功。'%host)
        time.sleep(1)
        break

def findHosts():
    info = u.findHost()
    print('++++++++++++++++++++++++')
    if info == {}:
        print('没有可分配的主机!')
    else:
        print('目前有如下未分组主机:')
        for k,v in info.items():
            print(v[0])
    print('++++++++++++++++++++++++')

#简单实现，有BUG
def groupInfo():
    while True:
        info = u.findGroup()
        if info == {}:
            print('目前没有分组，请创建主机组。注意：一个主机组至少包含一个主机！')
            time.sleep(1)
            gname = raw_input('创建一个主机组:').strip()
            findHosts()
            ghost = raw_input('请选择一个未分组的主机ip:').strip()
            gid = 1
            u.addGroup(gname,gid,ghost)
            print('创建%s组成功！'%gname)
            continue
        else:
            print('******************************')
            print('目前有如下组:')
            for k,v in info.items():
                print(v[0])
                if k % 2 == 0:
                    print('------------------')
            print('******************************')
            meu_dic = {
                '1':'创建新的主机组',
                '2':'为主机组添加主机',
                '3':'返回到上级菜单'
            }
            meu(meu_dic)
            choice = raw_input('请选择:').strip()
            if choice == '1':
                while True:
                    gname = raw_input('创建一个主机组:').strip()
                    findHosts()
                    ghost = raw_input('请选择一个未分组的主机ip(exit返回):').strip()
                    if ghost == 'exit':
                        break
                    gid = u.findGid() + 1
                    u.addGroup(gname,gid,ghost)
                    print('创建%s组成功！'%gname)
                    break
            elif choice == '2':
                while True:
                    print('有如下组：')
                    dic_info = u.findGroupName()
                    for k,v in dic_info.items():
                        print(v[0])
                    gname = raw_input('请选择一个主机组(exit返回):').strip()
                    if gname == 'exit':
                        break
                    findHosts()
                    ghost = raw_input('请选择一个未分组的主机ip(exit返回):').strip()
                    if ghost == 'exit':
                        break
                    gid = u.findGnameGid(gname)
                    u.addGroup(gname,gid,ghost)
                    print('为%s组添加%s主机成功！'%(gname,ghost))
                    time.sleep(1)
                    break
            elif choice == '3':
                break
            else:
                print('请输入正确的选项。')


#简单实现，有BUG
def userInfo():
    meu_user = {
        '1':'查看用户包含的主机组信息',
        '2':'为用户添加主机组',
        '3':'返回上级菜单'
    }
    while True:
        print('*******************')
        meu(meu_user)
        print('*******************')
        choice = raw_input('请选择:').strip()
        if choice == '1':
            print('目前有如下用户:')
            user_dic = u.findFuser()
            for k,v in user_dic.items():
                print(v[0])
            user = raw_input('请输入用户名查询:')
            userinfo = u.UserGroupInfo(user)
            print('用户%s包含的主机组信息:' %user)
            for k,v in userinfo.items():
                print(v[0])
            time.sleep(1)
        elif choice == '2':
            while True:
                print('目前有如下用户:')
                user_dic = u.findFuser()
                for k,v in user_dic.items():
                    print(v[0])
                user = raw_input('请输入用户:').strip()
                print('目前有如下组:')
                dic_info = u.findGroupName()
                for k,v in dic_info.items():
                    print(v[0])
                group = raw_input('请选择一个组:').strip()
                gid = u.findGnameGid(group)
                u.addUserInfo(user,gid,'root')
                print('为%s用户添加%s组'%(user,group))
                break
        elif choice == '3':
            break
        else:
            print('请输入正确的选项。。')


def adminRun():
    admin_meu = {
        '1':'创建堡垒机用户',
        '2':'添加主机',
        '3':'主机组操作',
        '4':'用户添加主机组操作',
        '5':'退出'
    }

    while True:
        print('+++++++++++++++++++++++')
        meu(admin_meu)
        print('+++++++++++++++++++++++')
        choice = raw_input('请选择:').strip()
        if choice == '1':
            addFuser()
        elif choice == '2':
            addHosts()
        elif choice == '3':
            groupInfo()
        elif choice == '4':
            userInfo()
        elif choice == '5':
            print('byebye~~')
            break
        else:
            print('请输入正确的选项.')

if __name__ == '__main__':
    adminRun()
