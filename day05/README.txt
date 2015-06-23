ftp单机版简单支持功能：
用户注册
用户登录
文件上传
文件下载
打印服务端用户目录列表中的文件
不支持断点续传功能
=====================================================================================================
使用方法（ftp单机版）:
①所有的程序放在同一级目录下

②创建用户数据库，创建账号密码，可以让程序连接到数据库。
参考：
-----------------------------------------------------------------------------------
创建库
create database chocolee;
-----------------------------------------------------------------------------------
创建表
CREATE TABLE `user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `username` varchar(32) NOT NULL COMMENT 'username',
  `passwd` char(32) NOT NULL COMMENT 'password ',
  `super` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'super status 0 is not super user 1 is super user',
  `flag` tinyint(4) NOT NULL DEFAULT '0' COMMENT 'user status 0 is active, 1 is locked',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COMMENT='user table ';
-----------------------------------------------------------------------------------
创建用户
grant all on chocolee.* to 'chocolee'@'%' identified by '123456';
-----------------------------------------------------------------------------------
UserClassMain.py程序配置数据库连接信息。
-----------------------------------------------------------------------------------

③设置ftp服务端根目录
在FtpServer.py中path变量修改主目录路径，如path = 'e:/ftp_data/%s' %data中，e:/ftp_data/为ftp根目录路径，这里存放了所有用户目录。

④启动ftp服务端
python FtpServer.py

⑥启动ftp客户端
python FtpMain.py

=====================================================================================================

程序文件介绍
tree_search.py  找alex作业题程序
admin.py 可为用户解锁
DBClassMain.py 连接数据库的类
UserClassMain.py  对用户操作的类
FtpServer.py ftp服务端
FtpMain.py ftp客户端及前端菜单等逻辑