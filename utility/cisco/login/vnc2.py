#!/usr/bin/python

import paramiko
from . import interactive

hostname='sh-cable-vnc-2'
port = 22
username = 'jelou'
password = 'lab123'

if __name__ == "__main__":
	paramiko.util.log_to_file('lyp_vnc2.log')
	s = paramiko.SSHClient()
	s.load_system_host_keys()
	s.connect(hostname, port, username, password)
#	s.invoke_shell()
	interactive.interactive_shell(s)
'''	stdin, stdout, stderr = s.exec_command('ls')
	print stdout.read()
	print stderr.read()
	s.close()

'''
