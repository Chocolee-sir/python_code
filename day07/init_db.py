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
group_index = 'create index if not exists groupid on group_info(groupid,groupname)'

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




