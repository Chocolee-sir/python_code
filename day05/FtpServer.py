#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'

import SocketServer
import os,sys,time
from UserClassMain import *

class MyServer(SocketServer.BaseRequestHandler):
    def setup(self):
        pass

    def handle(self):
        print self.request, self.client_address, self.server
        data = self.request.recv(1024)
        path = 'e:/ftp_data/%s' %data
        if os.path.exists(path) == False:
            os.makedirs(path)
            rev = '您是新用户，初始化目录完毕...'
            self.request.send(rev)
            time.sleep(1)
        else:
            self.request.send('......')
        while True:
            data = self.request.recv(1024)
            if data == 'ls':
                if os.listdir(path) == []:
                    self.request.send('None')
                else:
                    line = ''
                    for i in os.listdir(path):
                        line = line + '%s\n' %i
                    self.request.send(line.strip())
            else:
                data = data.split('|')
                if data[0] == "put":
                    filename_from_cli,file_size = data[1],int(data[2])
                    file_name = '%s/%s' %(path,filename_from_cli)
                    f = file(file_name,'wb')
                    recv_size = 0
                    flag = True
                    while flag:
                        if recv_size + 1024> file_size :
                            recv_data = self.request.recv(file_size - recv_size)
                            flag = False
                        else:
                            recv_data = self.request.recv(1024)
                            recv_size += 1024
                        f.write(recv_data)
                    f.close()
                    time.sleep(1)
                    self.request.send(md5_file('%s'%file_name))
                    print "put Receving file success!"

                elif data[0] == 'get':
                    file_path = '%s/%s' %(path,data[1])
                    file_size = os.stat(file_path).st_size
                    self.request.send(str(file_size))
                    file_size = int(file_size)
                    send_size = 0
                    f = file(file_path,'rb')
                    flag = True
                    while flag:
                        if send_size + 1024 > file_size:
                            data = f.read(file_size - send_size)
                            flag = False
                        else:
                            data = f.read(1024)
                            send_size += 1024
                        self.request.send(data)
                    f.close()
                    self.request.send(md5_file('%s'%file_path))
                    print "put Sending file success!"

    def finish(self):
        pass

if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(('127.0.0.1', 9999),MyServer)
    server.serve_forever()









