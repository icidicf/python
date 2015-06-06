#!/usr/bin/python
import time

def func1():
	print "func1 invoked "
	sum = 0
	for i in range(1000000):
		sum += i

def func2():
	print "func2 invoked "
	time.sleep(10)

func1()
func2()
