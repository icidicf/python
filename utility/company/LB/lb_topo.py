#!/usr/bin/python

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest="ixia",required=True, help="specify cm used in ixia")
parser.add_argument('-t', dest="tb",required=True, help="specify cm used in tb")

args =parser.parse_args()
cm_ixia = args.ixia
cm_tb = args.tb


topo_dict = {}
ixia = open(cm_ixia, 'r')
ixia_input = ixia.readlines()
ixia.close()


ixia_cm_list = [] 
for item in ixia_input :
	print	item 
	ixia_cm_list.append(item.rstrip())
	
#	m = re.match('G04#.+', it)
#	if m is not None:
#		print m.group()
#	print "line %d , content %s" % (i, it ) 



tb = open(cm_tb, 'r')
tb_input = tb.readlines()
tb.close()
for  item in tb_input:
	print item
	md_re = re.match('.*(Wi\d{1}/\d{1}/\d{1}:\d+).*', item)
	if md_re is not None:
		md = md_re.group(1)
		print "hit " + md_re.group()  
		print "md is %s" %(md_re.group(1))

	mac_re = re.search('([0-9a-f]{4}.[0-9a-f]{4}.[0-9a-f]{4})', item)
	if mac_re is not None:
		mac =  mac_re.group(1)
		print "get mac is " + mac
		if mac in ixia_cm_list:
			print "%s is in ixia list---------------------------------------------------------------------" % mac
			if md  in  topo_dict:
				topo_dict[md].append(mac)
			else :
				topo_dict[md] = []
				topo_dict[md].append(mac)
				
	
print "print the topo of CMs"
for md in  topo_dict:
	print "%s  %s " % (md , topo_dict[md])
