#!/usr/bin/python

for i in range(0,1):
	for j in range(10,35):
		print "interface wideband-Cable 1/0/%d:%d\n" % (i, j), 
		print "no cable ds-resiliency"
		print "exit"
