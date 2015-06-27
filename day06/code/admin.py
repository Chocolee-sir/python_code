#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
from UserMDBClass import UserInfo
import time

U = UserInfo('admin')

def meu(dic):
    for k,v in sorted(dic.items() ,key = lambda x:x[0] ,reverse=False):
        print k,v

def host_list():
    a = U.admin_info()
    tmp_list = []
    for i in a.items():
        tmp_list.append(i[1])
    print('++++++目前有以下主机++++++')
    print('主机\t\t\t属组')
    for i in range(len(tmp_list)):
        if i % 2 == 0:
            print tmp_list[i][0],tmp_list[i+1][0]
    print('++++++++++++++++++++++++++')


def user_list():
    a = U.user_info()
    print('+++++用户列表+++++')
    for k,v in a.items():
        print(v[0])
    print('++++++++++++++++++')

#此功能没做什么判断，有BUG，不浪费时间在这。
def add_host():
    print('=====================')
    ipaddr = raw_input('请输入ip地址:').strip()
    port = raw_input('请输入ssh连接端口:').strip()
    user = raw_input('请输入连接用户:').strip()
    passwd = raw_input('请输入连接密码:').strip()
    info_dic = {'hostinfo':'%s;%s;%s;%s'%(ipaddr,port,user,passwd)}
    U.create_host(info_dic)


#也有BUG，简单实现功能
def del_host():
    while True:
        host_list()
        choice = raw_input('请输入要删除的主机ip(exit返回):').strip()
        if choice == 'exit':
            break
        U.del_host(choice)
        print('已删除%s\n'%choice)
        time.sleep(1)


#有BUG，简单实现功能
def modify_group():
    while True:
        host_list()
        info = raw_input('请输入修改的主机ip(exit返回):').strip()
        if info == 'exit':
            break
        gname = raw_input('请输入属组名(exit返回):').strip()
        if gname == 'exit':
            break
        U.modify_host(info,gname)
        print('将%s的属组修改为%s\n'%(info,gname))
        time.sleep(1)


#简单实现功能，未多加判断，有BUG
def add_user():
    while True:
        user_list()
        username = raw_input('请输入账号(exit返回):').strip()
        if username == 'exit':
            break
        passwd = raw_input('请输入密码(exit返回):').strip()
        if  passwd == 'exit':
            break
        info_dic = {'username':username,'passwd':U.change_md5(passwd),'groupname':username}
        U.create_user(info_dic)
        print('用户添加成功。')

#简单实现
def del_user():
    while True:
        user_list()
        choice = raw_input('请输入要删除的用户(exit返回):').strip()
        if choice == 'exit':
            break
        U.del_user(choice)
        print('已删除用户%s\n'%choice)
        time.sleep(1)


#简单实现，未做复杂判断
def unlock_user():
    while True:
        a = U.lock_userlist()
        print('++++++锁定账户列表++++++')
        if a is None:
            print(a)
        else:
            for k,v in a.items():
                print(v[0])
        print('++++++++++++++++++++++++')
        info = raw_input('请输入要解锁的账户(exit返回):').strip()
        if info == 'exit':
            break
        U.unlock_user(info)
        print('%s账户已解锁'%info)
        time.sleep(1)


#主函数
def admin_run():
    main_meu = {
        '1':'主机操作',
        '2':'用户操作',
        '3':'退出'
    }

    host_meu = {
        '1':'查询主机',
        '2':'添加主机',
        '3':'删除主机',
        '4':'修改主机属组',
        '5':'返回上级菜单'
    }

    user_meu = {
        '1':'查询已有用户',
        '2':'添加用户',
        '3':'删除用户',
        '4':'解锁用户',
        '5':'返回上级菜单'
    }

    while True:
        meu(main_meu)
        choice = raw_input('请选择:').strip()
        if choice == '1':
            while True:
                meu(host_meu)
                choice = raw_input('请选择:').strip()
                if choice == '1':
                    host_list()
                elif choice == '2':
                    add_host()
                elif choice == '3':
                    del_host()
                elif choice == '4':
                    modify_group()
                elif choice == '5':
                    break
                else:
                    print('请输入正确的选项。')
        elif choice == '2':
            while True:
                meu(user_meu)
                choice = raw_input('请选择:').strip()
                if choice == '1':
                    user_list()
                elif choice == '2':
                    add_user()
                elif choice == '3':
                    del_user()
                elif choice == '4':
                    unlock_user()
                elif choice == '5':
                    break
                else:
                    print('请输入正确的选项。')
        elif choice == '3':
            break
        else:
            print('请输入正确的选项。')


if __name__ == '__main__':
    admin_run()
