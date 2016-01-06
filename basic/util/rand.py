#!/usr/bin/python
import random


print "rand is %d" % random.randint(0,4) 

li=[11,22,33,44]

rec = {11:0, 22:0,33:0,44:0}
for i in range(0,1000):
    pos = random.randint(0,len(li)-1)
    while li[pos] == 33:
        pos = random.randint(0,len(li)-1)

    va = li[pos]
    rec[va] +=1

    print "len is  rand next is %d" % va


for key in rec :
    print "key is %d, val is %d" %(key, rec[key])


def test_return():
    return "lyp", "wq"



a,b = test_return()

print "a is %s , b is %s" % (a,b)


