from datetime import datetime
from datetime import timedelta
from datetime import *
import time
# given_time = datetime.now()
# n = 15
# final_time = given_time + timedelta(seconds=n)
# diff = final_time - given_time
# print(diff)
# print(int(datetime.datetime.utcnow().timestamp()))
# print(given_time)
# print(final_time)

# future_date = datetime.datetime(1970, 1, 2)
# past_date = datetime.datetime(1970, 1, 1)
# difference = (future_date - past_date)
# total_seconds = difference.total_seconds()
# print(total_seconds)

date1 = datetime.now()
time.sleep(2)
date2 = datetime.now()

a_timedelta = date1 - date2
seconds = a_timedelta.total_seconds()

print(type(seconds))