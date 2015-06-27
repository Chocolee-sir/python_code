此版本BUG较多，由于有现成的模块，没有必要死磕，写的时候只支持简单实现功能。
------------------------------------------
使用方法:
1.python admin.py
创建用户组及主机，默认创建的主机没有属组，默认为None,可用此程序给其赋予某个组可执行权限。
2.python UserMain.py
用户组登录，就可以对相应的主机进行操作。
------------------------------------------
功能支持：
多进程批量分发
多进程批量执行命令
------------------------------------------
数据库表：
CREATE TABLE `host` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `hostinfo` varchar(50) NOT NULL COMMENT '主机信息，以逗号分隔，分别为IP地址、端口、登录用户、登录密码',
  `groupname` varchar(20) NOT NULL DEFAULT 'None' COMMENT '属于哪个组，默认没有组',
  PRIMARY KEY (`id`),
  KEY `groupname_index` (`groupname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='主机信息表 ';

CREATE TABLE `user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `username` varchar(32) NOT NULL COMMENT '用户名',
  `passwd` char(32) NOT NULL COMMENT '密码',
  `groupname` varchar(32) NOT NULL COMMENT '组名',
  `super` tinyint(4) NOT NULL DEFAULT '1' COMMENT '是否为超级用户，超级用户为0，普通用户为1',
  `flag` tinyint(4) NOT NULL DEFAULT '0' COMMENT '用户状态，0为可用，1为锁定',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_username` (`username`),
  UNIQUE KEY `unq_groupname` (`groupname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户表 ';

创建的程序用户需对此两表有select,update,delete,insert操作。


