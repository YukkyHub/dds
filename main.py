import json
from datetime import datetime

events2016, events2017, events2018, events2019 = [], [], [], []

with open('data/activity/analytics/events-2018-00000-of-00001.json') as f2019:
    for line in f2019:
        events2018.append(json.loads(line))


events2018_2 = json.dumps(events2019, indent=2)
print(events2018[0]["timestamp"][:-1])

date = datetime.strptime(events2018[0]["timestamp"][:-1], '%Y-%m-%dT%H:%M:%S.%f')

now = datetime.now()

time = now - date
print(time)
time += (now - date)
print(time)
