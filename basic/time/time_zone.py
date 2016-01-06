#!/router/bin/python

from datetime import datetime
from pytz import timezone
import pytz
date_format = '%m/%d/%Y-%H:%M:%S-%Z'
utc_time = datetime.now(tz=pytz.utc)

cn_time = utc_time.astimezone(timezone('Asia/Shanghai'))
print "Shanghai time     " + cn_time.strftime(date_format)

print "UTC time          " + utc_time.strftime(date_format)

pst_time = utc_time.astimezone(timezone('US/Pacific'))
print "US Pacific time   " + pst_time.strftime(date_format)



