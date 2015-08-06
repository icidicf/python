#!/usr/bin/python
import sys
import os.path

if (len(sys.argv) < 2 ):
	print "please specify the file name"
	sys.exit(0)

filename=sys.argv[1]+".cpp"
print "the file name is " + filename;

if os.path.isfile(filename):
	print filename+" the file is exist already, please choose the file name " 
	sys.exit(0)

with open(filename,'wt') as f:
	f.write("#include <iostream>"+os.linesep)
	f.write("#include <string>"+os.linesep)
	f.write(os.linesep*2)
	f.write("int main(void)"+os.linesep)
	f.write("{"+os.linesep);
	f.write(os.linesep*2)
	f.write("}"+os.linesep);

	

os.chmod(filename,764);




