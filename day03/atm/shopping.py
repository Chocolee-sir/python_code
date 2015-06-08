#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import credit_card_main as cardmain
import pickle
import sys,time
import readline
product_dic = {'1':'iphone 5288','2':'ipad 3688','3':'nike 1299','4':'coffee 28','5':'chocolee 8','6':'结算','7':'退出'}
shopping_list = []
dic_list = {}
money = 0


print('##################\n#    欢迎光临    #\n##################')
while True:
    cardmain.dic(product_dic,'product list')
    num = raw_input('请选择您要购买的商品编号：').strip()
    if num == "7":
        print('欢迎下次光临。')
        sys.exit(0)
    if num == "6":
        if len(shopping_list):
            print('进入结算系统.....\n')
            time.sleep(0.5)
            break
        else:
            print('对不起，购物篮空空如也,请选择商品~~\n')
            continue
    if num not in product_dic.keys()  or num == "":
        print('对不起，输入不正确，请输入商品列表中的编号。\n')
        time.sleep(1)
        continue
    tmp_list = product_dic[num].split()
    shopping_list.append(tmp_list[0])
    money += int(tmp_list[1])
    print('已将%s加入购物车\n'%tmp_list[0])

print('***您已选择如下商品***')
for i in  sorted(set(shopping_list) ,key = lambda x:x[0] ,reverse=False):
    print('%s x%s'%(i,shopping_list.count(i)))
print('总计消费:%s\n**********************'%money)

while True:
    info = raw_input('是否支付（yes/no）：')
    if info == 'yes' or info == 'YES':
        print('接入到银行支付系统......')
        time.sleep(0.5)
        login_return = cardmain.auth_user()
        if login_return:
            print('正在验证......')
            time.sleep(0.5)
            number = cardmain.find_card()
            dic_list = cardmain.import_card(dic_list)
            for i in dic_list.items():
                if number == i[0]:
                    info_list = dic_list[number]
                    available = float(info_list[-1])
                    if available < money:
                        print('%s此卡余额不足，没钱就别装逼,换张无限卡来装逼吧~~~~~'%number)
                        break
                    else:
                        print('支付成功，%s卡消费金额:%s元'%(number,money))
                        quota = available - money
                        info_list[-1] = quota
                        dic_list[i[0]] = info_list
                        cardmain.dump_card(dic_list)
                        cardmain.load_log(cardmain.action_time(),number,'消费',money)
                        print(' 感谢您的购物~~~~欢迎您下次光临。')
                        sys.exit(0)

    elif info == 'NO' or info == 'no':
        print('欢迎下次光临。')
        sys.exit(0)
    else:
        print('请输入正确，yes或者no')
        continue








