#!/usr/bin/python

import os

print "current dir is " + os.getcwd()

print "change dir to /ws/shell"
os.chdir('/ws/shell')

print "current dir is " + os.getcwd()
