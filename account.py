import json

with open('data/account/user.json') as f:
    data = json.load(f)

data2 = json.dumps(data, indent=2)

email = data.get("email")
username = data.get("username")
phone_number = data.get("phone")

nb_PrivateMsg = len(data.get("relationships"))
list_PrivateMsg = []
main_ip = data.get("ip")
list_ip = []
billing_info = {}
usr_accounts = {}

for accounts in data["connections"]:
    usr_accounts[accounts.get('type')[0].upper() + accounts.get('type')[1:]] = accounts.get('name')

for ip in data["mfa_sessions"]:
    list_ip.append(ip['ip'])

for pay in data["payments"]:
    billing_info["name"] = pay["payment_source"].get("billing_address").get("name")
    billing_info["city"] = pay["payment_source"].get("billing_address").get("city")
    billing_info["country"] = pay["payment_source"].get("billing_address").get("country")
    billing_info["postal_code"] = pay["payment_source"].get("billing_address").get("postal_code")
    billing_info["address"] = pay["payment_source"].get("billing_address").get("line_1")


def lister_pm():
    for users in data["relationships"]:
        list_PrivateMsg.append(users['user'].get('username'))
    return list_PrivateMsg


print(billing_info)

