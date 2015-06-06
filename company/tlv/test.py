#!/usr/bin/python

def change_hex_to_string(items):
	output=""
	for it in items:
		output += chr(int(it,16))
	return output


def chunk_with_specified_width(string, length):
	return (string[i+0: i+length] for i in range(0, len(string), length))
 

items = chunk_with_specified_width("746573742D74696D6500",2)
print items
str2=change_hex_to_string(items)
print str2


