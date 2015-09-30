#!/usr/bin/env python

import sys

def usage():
    print 'At least 1 arguments (incl. cmd name).'
    print 'usage: args.py arg1 ' 
    sys.exit(1)

argc = len(sys.argv)
if argc < 2:
    usage()

filename = sys.argv[1];
print "file name is " + filename

with open(filename, 'r') as f:
    for line in f:
        print line,


