#堡垒机程序（简单实现BUG很多）
-------------------------------------------
文件列表：
day7
├── admin.py    #管理程序，支持创建堡垒机用户，添加主机，创建主机组，为堡垒机分配主机组，查看审计日志,日志有大量BUG！！！
├── DemoClass.py    #堡垒机功能程序之一
├── init_db.py    #初始化sqlite数据库数据
├── interactive.py   #堡垒机功能程序之一
├── LogicSQLClass.py  #SQL逻辑类
├── main.py    #堡垒机菜单登录主程序
├── SqliteClass.py  #sqlite连接类
└── test.db    #sqlite数据库文件
-------------------------------------------
使用方法:
1.初始化数据库表
python init_db.py 

2.创建堡垒机用户，主机，主机组，为堡垒机用户分配主机组
test@ubuntu:~/liyiliang/day7$ python admin.py 
+++++++++++++++++++++++
1 创建堡垒机用户
2 添加主机
3 主机组操作
4 用户添加主机组操作
5 查询审计日志
6 退出
+++++++++++++++++++++++
 按顺序操作：
①创建堡垒机用户
②添加主机
③创建主机组，将主机分配给主机组
④为堡垒机用户添加主机组

3.运行主程序，打开堡垒机菜单，登陆
python main.py 
test@ubuntu:~/liyiliang/day7$ python main.py 
请输入用户名(exit退出):chocolee
请输入密码(exit退出):123456
++++chocolee 欢迎登陆堡垒机系统++++

您可操作以下主机组:
redhat
请选择主机组(exit退出):redhat
redhat组有以下ip列表:
10.10.206.193
请输入远程连接的地址(exit返回):10.10.206.193
*** Here we go!

------ Welcome chocolee Login 10.10.206.193 ------
Last login: Thu Jul  9 17:23:26 2015 from 10.10.140.187
[root@ln-master ~]# 
[root@ln-master ~]# ls -l
总计 8408
-rw-r--r-- 1 root    root        124 2014-08-08 2014.txt
....
[root@ln-master ~]# ifconfig
eth0      Link encap:Ethernet  HWaddr 00:50:56:97:39:7C  
          inet addr:10.10.206.193  Bcast:10.10.206.255  Mask:255.255.255.0
...

-------------------------------------------
查看审计日志
test@ubuntu:~/liyiliang/day7$ python admin.py 
+++++++++++++++++++++++
1 创建堡垒机用户
2 添加主机
3 主机组操作
4 用户添加主机组操作
5 查询审计日志
6 退出
+++++++++++++++++++++++
请选择:5
欢迎登录日志审计系统~~~~
请输入1查询日志(exit返回):1
ip地址 | 操作时间 | 登录堡垒机用户 | 登录远程机用户 | 操作命令
10.10.206.193 | 2015-07-10 23:25:37 | chocolee | root | ll
10.10.206.193 | 2015-07-10 23:25:40 | chocolee | root | ls -l
10.10.206.193 | 2015-07-10 23:26:15 | chocolee | root | ifconfig
10.10.206.193 | 2015-07-10 23:26:33 | chocolee | root | exit
