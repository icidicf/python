#!/usr/bin/python

def happyNumber(n):
	past= set();
	while(n != 1): 
#		print "n is " + str(n);
		n = sum(int(i)**2 for i in str(n));
		if n in past:
			return False;
		past.add(n);
#	print "n " + str(n) + "is a happy number"
	return True
	

for x in xrange(1000):
 if happyNumber(x) == True:
	print str(x) + " is happy number "


