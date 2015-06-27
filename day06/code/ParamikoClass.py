#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import paramiko
import os

class ParamikoClass(object):

    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __init__(self,host,port,user,password):
        self.host = host
        self.port = port
        self.user = user
        self.password =password

#执行命令函数
    def cmd_run(self,cmd):
        self.s.connect(self.host,self.port,self.user,self.password,timeout=1)
        stdin,stdout,stderr = self.s.exec_command(cmd)
        cmd_result = stdout.read(),stderr.read()
        print('++++++%s++++++'%self.host)
        for line in cmd_result:
            print line,
        print('\n')
        self.s.close()

#分发文件函数
    def put_file(self,file_path,remote_path):
        file_name = os.path.basename(file_path)
        t = paramiko.Transport((self.host,self.port))
        t.connect(username=self.user,password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(file_path,'%s/%s' %(remote_path,file_name))
        t.close()
        print('++++++%s++++++'%self.host)
        print('分发 %s 到%s 的 %s 目录下。'%(file_name,self.host,remote_path))
        print('\n')

    #未测试
    def get_file(self,remotepath,file_name,localpath):
        t = paramiko.Transport((self.host,self.port))
        t.connect(username=self.user,password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get('%s/%s'%(remotepath,file_name),'%s/%s'%(localpath,file_name))
        t.close()