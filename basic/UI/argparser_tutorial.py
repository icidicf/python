#!/usr/bin/python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int , help="display a square of a give number")
parser.add_argument("--verbosity", help="increase output verbosity",
				action="store_true")
args = parser.parse_args()
answer = args.square**2

if args.verbosity:
	print "the square of {} eqyals {}".format(args.square, answer)
else :
	print answer
