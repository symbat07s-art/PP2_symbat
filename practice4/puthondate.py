#1

from datetime import date, timedelta
today = date.today()
five_days_ago = today - timedelta(days=5)

print(five_days_ago)

#2

from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

#drop
from datetime import datetime

now  = datetime.now()
without_microseconds = now.replace(microsecond=0)

print(now)
print(without_microseconds)

#difference
from datetime import datetime

date1 = datetime(2026, 9, 26, 12, 0, 0)
date2 = datetime(2026, 9, 26, 15, 30, 0)

difference = date2 - date1
seconds = difference.total_second()

print(seconds)

