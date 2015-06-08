#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
from GameMainClass import *
import time
import os
choice = None
path = None
info_list = {}

#打印菜单列表
def meu_list(dic):
    global choice
    print('请选择:')
    for k,v in sorted(dic.items() ,key = lambda x:x[0] ,reverse=False):
        print k,v
    choice = raw_input('请输入编号:').strip()


#创建角色
def create_role():
    global info_list
    people = CreatePerson()
    people.init_name(path)
    people.init_age()
    people.init_sex()
    people.init_occ()
    people.init_money()
    people.init_lv()
    people.init_intodisk(path)
    info_list = people.load_info(path)

	
def into_disk(path, name, info_list):
    f = file('%s/%s.pkl' %(path, name),'wb')
    pickle.dump(info_list, f)
    f.close()


def load_info(path, name):
    with file('%s/%s.pkl' %(path, name),'rb') as f:
        info = pickle.load(f)
    return info

#主程序，所有逻辑都在这。
def login_game():
    global choice
    global path
    global info_list
    print('**********欢迎来到屌丝人生**********')
    meu1_list = {'1': '注册账号', '2': '登陆游戏', '3' :'退出'}
    meu2_list = {'1': '创建角色', '2': '返回到登陆页'}
    meu3_list = {'1': '创建新角色',  '2': '读档', '3': '返回到登陆页'}
    while True:
        meu_list(meu1_list)
        if choice == '1':
            acc = UserUse()
            acc.add_user()
        elif choice == '2':
            print('================================')
            login = UserUse()
            if login.login_user():
                print('登录成功......\n')
                time.sleep(1)
                account = login.find_account()
                path = 'userinfo/%s'%account
                while True:
                    if os.path.exists(path):
                        if os.listdir(path) == []:
                            print('***您目前没有角色，请创建角色***')
                            meu_list(meu2_list)
                            print('************************')
                            if choice == '1':
                                create_role()
                                sence = GameScene(info_list[0])
                                info_list = sence.GameRun(info_list)
                                into_disk(path, info_list[0], info_list)
                                print('%s角色已存档，退出当前角色!!!!'%info_list[0])
                            elif choice == '2':
                                break
                            else:
                                print('输入的编号不合法.')
                        else:
                            tmp_list = []
                            for i in os.listdir(path):
                                tmp_list.append(i.split('.')[0])
                            meu_list(meu3_list)
                            print('************************')
                            if choice == '1':
                                create_role()
                                sence = GameScene(info_list[0])
                                info_list = sence.GameRun(info_list)
                                into_disk(path, info_list[0], info_list)
                                print('%s角色已存档，退出当前角色!!!!'%info_list[0])
                            elif choice == '2':
                                print('您可选择如下角色:')
                                for i in tmp_list:
                                    print i
                                while True:
                                    info = raw_input('请输入角色名(exit返回上级):').strip()
                                    if info == 'exit':
                                        break
                                    if info not in tmp_list:
                                        print('输入的角色名不存在，请重新输入。')
                                    else:
                                        info_list = load_info(path,info)
                                        sence = GameScene(info)
                                        info_list = sence.GameRun(info_list)
                                        into_disk(path, info_list[0], info_list)
                                        print('%s角色已存档，退出当前角色!!!!'%info_list[0])
                                        break
                            elif choice == '3':
                                break
                            else:
                                print('输入的编号不合法.')
                    else:
                        os.mkdir(path)
                        print('***您目前没有角色，请创建角色***')
                        meu_list(meu2_list)
                        print('************************')
                        if choice == '1':
                            create_role()
                            sence = GameScene(info_list[0])
                            info_list = sence.GameRun(info_list)
                            into_disk(path, info_list[0], info_list)
                            print('%s角色已存档，退出当前角色!!!!'%info_list[0])
                        elif choice == '2':
                            break
                        else:
                            print('输入的编号不合法.')
        elif choice == '3':
            print('退出登陆页面....byebye!!')
            break
        else:
            print('请选择合法的编号。')


if __name__ == '__main__':
    login_game()
    #p = UserUse()
    #p.init_user()


