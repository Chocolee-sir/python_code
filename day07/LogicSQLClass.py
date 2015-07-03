#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
from SqliteClass import SqliteClass
import hashlib

class LSqlClass(object):

    s = SqliteClass('test.db')

    def changeMd5(self, password):
        m = hashlib.md5()
        m.update(password)
        return m.hexdigest()

    def addFloginUser(self,user,passwd):
        sql = "select 1 from fortress_user where user = '%s' limit 1" %user
        flag = self.s.queryRow(sql)
        if  flag != None:
            return False
        else:
            user_dic = {'user':user,'passwd':self.changeMd5(passwd)}
            self.s.insert('fortress_user',user_dic)
            self.s.commit()
            return True

    def addHost(self,host,port,user,passwd):
        sql = "insert into host_info(host,port,user,passwd) values('%s','%s','%s','%s')" \
              %(host,port,user,passwd)
        self.s.query(sql)
        self.s.commit()

    def findHost(self):
        sql = "select host from host_info where flag = 0"
        return self.s.queryAll(sql)

    def addGroup(self,groupname,groupid,host):
        sql = "insert into group_info(groupname,groupid,serverip) values('%s','%s','%s')"\
        %(groupname,groupid,host)
        sql2 = "update host_info set flag = 1 where host = '%s'" %host
        self.s.query(sql)
        self.s.query(sql2)
        self.s.commit()

    def findGroup(self):
        sql = "select groupname,GROUP_CONCAT(serverip) from group_info group by groupname"
        return self.s.queryAll(sql)

    def findGroupName(self):
        sql = "select groupname from group_info group by groupname"
        return self.s.queryAll(sql)

    def findGid(self):
        sql = "select max(groupid) from group_info"
        return self.s.queryRow(sql)[0]

    def findGnameGid(self,gname):
        sql = "select groupid from group_info where groupname ='%s' group by groupid" %gname
        return self.s.queryRow(sql)[0]

    def findFuser(self):
        sql = "select user from fortress_user"
        return self.s.queryAll(sql)

    def addUserInfo(self,user,groupid,sshuser):
        sql = "insert into user_info(user,groupid,sshuser) values('%s','%s','%s')" %(user,groupid,sshuser)
        self.s.query(sql)
        self.s.commit()

    def UserGroupInfo(self,username):
        sql = "select g.groupname from user_info u join group_info g \
        using (groupid) where u.user='%s' group by g.groupname;" %username
        return  self.s.queryAll(sql)

    def findFuserName(self,user):
        sql = "select 1 from fortress_user where user = '%s' limit 1 " %user
        return self.s.queryRow(sql)

    def findFuserPass(self,user):
        sql = "select passwd from fortress_user where user= '%s' " %user
        return self.s.queryRow(sql)[0]

    def findGroupHosts(self,groupname):
        sql = "select serverip from group_info where groupname = '%s'" %groupname
        return self.s.queryAll(sql)

    def findHostInfo(self,host):
        sql = "select host,port,user,passwd from host_info  where host = '%s'" %host
        return self.s.queryAll(sql)


