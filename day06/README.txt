�˰汾BUG�϶࣬�������ֳɵ�ģ�飬û�б�Ҫ���ģ�д��ʱ��ֻ֧�ּ�ʵ�ֹ��ܡ�
------------------------------------------
ʹ�÷���:
1.python admin.py
�����û��鼰������Ĭ�ϴ���������û�����飬Ĭ��ΪNone,���ô˳�����丳��ĳ�����ִ��Ȩ�ޡ�
2.python UserMain.py
�û����¼���Ϳ��Զ���Ӧ���������в�����
------------------------------------------
����֧�֣�
����������ַ�
���������ִ������
------------------------------------------
���ݿ��
CREATE TABLE `host` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '����id',
  `hostinfo` varchar(50) NOT NULL COMMENT '������Ϣ���Զ��ŷָ����ֱ�ΪIP��ַ���˿ڡ���¼�û�����¼����',
  `groupname` varchar(20) NOT NULL DEFAULT 'None' COMMENT '�����ĸ��飬Ĭ��û����',
  PRIMARY KEY (`id`),
  KEY `groupname_index` (`groupname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='������Ϣ�� ';

CREATE TABLE `user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '����id',
  `username` varchar(32) NOT NULL COMMENT '�û���',
  `passwd` char(32) NOT NULL COMMENT '����',
  `groupname` varchar(32) NOT NULL COMMENT '����',
  `super` tinyint(4) NOT NULL DEFAULT '1' COMMENT '�Ƿ�Ϊ�����û��������û�Ϊ0����ͨ�û�Ϊ1',
  `flag` tinyint(4) NOT NULL DEFAULT '0' COMMENT '�û�״̬��0Ϊ���ã�1Ϊ����',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_username` (`username`),
  UNIQUE KEY `unq_groupname` (`groupname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='�û��� ';

�����ĳ����û���Դ�������select,update,delete,insert������


