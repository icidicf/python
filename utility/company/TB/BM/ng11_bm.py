#!/usr/bin/python

import getpass 
import sys
import telnetlib
import re
import signal
import time
import string
import logging
def ctrl_c_handler(signo, frame):
	print "invoke ctrl c go to close telnet ", signo
	tn.write("exit\n")
	tn.close()
	sys.exit(0)


def is_contain_str(mac_addr, str):
	tn.write('scm\n')
	scm_output=tn.read_until('#')

	re_line=mac_addr+'.*'
	line = re.search(re_line, scm_output)

	if line is None:
		return False

	match_line =  line.group()
	re_str = re.search(str, match_line)
	if re_str is not None:
		return True
	else:
		return False

def print_match_line(mac_addr):
	tn.write('scm\n')
	scm_output=tn.read_until('#')

	re_line=mac_addr+'.*'
	line = re.search(re_line, scm_output)

	if line is not None:
		print line.group()
		logger.info(line.group())

def get_w_online_cm_list():
	tn.write('scm w c\n')
	scm_output=tn.read_until("#")

	re_mac_addr='[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]'
	cm_list=re.findall(re_mac_addr,scm_output)
	print cm_list
	
	
def wait_cm_online(mac_addr):
	if is_contain_str(mac_addr, "w-online") == True:
		print "%s is already w-online" % mac_addr
		return 

	while is_contain_str(mac_addr, 'w-online') == False:
		print "waiting %s w-online" % mac_addr
		time.sleep(10)

def clear_cable_modem(mac_addr):
	cmd = "clear cable modem " + mac_addr + " delete \n " 
	print cmd
	tn.write(cmd)
	tn.read_until('#')
	wait_cm_online(mac_addr)

def get_cm_status_transac_id(mac_addr, key_word):
	cmd = "show cable modem " + mac_addr + " cm-status \n"
	tn.write(cmd)
	cm_status = tn.read_until('#')
	re_pat=key_word+'.*'
	re_cm_status = re.search(re_pat, cm_status)
	if re_cm_status is not None:
		tar_line = re_cm_status.group()
		print tar_line
		items= re.split("\s+", tar_line)
		tran_id=int(items[3])
		return tran_id
	else:
		return 0

def wait_cm_to_bm(mac_addr):
	wait_cm_online(mac_addr)
	while is_contain_str(mac_addr, 'bm') == False:
		print "waiting %s enter BM" % mac_addr 
		time.sleep(10)

def wait_cm_to_normal(mac_addr):
	wait_cm_online(mac_addr)
	while is_contain_str(mac_addr, 'bm') == True:
		print "waiting %s return to  normal" % mac_addr 
		time.sleep(10)



logger = logging.getLogger("bm_log")
hdlr = logging.FileHandler('./ng11_bm_log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

host = "20.5.31.21"
user = "jelou"
password = "lab123"

tn =telnetlib.Telnet(host)
tn.read_until('#')
tn.write('term len 0\n')
tn.read_until('#')

signal.signal(signal.SIGINT, ctrl_c_handler)


get_cm_list
#clear_cable_modem(mac_addr)
'''
enter_transac_id = get_cm_status_transac_id(mac_addr, r"Battery") + 1 
leave_transac_id = get_cm_status_transac_id(mac_addr, r"A/C") + 1 
print "bm tran id %d , ac tran id %d "%  (enter_transac_id , leave_transac_id)
	print_match_line(mac_addr)
	if is_contain_str(mac_addr,'bm') == False:
		cmd = "test cable cm-status %s %d 9 010302010c \n "  % ( mac_addr, enter_transac_id)
		print cmd
		tn.write(cmd);
		result = tn.read_until('#')
		logger.info(result)
		wait_cm_to_bm(mac_addr)
		enter_transac_id += 1
	else : 
		cmd ="test cable cm-status %s %d 10 010302010c \n" % ( mac_addr ,leave_transac_id)
		print cmd 
		tn.write(cmd);
		result = tn.read_until('#')
		logger.info(result)
		wait_cm_to_normal(mac_addr)
		leave_transac_id += 1

'''
