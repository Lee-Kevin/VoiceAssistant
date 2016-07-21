#!/usr/bin/env python

from datetime import datetime, timedelta
from pytz import timezone
import pytz
import time
# fmt = '%Y-%m-%d %H:%M:%S %Z%z'
# fmt = '%Y-%m-%d %H:%M'
fmt = '%m-%d %H:%M'
local_tz = timezone('Asia/Shanghai') 
def TimeUpdate():
    now_utc = datetime.utcnow()
    now_utc = pytz.utc.localize(now_utc)
    local_time = now_utc.astimezone(local_tz)
    return local_time.strftime(fmt)
    
if __name__ == "__main__":
    while True:
        print(TimeUpdate())
        time.sleep(60)
    