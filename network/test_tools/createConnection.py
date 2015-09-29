#!/usr/bin/python

from socket import socket, AF_INET,SOCK_STREAM
import sys


if len(sys.argv) < 2:
    print "please give connection you want to set"
    sys.exit(0)



srvIP = '192.168.102.129'
srvPort=12345
connNum = sys.argv[1]
j=0
for i in range(int(connNum)):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((srvIP,srvPort))
    print "connection " + str(i) + "is set up for " + str(srvIP) + " " + str(srvPort)


while 1:
    j += 1


