#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
from SqliteClass import *
t = SqliteClass('test.db')

#用户表
user_table = '''
create table if not exists user_info(
id integer primary key autoincrement,
user varchar(8) not null,
groupid smallint(4) not null default 0,
sshuser varchar(8) not null);
'''
user_index = 'create index if not exists groupid on user_info(groupid,user)'

#用户组表
group_table = '''
create table if not exists group_info(
id integer primary key autoincrement,
groupname varchar(8) not null,
groupid smallint(4) not null default 0,
serverip varchar(20) not null);
'''
group_index = 'create unique index if not exists groupid on group_info(groupid,groupname,serverip)'

#日志审计表
auditlog_table='''
create table if not exists audit_log(
id integer primary key autoincrement,
ophost varchar(20) not null,
optime datetime not null,
opuser varchar(8) not null,
opcmd varchar(20) not null);
'''
auditlog_index = 'create index if not exists groupid on audit_log(ophost)'

#堡垒机登陆用户信息表
fortress_table ='''
create table if not exists fortress_user(
id integer primary key autoincrement,
user varchar(8) not null,
passwd varchar(50) not null);
'''

#主机信息表
host_table ='''
create table if not exists host_info(
host varchar(20)  not null,
port smallint(5) not null DEFAULT 22,
user varchar(8) not null DEFAULT 'root',
passwd varchar(50) not null,
flag smallint(1) not null DEFAULT 0);
'''
host_index = 'create unique index if not exists host on host_info(host,user)'


if __name__ == '__main__':
    t.query('drop table if EXISTS user_info')
    t.query('drop table if EXISTS group_info')
    t.query('drop table if EXISTS audit_log')
    t.query('drop table if EXISTS fortress_user')
    t.query('drop table if EXISTS host_info')
    t.query(user_table)
    t.query(user_index)
    t.query(group_table)
    t.query(group_index)
    t.query(auditlog_table)
    t.query(auditlog_index)
    t.query(fortress_table)
    t.query(host_table)
    t.query(host_index)
    t.commit()
    t.close()