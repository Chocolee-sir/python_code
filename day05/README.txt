ftp�������֧�ֹ��ܣ�
�û�ע��
�û���¼
�ļ��ϴ�
�ļ�����
��ӡ������û�Ŀ¼�б��е��ļ�
��֧�ֶϵ���������
=====================================================================================================
ʹ�÷�����ftp�����棩:
�����еĳ������ͬһ��Ŀ¼��

�ڴ����û����ݿ⣬�����˺����룬�����ó������ӵ����ݿ⡣
�ο���
-----------------------------------------------------------------------------------
������
create database chocolee;
-----------------------------------------------------------------------------------
������
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
�����û�
grant all on chocolee.* to 'chocolee'@'%' identified by '123456';
-----------------------------------------------------------------------------------
UserClassMain.py�����������ݿ�������Ϣ��
-----------------------------------------------------------------------------------

������ftp����˸�Ŀ¼
��FtpServer.py��path�����޸���Ŀ¼·������path = 'e:/ftp_data/%s' %data�У�e:/ftp_data/Ϊftp��Ŀ¼·�����������������û�Ŀ¼��

������ftp�����
python FtpServer.py

������ftp�ͻ���
python FtpMain.py

=====================================================================================================

�����ļ�����
tree_search.py  ��alex��ҵ�����
admin.py ��Ϊ�û�����
DBClassMain.py �������ݿ����
UserClassMain.py  ���û���������
FtpServer.py ftp�����
FtpMain.py ftp�ͻ��˼�ǰ�˲˵����߼�