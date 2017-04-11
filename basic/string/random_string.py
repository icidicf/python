#!/usr/bin/env python
import sys
import string
import random 

def id_generator(size):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _
            in range(size))


if len(sys.argv) <2 :
    print "specify len"
    sys.exit(-1)

rand_str = id_generator(int(sys.argv[1]))
print rand_str
