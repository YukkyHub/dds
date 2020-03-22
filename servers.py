import json

with open('data/servers/index.json') as f:
    data = json.load(f)

data2 = json.dumps(data, indent=2)
servers = json.loads(data2)

nb_servers = len(servers)

print('Nombre de serveurs :', nb_servers)
