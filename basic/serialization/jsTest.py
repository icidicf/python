#!/usr/bin/python

import json

r1 = json.dumps(['foo',{'bar':('baz',None,1.0,2)}])

print r1

print json.dumps("\"foo\bar")

res = json.loads(r1)

print "revert is " 
print res
