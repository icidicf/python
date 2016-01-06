#!/usr/bin/python3

from urllib.request import urlopen
import sys
import pprint
import json

url = 'http://web.juhe.cn:8080/environment/air/cityair?city=shanghai&key=28c2781655638400b6dcc9b69193b513'
rsp = urlopen(url)
result = rsp.readall().decode('utf-8')

print (result)

'''
if len(sys.argv) < 2:
    print "please give json file"
    sys.exit(0)


filename = sys.argv[1]
print "input file is " + filename



with open(filename , 'r') as f:
    jdata = json.loads(f)
'''

jdata = json.loads(result)


print ("result code is " + jdata['resultcode'])
print ("reason is " + jdata['reason'])
print ("error_code is " + str(jdata['error_code']))


pprint.pprint(jdata)

print ("---------------------------------------------------")
print (json.dumps(jdata,indent=4, sort_keys=True, ensure_ascii=False))
