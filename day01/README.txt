使用方法：
python user_mysql.py
注意:
需要安装MySQLdb模块
Ubuntu：sudo apt-get install python-mysqldb
CentOS：yum install MySQL-python

==================================================================
mysql数据库操作
==================================================================
#创建数据库及用户
mysql> create database chocolee character set utf8; 
mysql> grant execute,select,update,insert,delete on chocolee.* to 'chocolee'@'%' identified by '123456';


#创建表
用户表
CREATE TABLE IF NOT EXISTS user(
id  INT UNSIGNED  AUTO_INCREMENT PRIMARY KEY NOT NULL,
name VARCHAR(20) NOT NULL,
password VARCHAR(50) NOT NULL ,
errorcount TINYINT UNSIGNED NOT NULL DEFAULT 0,
INDEX name_index(name)
)ENGINE = InnoDB DEFAULT CHARSET=utf8;
临时表
CREATE TABLE IF NOT EXISTS locktmp(
name VARCHAR(20)  NOT NULL,
time TIMESTAMP NOT NULL,
INDEX name_index(name)
)ENGINE = InnoDB DEFAULT CHARSET=utf8;


#插入数据
mysql> insert into user(name,password) values('Thunder',md5('111111'));
mysql> insert into user(name,password) values('Sainter',md5('222222'));
mysql> insert into user(name,password) values('Chocolee',md5('333333'));
mysql> insert into user(name,password) values('Kenney',md5('444444'));  
mysql> select * from user;
+----+----------+----------------------------------+------------+
| id | name     | password                         | errorcount |
+----+----------+----------------------------------+------------+
|  1 | Thunder  | 96e79218965eb72c92a549dd5a330112 |          0 |
|  2 | Sainter  | e3ceb5881a0a1fdaad01296d7554868d |          0 |
|  3 | Chocolee | 1a100d2c0dab19c4430e7d73762b3423 |          0 |
|  4 | Kenney   | 73882ab1fa529d7273da0db6b49cc4f3 |          0 |
+----+----------+----------------------------------+------------+


#导入存储过程
存储过程解锁 2分钟解锁
DELIMITER //
CREATE DEFINER=`chocolee`@`%` PROCEDURE `unlock_user`(IN lock_name varchar(20))
begin
    declare sec int;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET sec = 1;
    select (UNIX_TIMESTAMP(now()) - UNIX_TIMESTAMP(time)) into sec from chocolee.locktmp where name= lock_name;
    if  (sec is not null) and sec >120 then
       update chocolee.user set errorcount=0 where name = lock_name;
       delete from chocolee.locktmp where name = lock_name;
    end if;
end
//
DELIMITER ;
