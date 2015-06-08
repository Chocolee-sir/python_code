#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import credit_card_main as cardmain
import time,sys,os
import fileinput
#import readline
card_dic = {
    '12347998': ['96e79218965eb72c92a549dd5a330112', '15000', 15000],
    '12348888': ['e3ceb5881a0a1fdaad01296d7554868d', '10000', 10000]
}
admin_meu = {'1': '添加用户',
             '2': '删除用户',
             '3': '锁定用户',
             '4': '解锁用户',
             '5': '恢复到默认设置',
             '6': '修改密码',
	     '7': '退出'
}


#打印用户列表函数
def user_list():
    card_list1 = {}
    card_list1 = cardmain.import_card(card_list1)
    print('++++目前有以下卡号++++')
    for i in card_list1.items():
        print('+      %s      +'%i[0])
    print('++++++++++++++++++++++')


#添加用户函数
def add_user():
    print('####进入添加用户页面，如想返回上级菜单输入exit####')
    while True:
        user_list()
        card_list = {}
        status = False
        card_id = raw_input('请输入新的8位数字卡号（输入exit退出）:').strip()
        if card_id == 'exit' or card_id == 'EXIT':
            break
        if len(card_id) != 8 or card_id.isdigit() == False:
            print('闹呢？测BUG呢？？？？')
            continue
        card_list = cardmain.import_card(card_list)
        for i in card_list.items():
            if card_id == i[0]:
                print('卡号已存在，请输入其它8位数字卡号.')
                break
        else:
            while True:
                passwd = raw_input('请输入6位数字密码（输入exit退出）:').strip()
                if passwd == 'exit' or passwd == 'EXIT':
                    status = True
                    break
                if passwd.isdigit() == False or len(passwd) != 6:
                    print('闹呢？测BUG呢？？？？')
                    continue
                break
            if status:break
            while True:
                limit = raw_input('请输入额度(必须大于15000且是1000的整数)（输入exit退出）:').strip()
                if limit == 'exit' or limit == 'EXIT':
                    status = True
                    break
                if limit.isdigit() == False or int(limit) < 15000 or int(limit) % 1000 != 0:
                    print('闹呢？测BUG呢？？？？')
                    continue
                break
            if status:break
            card_list[card_id] = [cardmain.change_md5(passwd), limit, int(limit)]
            cardmain.dump_card(card_list)
            print('%s 卡号添加完成，额度为:%s'%(card_id,limit))
            time.sleep(2)
            #break


#删除用户函数
def del_user():
    print('####进入删除用户页面，如想返回上级菜单输入exit####')
    while True:
        user_list()
        card_list2 ={}
        card_id = raw_input('请输入要删除的ID（输入exit退出）：').strip()
        if card_id == 'exit' or card_id == 'EXIT':
            break
        if len(card_id) != 8 or card_id.isdigit() == False:
            print('闹呢？测BUG呢？？？？')
            continue
        card_list2 = cardmain.import_card(card_list2)
        for i in card_list2.items():
            if card_id == i[0]:
                card_list2.pop(card_id)
                cardmain.dump_card(card_list2)
                print('删除卡号%s.........'%card_id)
                time.sleep(1)
                print('删除成功~~~~~~')
                break
        else:
            print('您输入的ID不存在或有误...')
            continue
        #break


#锁定用户函数
def lock_user():
    print('####进入锁定用户页面，如想返回上级菜单输入exit####')
    while True:
        user_list()
        card_list3 = {}
        status = False
        card_id = raw_input('请输入要锁定的ID（输入exit退出）:').strip()
        if card_id == 'exit' or card_id == 'EXIT':
            break
        if len(card_id) != 8 or card_id.isdigit() == False:
            print('闹呢？测BUG呢？？？？')
            continue
        card_list3 = cardmain.import_card(card_list3)
        for i in card_list3.items():
            if card_id == i[0]:
                cardid = '%s\n' %card_id
                with file('lock.txt','r+') as f:
                    if f != "":
                        for i in f.readlines():
                            if cardid == i:
                                print('%s此卡已锁定，不能重复锁定'%card_id)
                                status = True
                                break
                        else:
                            f.write(cardid)
                            print('已将%s此卡锁定......'%card_id)
                            time.sleep(1)
                            status = True
                    else:
                        f.write(cardid)
                        print('已将%s此卡锁定......'%card_id)
                        time.sleep(1)
                        status = True
            if status:break
        #if status:break
        else:
            print('输入的卡号不存在....')
            break


#解锁用户函数
def unlock_user():
    print('####进入解锁用户页面，如想返回上级菜单输入exit####')
    while True:
        user_list()
        card_list4 = {}
        status = False
        card_id = raw_input('请输入要解锁的ID（输入exit退出）:').strip()
        if card_id == 'exit' or card_id == 'EXIT':
            break
        if len(card_id) != 8 or card_id.isdigit() == False:
            print('闹呢？测BUG呢？？？？')
            continue
        card_list4 = cardmain.import_card(card_list4)
        for i in card_list4.items():
            if card_id == i[0]:
                cardid = '%s\n' %card_id
                with file('lock.txt','r') as f:
                    if f != '':
                        for i in f.readlines():
                            if cardid == i:
                                f.close()
                                for line in fileinput.input('lock.txt',inplace=1):
                                    line = line.replace(cardid,'')
                                    print line,
                                print('已将%s卡解锁~~~~'%card_id)
                                status = True
                                break
                        else:
                            print('%s此卡没有锁定...'%card_id)
                            status = True
                    else:
                        print('%s此卡没有锁定...'%card_id)
                        status = True
            if status:break
        #if status:break
        else:
            print('能不能别测BUG了~~~')


#修改密码函数
def modify_pass():
    print('####进入修改密码页面，如想返回上级菜单输入exit####')
    while True:
        user_list()
        card_list5 = {}
        status = False
        number = raw_input('请输入要修改密码的ID（输入exit退出）:').strip()
        if number == 'exit' or number == 'EXIT':
            break
        if len(number) != 8 or number.isdigit() == False:
            print('闹呢？测BUG呢？？？？')
            continue
        card_list5 = cardmain.import_card(card_list5)
        for i in card_list5.items():
            if number == i[0]:
                cardmain.modify_passwd(number)
                status = True
                break
        else:
            print('输入的ID不存在....')
        #if status:break


#恢复默认函数
def default():
    cardmain.dump_card(card_dic)
    os.system('>lock.txt')
    os.system('>consume.txt')     
    print('已恢复到默认设置.....')
    sys.exit(0)


#程序主函数
def meu_run():
    while True:
        cardmain.dic(admin_meu,'admin system')
        info = raw_input('尊敬的管理者，请输入服务编号:').strip()
        if info.isdigit() == False or int(info) > 7 or int(info) < 1:
            print('别测BUG了，OK？？')
            continue
        if info == '1':
            add_user()
        if info == '2':
            del_user()
        if info == '3':
            lock_user()
        if info == '4':
            unlock_user()
        if info == '5':
            default()
        if info == '6':
            modify_pass()
        if info == '7':
            print('Byebye~~~~')
            sys.exit(0)

if __name__ == '__main__':
    meu_run()
