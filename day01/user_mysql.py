#!/usr/bin/env python
#encoding:utf-8
import MySQLdb
import warnings
import readline,time
import hashlib
import getpass

warnings.filterwarnings("ignore")

MysqlHost = '10.10.206.193'
MysqlUser = 'chocolee'
MysqlPass = '123456'
MysqlPort = 3307
LoginSucess = False
LoginLock = False
flag = 0
n = ''
psw = ''

#将输入的密码转换成MD5函数
def check_md5(passwd):
    global psw
    m = hashlib.md5()
    m.update(passwd)
    psw = m.hexdigest()


try:
    #连接数据库
    conn = MySQLdb.connect(host=MysqlHost,user=MysqlUser,passwd=MysqlPass,port=MysqlPort,charset='utf8')
    cur = conn.cursor()
    while True:
        Name = raw_input('Username:')
        Name = Name.strip()
        if Name == "":         #判断用户名是否为空
            print '\033[1;33;40mWarning:The username cannot be empty,please input again.\033[0m'
            continue
        else:
            unlock_cmd="call chocolee.unlock_user('%s')" %Name
            check_user_cmd="select 1 from chocolee.user where name = '%s' limit 1" %Name
            check_pass_cmd="select password from chocolee.user where name = '%s'"  %Name
            check_err_count="select errorcount from chocolee.user where name = '%s'" %Name
            add_err_count="update chocolee.user set errorcount = errorcount + 1 where name = '%s'" %Name  
            insert_lockuser="insert into chocolee.locktmp(name) values('%s')"  %Name
        
	    cur.execute(check_user_cmd)       #检查用户是否在数据库中存在
            for n in cur.fetchall():
                n = int(n[0]) 
            if n == "":
                print "\033[1;33;40mWarning:The user '%s' does not exist,please input again.\033[0m"  %Name
                continue
            else:
                cur.execute(unlock_cmd)     #存在则执行存储过程，检查此用户是否被锁，如果被锁且锁定时间超过2分钟则解锁
	        time.sleep(0.3)	
	        cur.execute(check_err_count)       #在数据库中检查登陆错误次数，如果大于等于3，则为锁定状态，直接退出
                for n in cur.fetchall():
                    n = int(n[0])
                if n >= 3:
                    print "\033[1;31;40mError:The user '%s' is locked,try again after two minutes.\033[0m"  %Name
                    break 
		
	for i in range(3):
	    Pass = getpass.getpass('Password:')
	    check_md5(Pass)
            cur.execute(check_pass_cmd)     #从数据库中检查密码
            for n in cur.fetchall():
                n = str(n[0])
            if n == psw:
                print '\033[1;32;40mCongratulations!!!!! Login Successful!!!!!\033[0m'
                LoginSucess = True
                break
			else:
                print '\033[1;34;40mInfo:Sorry,Authentication failed,please input again.\033[0m' 
                cur.execute(add_err_count)      #密码输入不正确，在数据库errorcount字段自增1
                flag = flag + 1
                if flag == 3:
                    print "\033[1;31;40mError:The user '%s' is locked,try again after two minutes.\033[0m"  %Name
                    cur.execute(insert_lockuser)      #输入三次密码错误，将用户记录插入到锁定临时表               
                    LoginLock = True
                    break
        if LoginSucess:
            break
        if LoginLock:
            break 
			
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "MySQLdb Error",e
