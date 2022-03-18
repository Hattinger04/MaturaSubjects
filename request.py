import requests
import json
import keys

key = keys.requestkey
host = keys.host
userlist = keys.userlist

response = requests.put("%s" % (host) ,data={
    "key" : key,
    "users": json.dumps(userlist)
}).json()
print(response)


response = requests.get("%s" % (host), data={
    "username" : "Username",
    "password" : "Password"
}).json()
print(response)
