import socket
import os,sys,datetime,time
from SqliteClass import *


s = SqliteClass('test.db')

try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan,django_loginuser,username,hostname):
    print """\033[;34m------ Welcome %s Login %s ------\033[0m""" % (django_loginuser,hostname)
    if has_termios:
        posix_shell(chan,django_loginuser,username,hostname)
    else:
        windows_shell(chan)


def posix_shell(chan,django_loginuser,username,hostname):
    import select
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)

        record = []
        ''' record operation log '''
        #day_time = time.strftime('%Y_%m_%d')
        #f = open('audit_%s_%s.log' % (day_time,django_loginuser),'a')
        while True:
	    date =time.strftime('%Y-%m-%d %H:%M:%S')
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = chan.recv(1024)
                    if len(x) == 0:
                        print '\r\n*** EOF\r\n',
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                record.append(x)
                chan.send(x)

            if x == '\r':
                cmd = ''.join(record).split('\r')[-2]
                if cmd == '':
                    continue
                cmd = cmd.replace('\t','|tab|')
                sql = "insert into audit_log(ophost,optime,loginuser,opuser,opcmd) VALUES ('%s','%s','%s','%s','%s')" \
                      % (hostname,date,django_loginuser,username,cmd)
                s.query(sql)
                s.commit()
                #log = "%s | %s | %s | %s\n" % (hostname,date,django_loginuser,cmd)
                #f.write(log)
                #f.flush()
       # f.close()
        s.close()


    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

    
# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
        
    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()
        
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
        
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass

