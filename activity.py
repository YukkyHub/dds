import json
from datetime import datetime, timedelta

events2016, events2017, events2018, events2019 = [], [], [], []

with open('data/activity/analytics/events-2016-00000-of-00001.json') as f2016:
    for line in f2016:
        events2016.append(json.loads(line))
with open('data/activity/analytics/events-2017-00000-of-00001.json') as f2017:
    for line in f2017:
        events2017.append(json.loads(line))
with open('data/activity/analytics/events-2018-00000-of-00001.json') as f2018:
    for line in f2018:
        events2018.append(json.loads(line))

with open('data/activity/analytics/events-2019-00000-of-00001.json') as f2019:
    for line in f2019:
        events2019.append(json.loads(line))

events2019_2 = json.dumps(events2019, indent=2)
all_l = [events2016, events2017, events2018, events2019]

nb_city = 0
sessions = 0

list_games = []

applications = []

connected_time = 0
days = 0
date = datetime.now()

for m in all_l:
    for i in m:
        if 'city' in i:
            nb_city += 1
        if i["event_type"] == "launch_game" and i.get("game") not in list_games:
            list_games.append(i.get("game"))
        if i["event_type"] == "session_end":
            sessions += 1
        if "day" in i:
            if int(i.get("day")) >= int(days):
                days = i["day"]
                date = datetime.strptime(i["timestamp"][:-1], '%Y-%m-%dT%H:%M:%S.%f')
        if "application_id" in i:
            if i.get("application_id") not in applications:
                applications.append(i.get("application_id"))


def _time():

    dict = {}
    total_time = timedelta(seconds=0)

    for n in all_l:
        for i in n:
            if "session_start" or "session_end":
                if i.get('session') not in dict:
                    if i.get('session') is not None:
                        num_session = i.get('session')
                        dict[num_session] = datetime.strptime(i["timestamp"][:-1], '%Y-%m-%dT%H:%M:%S.%f')
                elif dict.get(i.get('session')) > datetime.strptime(i["timestamp"][:-1], '%Y-%m-%dT%H:%M:%S.%f'):
                    total_time += (dict.get(i.get('session')) - datetime.strptime(i["timestamp"][:-1], '%Y-%m-%dT%H:%M:%S.%f'))
                    del dict[i.get('session')]
                elif dict.get(i.get('session')) < datetime.strptime(i["timestamp"][:-1], '%Y-%m-%dT%H:%M:%S.%f'):
                    total_time += datetime.strptime(i["timestamp"][:-1], '%Y-%m-%dT%H:%M:%S.%f') - (dict.get(i.get('session')))
                    del dict[i.get('session')]
    return total_time


x_day = timedelta(days=int(days))
first_connection = date - x_day
connected_time = _time()


print(events2019_2[:10000])
print(nb_city)
print(list_games)
print("sessions :", sessions)
print("days :", days)
print("date :", date)
print("first_connection :", first_connection)
print("total connected spent :", connected_time)
