#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import hashlib
import pickle
import time,sys
import re
#import readline
atm_dic = {'1':'查询可用额度','2':'取现','3':'还款','4':'转账','5':'修改密码','6':'查看上月账单','7':'退卡'}
number = ''

#退出函数
def atm_exit():
    while True:
        info = raw_input('输入0可返还到上级菜单:')
        if info == "0":
            break


#打印字典函数
def dic(dic,info):
    print('*****%s*****'%info)
    l = len('*****%s*****'%info)
    for k,v in sorted(dic.items() ,key = lambda x:x[0] ,reverse=False):
        print k,v
    print('*'*l)


#记录消费记录函数
def load_log(time,card_num,action,money):
    with file('consume.txt', 'a+') as f:
        f = f.write('%s %s %s %s\n' %(time, card_num, action, money))


#时间函数
def action_time():
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    return t

	
#寻找账号函数
def find_card():
    info = account
    return info


#序列化函数，将内存内容落地
def dump_card(name_info):
    f = file('dump_into_disk.pkl', 'wb')
    pickle.dump(name_info,f)
    f.close()


#序列化函数，将文件内容加载到内存
def import_card(info):
    with file('dump_into_disk.pkl', 'rb') as f:
        info = pickle.load(f)
    return info


#md5密码转换函数
def change_md5(passwd):
    pwd = None
    m = hashlib.md5()
    m.update(passwd)
    pwd = m.hexdigest()
    return pwd


#用户登录验证函数
def auth_user():
    global account
    card_dic = {}
    loginStatus = False
    lockStatus = False
    count = 0
    while True:
        account = raw_input('请输入信用卡卡号:').strip()
        if account == "":
            print('卡号不能为空，请重新输入。')
            continue
        card_dic = import_card(card_dic)
        for i in card_dic.items():
            if account == i[0]:
                with file('lock.txt', 'r') as lock_list:
                    if lock_list != "":
                        lock_list = lock_list.readlines()
                        for n in lock_list:
                            if account == n.split()[0]:
                                print('此卡已锁定，请联系银行工作人员。')
                                lockStatus = True
                                break
                if lockStatus:break
                find_card()
                for m in range(3):
                    pwd = raw_input('请输入密码:').strip()
                    if card_dic[account][0] == change_md5(pwd):
                        loginStatus = True
                        return loginStatus
                    else:
                        count += 1
                        a = 3 - count
                        print('密码错误，您还可以尝试错误输入%s次。' %a)
                    if count == 3:
                        print('密码错误输入3次，卡号%s已锁定。如要解锁，请联系银行工作人员。'%account)
                        with file('lock.txt','a') as f:
                            f.write('%s\n' %account)
                        lockStatus = True
                        break
        if lockStatus:break
        else:
            print('未识别的卡号，请重新输入。')


#账单函数
def bill(card_number):
    m_list = []
    tmp_list = []
    last = 0
    with file('consume.txt', 'r') as f:
        if f != '':
            f = f.readlines()
            for n in f:
                if card_number == n.strip().split()[2]:
                    if '还款' in n.strip().split():
                        print('\033[1;31;40m%s\033[0m'%n.strip())
                    else:
                        print(n.strip())
            for n in f:
                if card_number == n.strip().split()[2]:
                    e = n.strip().split()[3:]
                    for i in e:
                        p = re.findall('^-?\d+$',i)
                        m_list.append(p)
                    while [] in m_list:
                        m_list.remove([])
                    tmp_list = reduce(lambda x,y:x+y,m_list)
            if tmp_list != []:
                for n in tmp_list:
                    last += int(n)
                print('您本期全部应还款额：%s元'%last)
            else:
                print('本期未消费...')
        else:
            print('本期未消费...')
            return


#取现函数
def atm_cash():
    print('####进入取现页面，如想返回上级菜单输入exit####')
    card_list2 = {}
    while True:
        print('注意：最低提现100元，提现金额为100的整数倍，手续费为%5\n')
        m =raw_input('请输入您要提现的金额:').strip()
        if m.isdigit():
            if int(m) < 100:
                print('金额小于100元，无法提现。')
                continue
            elif int(m)%100 == 0:
                card_list2 = import_card(card_list2)
                for i in card_list2.items():
                    if number == i[0]:
                        info_list = card_list2[number]
                        if float(info_list[-1]) < float(m):
                            print('对不起，余额不足。')
                            break
                        else:
                            quota = float(info_list[-1]) - float(m) - float(m)*0.05
                            info_list[-1] = quota
                            card_list2[number] = info_list
                            dump_card(card_list2)
                            q = '%s 手续费 %s' %(m,int(int(m)*0.05))
                            load_log(action_time(),number,'取现',q)
                            print('本次提现:%s元  手续费:%s元\n剩余金额:%s元'%(m,float(m)*0.05,quota))
                            time.sleep(2)
                break
            else:
                print('能不能输入100的整数？？')
                continue
        elif m == 'exit' or m == 'EXIT':
            break
        else:
            print('哥们儿，你是在测BUG吗？？')
            continue


#还款函数
def atm_repayment():
    print('####进入还款页面，如想返回上级菜单输入exit####')
    card_list3 = {}
    while True:
        m = raw_input('请输入还款金额:').strip()
        if m.isdigit() and float(m) > 0:
            card_list3 = import_card(card_list3)
            for i in card_list3.items():
                if number == i[0]:
                    info_list = card_list3[number]
                    quota = float(info_list[-1]) + float(m)
                    info_list[-1] = quota
                    card_list3[number] = info_list
                    dump_card(card_list3)
                    q = '-%s' %m
                    load_log(action_time(),number,'还款',q)
                    print('还款成功，您本次还款金额:%s元'%m)
                    time.sleep(2)
            break
        elif m == 'exit' or m == 'EXIT':
            break
        else:
            print('哥们儿，你是在测BUG吗？？')
            continue


#转账函数
def atm_transfer():
    print('####进入转账页面，如想返回上级菜单输入exit####')
    card_list4 = {}
    status = False
    tran = False
    while True:
        card_number = raw_input('请输入收款人账号:').strip()
        card_list4 = import_card(card_list4)
        for i in card_list4.items():
            if card_number == i[0]:
                info_list = card_list4[card_number]
                if card_number == number:
                    print('不能给自己转账！！！！你是没事找事吗？')
                    break
                money = raw_input('请输入转账金额:').strip()
                if money.isdigit() and float(money) > 0:
                    quota = float(info_list[-1]) + float(money)
                    info_list[-1] = quota
                    card_list4[card_number] = info_list
                    for i in card_list4.items():
                        if number == i[0]:
                            info_list = card_list4[number]
                            if float(info_list[-1]) < float(money):
                                print('金额不足~~转账失败')
                                time.sleep(1)
                                status = True
                                break
                            else:
                                quota = float(info_list[-1]) - float(money)
                                info_list[-1] = quota
                                card_list4[number] = info_list
                                dump_card(card_list4)
                                load_log(action_time(),number,'转账',money)
                                print('转账成功！！给%s卡转账金额:%s元'%(card_number,float(money)))
                                time.sleep(1)
                                status = True
                                break
                else:
                    print('哥们儿，你是在测BUG吗？？')
                    break
            elif card_number == 'exit' or card_number == 'EXIT':
                tran = True
            if tran:break
            if status:break
        else:
            print('收款人账号不存在.......')
            time.sleep(1)
            break
        if tran:break
        if status:break


#修改密码函数
def modify_passwd(number):
    print('####进入修改密码页面，如想返回上级菜单输入exit####')
    card_list5 = {}
    while True:
        passwd_1 = raw_input('请输入6位数字的新密码:').strip()
        if passwd_1 == 'exit':
            break
        if passwd_1.isdigit() == False or len(passwd_1) != 6:
            print('测BUG？能不能输入正确的格式？')
            continue
        passwd_2 = raw_input('请再次输入新的密码:').strip()
        if passwd_1 == passwd_2:
            card_list5 = import_card(card_list5)
            for i in card_list5.items():
                if number == i[0]:
                    info_list = card_list5[number]
                    info_list[0] = change_md5(passwd_2)
                    card_list5[number] = info_list
                    dump_card(card_list5)
                    print('密码修改成功。')
                    time.sleep(1)
                    break
        else:
            print('两次密码输入不相同，请重新输入!')
            time.sleep(1)
            continue
        break

		
#atm程序主函数
def atm_run():
    global number
    print('####欢迎来到ATM机####')
    login_return = auth_user()
    number = find_card()
    if login_return:
        while True:
            dic(atm_dic,'Welcome card:%s'%number)
            choice = raw_input('输入您想要办理的业务编号:').strip()
            if choice == "7":
                print('退卡中......')
                time.sleep(0.5)
                print('已退卡，再见。')
                return
            if choice not in atm_dic.keys() or choice == "":
                print('输入错误，请输入正确的编号！\n')
                time.sleep(1)
                continue
            if choice == '1':
                card_list1 = {}
                card_list1 = import_card(card_list1)
                for i in card_list1.items():
                    if number == i[0]:
                        print('%s 卡固额：%s元 | 可用余额：%s元'%(number,card_list1[number][-2],card_list1[number][-1]))
                        atm_exit()
            if choice == '2':
                atm_cash()
            if choice == '3':
                atm_repayment()
            if choice == '4':
                atm_transfer()
            if choice == '5':
                modify_passwd(number)
            if choice == '6':
                print('####进入查询账单页面，如想返回上级菜单输入0####')
                bill(number)
                atm_exit()
    else:
        print('退出ATM机系统')


if __name__ == "__main__":
    atm_run()




