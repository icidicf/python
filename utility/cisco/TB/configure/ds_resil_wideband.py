#!/usr/bin/python

for i in range(0,1):
	for j in range(20,47):
		print "interface wideband-Cable 1/0/%d:%d\n" % (i, j), 
		print "cable ds-resiliency"
		print "exit"
