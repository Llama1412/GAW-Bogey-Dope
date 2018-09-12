import urllib.request
import json
import os
count = 0
with urllib.request.urlopen("http://dcs.hoggitworld.com/") as url:
	data = json.loads(url.read().decode())
	for i in range(len(data["objects"])):
		if data["objects"][i]["Flags"]["Human"] == True:
			count = count + 1
			print(data["objects"][i]["UnitName"])
			print("\r")
print("Player count:\t"+str(count))
os.system('pause')
