import json, csv
import re
import time
from datetime import datetime, timedelta

with open('data/messages/index.json', encoding="utf8") as f:
    data = json.load(f)

data2 = json.dumps(data, indent=2)
messages = json.loads(data2)

mp_list = []
msg = 0


def _dmlist():

    for i in messages:
        if type(messages[i]) == str:
            if messages[i].startswith('Direct Message with'):
                mp_list.append(messages[i][19:])


def _totalMessages(total_msg=0):

    for i in messages:
        path = 'data/messages/' + str(i) + '/messages.csv'
        with open(path, encoding="utf8") as m:
            pmsg = csv.DictReader(m, delimiter=',')
            col = list(pmsg)
            total_msg += len(col)
    return total_msg


def _rankMessages(top=10):
    ranking = {}
    for id in messages:
        path = 'data/messages/' + str(id) + '/messages.csv'
        with open(path, encoding="utf8") as m:
            pmsg = csv.DictReader(m, delimiter=',')
            max_msg = len(list(pmsg))
            if type(messages.get(id)) != type(None):
                if(messages.get(id)[:20]) == "Direct Message with ":
                    ranking[messages.get(id)[20:]] = max_msg
                else:
                    ranking["Group/Server: " + messages.get(id)] = max_msg
    ranking = sorted(ranking.items(), key=lambda t: t[1], reverse=True)
    return ranking[:top][:top]



def _occWords():
    ranking = {}
    for id in messages:
        path = 'data/messages/' + str(id) + '/messages.csv'
        with open(path, encoding="utf8") as m:
            pmsg = csv.DictReader(m, delimiter=',')
            for row in pmsg:
                msgs = row["Contents"].split(' ')
                for msg in msgs:
                    if type(ranking.get(msg)) != type(None):
                        ranking[msg] = int(ranking.get(msg)) + 1
                    else:
                        ranking[msg] = 1
    ranking = sorted(ranking.items(), key=lambda t: t[1], reverse=True)
    return ranking[:100][:100]


def _findPassword():
    potential_pw = []
    highly_pw = []
    pattern = re.compile("^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z]{8,}$")
    pattern_res = re.compile("^([0-9][0-9][0-9]|[1-4][0-9][0-9][0-9])x([1-9][0-9][0-9]|[1-4][0-9][0-9][0-9])$")
    pattern_min = re.compile("^(([0-9][0-9][0-9]|[0-9][0-9])min([0-9][0-9])s$)|([0-9][0-9][0-9]|[0-9][0-9])min$")
    mdp = ["mdp : ", "mdp :", "mdp:", "mdp: ", "password :", "password : "]
    with open('auth_words.csv', encoding="utf8") as m:
        auth_words = csv.DictReader(m, delimiter=',')
        for id in messages:
            path = 'data/messages/' + str(id) + '/messages.csv'
            with open(path, encoding="utf8") as m:
                pmsg = csv.DictReader(m, delimiter=',')
                for row in pmsg:
                    msgs = row["Contents"].split(' ')
                    if any(x in row["Contents"] for x in mdp):
                        try:
                            if highly_pw.count(msgs[msgs.index(':') + 1]) == 0:
                                highly_pw.append(msgs[msgs.index(':') + 1])
                        except:
                            None
                    for msg in msgs:
                        if pattern.match(msg):
                            if potential_pw.count(msg) == 0:
                                potential_pw.append(msg)
        for word in auth_words:
            for pw in potential_pw:
                if pw.find(word['mot']) != -1:
                    potential_pw.remove(pw)
                elif pattern_res.match(pw) or pattern_min.match(pw):
                    potential_pw.remove(pw)
    print(len(potential_pw))
    return highly_pw, potential_pw


def _msgStreak(days=1, size=10):
    streak = {}

    for id in messages:
        if type(messages[id]) == str:
            if messages[id].startswith('Direct Message with'):
                streak[messages[id][19:]] = 1

                path = 'data/messages/' + str(id) + '/messages.csv'
                with open(path, encoding="utf8") as m:
                    pmsg = csv.DictReader(m, delimiter=',')
                    col = list(pmsg)
                    col.reverse()
                    line = 0
                    cur_streak = 0
                    for row in col:
                        try:
                            if line > 0:
                                if ((datetime.strptime(row["Timestamp"][:-6],
                                                       '%Y-%m-%d %H:%M:%S.%f')).date() == previousDate.date()
                                        + timedelta(days=1)):
                                    cur_streak += 1
                                else:
                                    if ((datetime.strptime(row["Timestamp"][:-6],
                                                           '%Y-%m-%d %H:%M:%S.%f') - previousDate).days) >= days:
                                        if cur_streak > streak[messages[id][19:]]:
                                            streak[messages[id][19:]] = cur_streak + 1
                                        cur_streak = 0
                        except ValueError:
                            None
                        try:
                            previousDate = datetime.strptime(row["Timestamp"][:-6], '%Y-%m-%d %H:%M:%S.%f')
                        except ValueError:
                            previousDate = datetime.strptime(row["Timestamp"][:-6], '%Y-%m-%d %H:%M:%S')

                        line += 1
    streak = sorted(streak.items(), key=lambda item: item[1], reverse=True)
    return streak[:size]



def _whereLive():
    locations = {}
    most_potential_city = 'unknown'
    for id in messages:
        path = 'data/messages/' + str(id) + '/messages.csv'
        with open(path, encoding="utf8") as m:
            pmsg = csv.DictReader(m, delimiter=',')
            for row in pmsg:
                if row["Contents"].find("j'habite") != -1:
                    msgs = row["Contents"][row["Contents"].find("j'habite")+8:row["Contents"].find("j'habite")+30].split(' ')
                    for msg in msgs:
                        if type(locations.get(msg.lower())) != type(None):
                            if len(msg) > 3:
                                locations[msg.lower()] = int(locations.get(msg.lower())) + 1
                        else:
                            locations[msg.lower()] = 1
    locations = sorted(locations.items(), key=lambda t: t[1], reverse=True)
    most_potential_city = list(locations)[0]
    return most_potential_city[0]


def _smileysUsage():
    smileys = {}
    pattern = re.compile("(\A|\s)(((>[:;=+])|[>:;^=+])[,*]?[-~+o]?(\)+|\(+|\}+|\{+|\]+|\[+|\|+|\/+|\+|>+|<+|D+|"
                         "[@#!OoPpXxZS$03^])|>?[xX8][-~+o]?(\)+|\(+|\}+|\{+|\]+|\[+|\|+|\/+|\+|>+|<+|D+|d+))(\Z|\s)")
    for id in messages:
        path = 'data/messages/' + str(id) + '/messages.csv'
        with open(path, encoding="utf8") as m:
            pmsg = csv.DictReader(m, delimiter=',')
            for row in pmsg:
                msgs = row["Contents"].split(' ')
                for msg in msgs:
                    if type(smileys.get(msg)) != type(None):
                        if pattern.match(msg):
                            smileys[msg] = int(smileys.get(msg)) + 1
                    else:
                        smileys[msg] = 1
    smileys = sorted(smileys.items(), key=lambda t: t[1], reverse=True)
    return smileys[:30][:30]


def _test():
    locations = {}
    most_potential_city = 'unknown'
    for id in messages:
        path = 'data/messages/' + str(id) + '/messages.csv'
        with open(path, encoding="utf8") as m:
            pmsg = csv.DictReader(m, delimiter=',')
            for row in pmsg:
                    msgs = row["Contents"].split(' ')
                    for msg in msgs:
                        if msg.lower() == "t'aime":
                            print(messages.get(id))
                            print(row["Contents"])


print(_test())





