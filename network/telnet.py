#!/usr/bin/python

import getpass 
import sys
import telnetlib

host = "sh-cable-lotus"
user = "jelou"
password = "lab123"

tn =telnetlib.Telnet(host)

tn.read_until("login:")
tn.write(user + "\n")

tn.read_until("Password:")
tn.write(password + "\n")

tn.write("ls\n");
tn.write("echo \"welcome Yangping\"\n");

##### interactive mode ############
tn.interact();


#########do job and exit################
#tn.write("show history\n")
#print tn.read_all()
#tn.write("exit\n");



