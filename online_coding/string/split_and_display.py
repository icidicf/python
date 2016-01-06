#!/usr/bin/python
import sys
import re
if len(sys.argv) < 2 :
	input = "/users/jelou/local/bin/:/users/jelou/local/bin/cbr:/users/jelou/local/bin/10k:/users/jelou/bin:/router/bin:/usr/bin:/usr/sbin:/usr/ucb:/usr/xpg4/bin:/usr/ccs/bin:/opt/vde/services/instances/vde_latest/bin/vnc:/opt/vde/services/instances/vt-226/bin:/usr/kerberos/bin:/usr/local/bin:/bin:/usr/bin:/usr/X11R6/bin:/opt/vde/services/instances/vt-226/bin/vnc:/opt/vde/bin:/usr/X11R6/bin:/usr/cisco/bin:/usr/X11R6/bin"

else :
	input = sys.argv[1]

entry = re.split(":",input)
i=0
for it in entry:
	print "NO.%d is %s" %(i, it)
	i += 1




