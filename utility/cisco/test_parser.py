#!/usr/bin/python
import argparse

def jelou_copy_image(args):
	ddts=args.ddts
	print "ddts name is " + ddts

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(help="sub command")
	copy_image_parser = subparsers.add_parser("copy_image", 
							help="Copy image from server")
	copy_image_parser.set_defaults(func=jelou_copy_image)
	copy_image_parser.add_argument("-d", "--ddts",dest="ddts", 
							required=True, help="DDTS name")

	args = parser.parse_args()
	args.func(args)
	print "hello world"
#	jelou_copy_image("CSC123456")


