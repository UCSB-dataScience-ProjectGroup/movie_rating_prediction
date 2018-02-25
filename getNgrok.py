import os
import json

os.system("curl http://localhost:4040/api/tunnels > tunnels.json")

with open('tunnels.json') as data_file:
    datajson = json.load(data_file)

msg = ""
msg = datajson['tunnels'][0]['public_url']

file = open('ngrokTunnel.txt', 'w')
file.write(msg)

os.system("git add ngrokTunnel.txt")
os.system('git commit --amend --no-edit')
os.system('git push origin master')
