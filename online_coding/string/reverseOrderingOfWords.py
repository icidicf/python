#!/usr/bin/python
import sys
import re

if (len(sys.argv) < 2):
	print "please enter input test string";
	sys.exit(0);

inputStr=sys.argv[1];

#version 1
#tempStr=inputStr.split(" ");
tempStr=re.split('\s+',inputStr);
tempResult=[];
outStr="";
for i in tempStr:
	part=i[::-1];
	tempResult.append(part);
	outStr=" ".join(tempResult);

print "just reverse the word , not change the word order  " + outStr;



#version 3
print "not reverse the word , change the order of the words " + ' '.join(reversed(inputStr.split()))


