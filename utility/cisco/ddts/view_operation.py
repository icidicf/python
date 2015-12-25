#!/router/bin/python
import sys
import os
import re


vt = "/opt/vde/services/instances/vde_latest/bin/vde_tool "
vtn = vt + "--Vno_sync"

def patch_and_sa(diff_file, ddts):
    print "go to patch %s for %s" % (diff_file, ddts)
    os.system(vtn + " cc_patch " + diff_file) 
    print "go to get temp.diff for %s" %  ddts
    os.system(vtn + " cc_diff > temp.diff")



if __name__ == "__main__":
    if not len(sys.argv) > 1:
	print __doc__
	print "plese in put arg"
	sys.exit(1)

    diff_name = sys.argv[1]
    cur_pwd = os.getcwd();
    m = re.match ('.*(CSC.*[0-9]{5}).*', str(cur_pwd))
    ddts_name = m.group(1)
    print "diff fie %s  cur path %s ddts %s" % (diff_name, \
    cur_pwd, m.group(1))


    patch_and_sa(diff_name, ddts_name)
