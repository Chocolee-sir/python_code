#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import pickle
import os
import hashlib
import fileinput
import time
import random

#创建人物的类
class CreatePerson(object):
    proper = []
    def init_name(self, path):
        while True:
            info = raw_input('创建一个角色名:').strip()
            if os.path.isfile('%s/%s.pkl'%(path, info)):
                print('角色名已存在，请输入其他的角色名.')
                continue
            else:
                self.proper.append(info)
                break

    def init_age(self):
        while True:
            info = raw_input('输入角色年龄:').strip()
            if info.isdigit() is False or int(info) >100:
                print('输入的年龄不合法，请重新输入。')
                continue
            else:
                self.proper.append(info)
                break

    def init_print(self, dic, i):
        while True:
            for k,v in dic.items():
                print k,v
            info = raw_input('请选择%s(1或2):'%i).strip()
            if info not in dic.keys():
                print('输入有误，请重新输入。')
                continue
            else:
                self.proper.append(dic[info])
                break

    def init_sex(self):
        dic = {'1': 'male', '2': 'female'}
        self.init_print(dic, '性别')

    def init_occ(self):
        dic = {'1': 'Development', '2': 'Operation'}
        self.init_print(dic, '职业')

    def init_money(self):
        self.proper.append(10000)

    def init_lv(self):
        self.proper.append(1)

    def init_intodisk(self, path):
        f = file('%s/%s.pkl' %(path, self.proper[0]),'wb')
        pickle.dump(self.proper, f)
        f.close()

    def load_info(self, path):
        with file('%s/%s.pkl' %(path, self.proper[0]),'rb') as f:
            info = pickle.load(f)
        return info

#创建账号的类
class UserUse(object):
    account = None

    def change_md5(self, passwd):
        pwd = None
        m = hashlib.md5()
        m.update(passwd)
        pwd = m.hexdigest()
        return pwd

    def find_account(self):
        global account
        info = account
        return info

    def dump_userlist(self, info):
        f = file('userlist.pkl', 'wb')
        pickle.dump(info,f)
        f.close()

    def init_user(self):
        dic = {'abc': '123'}
        self.dump_userlist(dic)

    def import_userlist(self):
        with file('userlist.pkl', 'rb') as f:
            info = pickle.load(f)
        return info

    def add_user(self):
        user_dic = self.import_userlist()
        status = False
        while True:
            account = raw_input('请输入注册账号:').strip()
            if account == '':
                print('输入不能为空，请重新输入。')
                continue
            if account in user_dic.keys():
                print('账号已存在，请用其他账号。')
                continue
            else:
                while True:
                    passwd_1 = raw_input('请输入密码:').strip()
                    passwd_2 = raw_input('请再次输入密码:').strip()
                    if passwd_1 == '':
                        print('对不起，密码不能为空.')
                        continue
                    if passwd_1 != passwd_2:
                        print('两次密码输入不同，请重新输入。')
                        continue
                    else:
                        user_dic[account] = self.change_md5(passwd_2)
                        self.dump_userlist(user_dic)
                        print('恭喜~~~%s用户注册成功~~请牢记您的密码'%account)
                        status = True
                        break
            return True

    def login_user(self):
        global account
        user_dic = {}
        loginStatus = False
        lockStatus = False
        count = 0
        while True:
            account = raw_input('请输入账号:').strip()
            if account == "":
                print('卡号不能为空，请重新输入。')
                continue
            user_dic = self.import_userlist()
            if account in user_dic.keys():
                with file('lock.txt', 'r') as lock_list:
                    if lock_list != "":
                        lock_list = lock_list.readlines()
                        for n in lock_list:
                            if account == n.split()[0]:
                                print('此卡已锁定，请联系客服。')
                                lockStatus = True
                                break
                if lockStatus:break
                self.account = account
                self.find_account()
                for m in range(3):
                    pwd = raw_input('请输入密码:').strip()
                    if user_dic[account] == self.change_md5(pwd):
                        loginStatus = True
                        return loginStatus
                    else:
                        count += 1
                        a = 3 - count
                        print('密码错误，您还可以尝试错误输入%s次。' %a)
                    if count == 3:
                        print('密码错误输入3次，卡号%s已锁定。如要解锁，请联系客服。'%account)
                        with file('lock.txt','a') as f:
                            f.write('%s\n' %account)
                        lockStatus = True
                        break
                if lockStatus:break
            else:
                print('账号不存在~~~~~')


#场景类
class GameScene(object):

    def __init__(self, name):
        self.name = name

    def print_dic(self,dic):
        print('*********有如下选择*********')
        for k,v in sorted(dic.items() ,key = lambda x:x[0] ,reverse=False):
            print k,v

    def start(self):
        info ='%s 你好，欢迎进入屌丝世界。你可能是运维或者是开发' \
            '，在这里，只要你怀着坚强而勇敢、仁慈而善良的信念，一切皆有可能。\n' %self.name
        print info
        time.sleep(3)

    def study(self, info_list):
        dic = {'1':'老男孩运维 学费5000','2':'老男孩python 学费6000','3':'MBA 学费500000'}
        self.print_dic(dic)
        while True:
            choice = raw_input('请输入编号(exit返回上级):').strip()
            if choice == '1':
                if info_list[-2] < 5000:
                    print('你连学习的钱都没有，都不知道你是怎么混的？可怜之人，必有可恨之处！')
                else:
                    if info_list[-1] <= 15:
                        print('你选择了老男孩运维，苦逼了5个月，战斗力今非昔比~~~~快去挑战吧！！')
                        info_list[-2] = info_list[-2] - 5000
                        info_list[-1] = info_list[-1] + 3
                    else:
                        print('你都这水平了，还来老男孩运维，老男孩老师不想教你，别来运维0基础装逼。')
            elif choice == '2':
                if info_list[-2] < 6000:
                    print('你连学习的钱都没有，都不知道你是怎么混的？可怜之人，必有可恨之处！')
                else:
                    if info_list[-1] < 30:
                        print('你选择了老男孩python，苦逼了4个月，战斗力今非昔比~~~~快去挑战吧！！')
                        info_list[-2] = info_list[-2] - 6000
                        info_list[-1] = info_list[-1] + 4
                    else:
                        print('alex不想教你，你太他妈装逼了！！！！')
            elif choice == '3':
                if info_list[-2] < 500000:
                    print('MBA可是你这等屌丝能玩的起的？？')
                else:
                    print('你选择了MBA，交到了一群发烧友，屌丝逆袭从此开始！')
                    info_list[-2] = info_list[-2] - 500000
                    info_list[-1] = info_list[-1] + 30
            elif choice == 'exit':
                break
            else:
                print('鸡巴蛋，测个毛的BUG~~~~')

    def work(self, info_list):
        salary = info_list[-1] * 1000
        info_list[-2] = info_list[-2] + salary
        print('%s 恭喜~~经过1个月的辛勤劳动，你得到了%s的薪水~~~相信自己，总有一天能赢取白富美。'%(self.name,salary))

    def find_girl(self, info_list):
        dic = {'1': '黑穷丑 最低要求Lv:15','2': '白富美 最低要求Lv:100'}
        self.print_dic(dic)
        while True:
            choice = raw_input('请输入编号(exit返回上级):').strip()
            if choice == '1':
                print('%s: Hi baby,能当俺媳妇不?'%self.name)
                time.sleep(2)
                if info_list[-1] < 15:
                   print('黑穷丑:小逼崽子，就你那怂样，还想娶老婆，等你牛逼点再来找姐吧，没准姐还能看给你洗脚的机会~')
                else:
                    print('黑穷丑:可以啊，哥哥，今晚需要妹子伺候你不？？来嘛~~爱死你了~~~')
                    time.sleep(2)
                    print('%s:他妈的，有钱就是不一样~~~~~~~\n ~~屁颠屁颠开房去了！！！！'%self.name)
                    time.sleep(2)
            elif choice == '2':
                print('%s: Hi girl,能不能给俺一个机会?'%self.name)
                time.sleep(2)
                if info_list[-1] < 100:
                    print('白富美:你有车吗？你有房吗？你有贷款吗？你能给我买得起10万块的包包吗？如果不能，凭什么想上我？')
                    time.sleep(2)
                    print('%s:...........我去，败家娘们儿，总有一天爷让你给我端洗脚水~~'%self.name)
                    time.sleep(2)
                else:
                    print('白富美:爷，您来了啊？今晚咱们去哪XXOO？我看上一双鞋，才20万，帮我买了吧~~~~')
                    time.sleep(2)
                    print('%s: 我的无限信用卡，没有密码，拿去随便刷~~~~'%self.name)
                    time.sleep(2)
                    print('白富美:爱死你了，么么哒。。。')
                    time.sleep(2)
                    print('%s:这就是现实~~~~,操了，爷今晚好好陪你玩！！\n希尔顿走着~~~~~'%self.name)
                    time.sleep(2)
            elif choice == 'exit':
                break
            else:
                print('不要测BUG了~~~~~~')

    def make_friends(self,  info_list):
        dic = {'1': '技术屌丝(最低Lv:10 每次消耗金钱:1000,Lv提升1)','2': 'IT精英(最低Lv:50,每次消耗金钱:100000,Lv提升3)'}
        self.print_dic(dic)
        while True:
            choice = raw_input('请输入编号(exit返回上级):').strip()
            if choice == '1':
                print('%s:屌丝哥，我们交个朋友吧~~'%self.name)
                time.sleep(2)
                if info_list[-1] < 10:
                    print('技术屌丝:哥们儿，不是我看不起你，你实在太弱小了，我都不想搭理你。')
                    time.sleep(2)
                else:
                    if info_list[-2] < 1000:
                        print('技术屌丝:兄弟，连吃饭的钱都付不起，怎么交朋友啊？？努力挣钱吧')
                        time.sleep(2)
                    else:
                        info_list[-1] = info_list[-1] + 1
                        info_list[-2] = info_list[-2] - 1000
                        print('技术屌丝:哥们，我请你吃放吧~~我还想问你python怎么写呢？我还不会写╮(╯▽╰)╭')
                        time.sleep(2)
                        print('%s:(*@ο@*) 哇～'%self.name)
                        time.sleep(2)
            elif choice == '2':
                print('%s:大神，我们做朋友吧~~'%self.name)
                time.sleep(2)
                if info_list[-1] < 50:
                    print('IT精英:你想成为我朋友？资本在哪里？')
                    time.sleep(2)
                else:
                    if info_list[-2] < 100000:
                        print('IT精英:原来你是个屌丝啊，没钱装孙子啊~~~~')
                        time.sleep(2)
                    else:
                        info_list[-1] = info_list[-1] + 3
                        info_list[-2] = info_list[-2] - 100000
                        print('IT精英:来来来，咱们研究下google架构问题~~~~~~')
                        time.sleep(2)
                        print('%s:嗯哼~'%self.name)
                        time.sleep(2)
            elif choice == 'exit':
                break
            else:
                print('这个不是BUG~~~~')

    def make_money(self, info_list):
        dic = {'1': '创业(Lv:最低20)', '2': '炒股(Lv:最低2)'}
        tmp_list = [0.1]*9 + [100]
        print('******在这里，要么达到人生巅峰，要么万劫不复！！！望君慎重慎重******')
        self.print_dic(dic)
        while True:
            choice = raw_input('请输入编号(exit返回上级):').strip()
            if choice == '1':
                if info_list[-1] < 20:
                    print('%s 再修炼修炼，等到20级了再来挑战吧' %self.name)
                    time.sleep(2)
                    break
                else:
                    if info_list[-2] > 200000:
                        num = random.choice(tmp_list)
                        if num == 100:
                            info_list[-1] = info_list[-1] + 100
                            info_list[-2] = info_list[-2] * 100
                            print('恭喜你%s~~~~创业成功，资产提升100倍，等级增加100级，你可以少奋斗200年了~~~'%self.name)
                            time.sleep(2)
                        else:
                            info_list[-1] = info_list[-1] + 2
                            info_list[-2] = info_list[-2] * 0.1
                            print('失败就失败了吧，大不了重头再来！！加油%s!!!资产缩水9成，等级增加2级。'%self.name)
                            time.sleep(2)
                    else:
                        print('%s 资金不足，等你资产超过20万了再来挑战吧' %self.name)
                        time.sleep(2)
                        break
            if choice == '2':
                if info_list[-1] < 2:
                    print('%s你是在拿钱玩命吗？穷逼还是别玩股票了。。。'%self.name)
                    time.sleep(2)
                    break
                else:
                    if info_list[-2] > 100:
                        num = random.randrange(20)
                        if num < 10:
                            info_list[-1] = info_list[-1] - 1
                            info_list[-2] = info_list[-2] * num * 0.1
                            s = 10 - num
                            print('%s，你的资产缩水%s成，等级下降1级，还想玩股票吗？股市有风险，投资需谨慎！'%(self.name, s))
                            time.sleep(2)
                        else:
                            info_list[-2] = info_list[-2] * num * 0.1
                            s = num - 10
                            print('%s,运气不错，资产增加%s成，股票好刺激啊~~股市有风险，投资需谨慎。'%(self.name, s))
                            time.sleep(2)
                    else:
                        print('你连100块都没有了，还玩股票。。。100块都不给我。。100块都不给我。。穷孙子！')
                        time.sleep(2)
                        break
            elif choice == 'exit':
                break
            else:
                print('BUG，no no no  not BUG~~~~')

    def GameRun(self,info_list):
        self.start()
        dic = {'1': '学习','2': '找性福','3': '工作','4': '交友','5': '想不想一夜暴富'}
        while True:
            print '\033[1;31;40m%s属性 Lv:%s Money:%s\033[0m' %(info_list[0],info_list[-1],info_list[-2])
            self.print_dic(dic)
            choice = raw_input('请输入编号(exit返回到角色页):').strip()
            if choice == '1':
                self.study(info_list)
            elif choice == '2':
                self.find_girl(info_list)
            elif choice == '3':
                self.work(info_list)
            elif choice == '4':
                self.make_friends(info_list)
            elif choice == '5':
                self.make_money(info_list)
            elif choice == 'exit':
                return info_list
            else:
                print('请输入正确的编号~~~~~~~\n')
                time.sleep(1)