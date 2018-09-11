import urllib.request
import json
import os
with urllib.request.urlopen("http://dcs.hoggitworld.com/") as url:
    data = json.loads(url.read().decode())
    for i in range(len(data["objects"])):
        if data["objects"][i]["Flags"]["Human"] == True:
            print(data["objects"][i]["UnitName"])
            print("\r")
os.system('pause')
