#!/usr/bin/python

''''
In [1]: class DoubleRep(object):
   ...:         def __str__(self):
   ...:                         return "Hi, I'm a __str__"
   ...:         def __repr__(self):
   ...:                         return "Hi, I'm a __repr__"
   ...:     

In [2]: dr = DoubleRep()

In [3]: print dr
Hi, I'm a __str__

In [4]: dr
Out[4]: Hi, I'm a __repr__
'''


class DoubleRep(object):
	def __str__(self):
		return "Hi, I'm a __str__"
	def __repr__(self):
		return "Hi, I'm a __repr__"


dr = DoubleRep()

print "test print , this is unoffical %s " % dr
print dr
print "test repr, this is offical %r " % dr

