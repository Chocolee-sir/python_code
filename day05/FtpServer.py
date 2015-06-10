#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'

import SocketServer
import os,sys,time

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
                    #os.listdir(path) 从这开始
                    #self.request.send()




    def finish(self):
        pass

if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(('127.0.0.1', 9999),MyServer)
    server.serve_forever()









