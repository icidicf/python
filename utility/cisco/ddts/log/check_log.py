#!/usr/bin/python

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('-l', dest="log",required=True, help="specify a log need to process")

args =parser.parse_args()
log_name = args.log

print "imput log is " + log_name
f = open(log_name, 'r')
out = f.readlines()
f.close

i = 0
for it in out :
	i = i+1

	m = re.match('G04#.+', it)
	if m is not None:
		print m.group()
#	print "line %d , content %s" % (i, it ) 

