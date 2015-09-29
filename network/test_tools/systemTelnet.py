#!/usr/bin/python

from socket import socket, AF_INET,SOCK_STREAM
import sys
import os


if len(sys.argv) < 2:
    print "please give connection you want to set"
    sys.exit(0)



srvIP = '192.168.102.129'
srvPort='12345'
arg = [srvIP, srvPort]
connNum = sys.argv[1]
j=0
for i in range(int(connNum)):
    ret = os.fork()
    if ret == 0:
        print "telnet " + str(i) + " is set up for " + str(srvIP) + " " + str(srvPort)
    else:
        #os.execl('/usr/bin/telnet','telnet',"192.168.102.129", '12345')
        os.execl('/usr/bin/telnet','telnet',"192.168.102.129", '12345')


while 1:
    j += 1


