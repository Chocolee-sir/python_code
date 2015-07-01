#!/usr/bin/env python
# encoding:utf-8
__author__ = 'Chocolee'
import socket
import sys
import traceback
import paramiko
import interactive

class DemoSimple(object):

    def __init__(self,hostname,username,port,pw):
        self.hostname = hostname
        self.username = username
        self.port = port
        self.pw = pw

    def connect(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.hostname, self.port))
        except Exception, e:
            print '*** Connect failed: ' + str(e)
            traceback.print_exc()
            sys.exit(1)

        try:
            t = paramiko.Transport(sock)
            try:
                t.start_client()
            except paramiko.SSHException:
                print '*** SSH negotiation failed.'
                sys.exit(1)

            if not t.is_authenticated():
                t.auth_password(self.username, self.pw)
            if not t.is_authenticated():
                print '*** Authentication failed. :('
                t.close()
                sys.exit(1)

            chan = t.open_session()
            chan.get_pty()
            chan.invoke_shell()
            print '*** Here we go!'
            print
            interactive.interactive_shell(chan,self.username,self.hostname)
            chan.close()
            t.close()

        except Exception, e:
            print '*** Caught exception: ' + str(e.__class__) + ': ' + str(e)
            traceback.print_exc()
            try:
                t.close()
            except:
                pass
            sys.exit(1)


if __name__ == '__main__':
    u = DemoSimple('10.10.206.194','root',22,'e_OP@194#!')
    u.connect()