#!/usr/bin/python

import re


p = re.compile('(a)b')
m = p.match('ab')

p = re.compile('.*?(\d+)lyp')
m = p.match("wq12lyp")
print m.group(1)


text = "c8fb.26a6.c4c6 93.15.0.35      C6/0/0/U15    w-online          2     0.00   1793   0   N "

#p = re.compile('C6/0/0/U(\d+)')
p = re.compile('(C6/0/0)')
m = p.search(text)
print m.group(1)
