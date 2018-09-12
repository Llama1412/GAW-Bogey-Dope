import urllib.request
import json
import time
import math
import os
import geopy.distance
from termcolor import colored
class Bogey:
	def __init__(self, Type, Bearing, Range, Altitude, Threat):
			self.Type = Type
			self.Bearing = Bearing
			self.Range = Range
			self.Altitude = Altitude
			self.Threat = Threat

class THREAT:
	HIGH = "red"
	MEDIUM = "yellow"
	LOW = "green"
	NONE = "blue"

threats = {
	"Su-27": THREAT.HIGH,
	"F-5E-3": THREAT.HIGH,
	"Su-25T": THREAT.MEDIUM,
	"Mi-26": THREAT.LOW,
	"J-11A": THREAT.HIGH,
	"A-50": THREAT.NONE,
	"MiG-21Bis": THREAT.HIGH,
	"MiG-29S": THREAT.HIGH,
	"MiG-31": THREAT.HIGH
}
try:
	target = input("Enter user:\t")  #Enter Name Here
	#target = "Skillhouse246"
	def calculate_initial_compass_bearing(pointA, pointB):
	    lat1 = math.radians(pointA[0])
	    lat2 = math.radians(pointB[0])
	    diffLong = math.radians(pointB[1] - pointA[1])
	    x = math.sin(diffLong) * math.cos(lat2)
	    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
	            * math.cos(lat2) * math.cos(diffLong))
	    initial_bearing = math.atan2(x, y)
	    initial_bearing = math.degrees(initial_bearing)
	    compass_bearing = (initial_bearing + 360) % 360
	    return compass_bearing
	
	def make_bogey(target, MyPos):
		Lat = target["LatLongAlt"]["Lat"]
		Lon = target["LatLongAlt"]["Long"]
		Alt = target["LatLongAlt"]["Alt"]
		TPos = (Lat, Lon)
		Distance = geopy.distance.distance(MyPos,TPos).nm
		A = (MyLat, MyLon)
		B = (Lat, Lon)
		Bearing = calculate_initial_compass_bearing(A, B)
		return Bogey(Type, Bearing, Distance, round(Alt/1000,1), Threat)

	def print_bogeydope(player_name, bogeys):
		print(colored("---------------------------","cyan"))
		print(colored("Bogey dope for "+player_name+".","cyan"))
		print(colored("---------------------------\n","cyan"))
		for bogey in bogeys:
				print(colored("Target Type:\t"+bogey.Type,bogey.Threat))
				print(colored("Distance:\t"+str(round(bogey.Range,1))+" Miles",bogey.Threat))
				print(colored("Bearing:\t"+str(round(bogey.Bearing,0)),bogey.Threat))
				print(colored("Altitude:\tAngels "+str(round(bogey.Altitude/1000,1)),bogey.Threat))
				print("\r")
		print("Target Count:\t"+str(len(bogeys)))

	while True:
			with urllib.request.urlopen("http://state.hoggitworld.com/") as url:
				data = json.loads(url.read().decode())
				for i in range(len(data["objects"])):
					if data["objects"][i]["Flags"]["Human"] == True:
						if data["objects"][i]["UnitName"] == target:
							MyLat = data["objects"][i]["LatLongAlt"]["Lat"]
							MyLon = data["objects"][i]["LatLongAlt"]["Long"]
							MyAlt = data["objects"][i]["LatLongAlt"]["Alt"]

				os.system('cls' if os.name=='nt' else 'clear')
				unsorted_bogeys = []
				count = 0
				for i in range(len(data["objects"])):
					if data["objects"][i]["Flags"]["Human"] == False:
						if data["objects"][i]["Coalition"] == "Allies" and data["objects"][i]["Flags"]["Born"] == True:
							plane = data["objects"][i]
							Type = False
							Threat = False
							if plane["Name"] in threats.keys():
								Type = plane["Name"]
								Threat = threats[plane["Name"]]

							if not Type:
								continue
							my_pos =(MyLat, MyLon) 
							unsorted_bogeys.append(make_bogey(plane,my_pos))
							
			sorted_bogeys = sorted(unsorted_bogeys, key=lambda x: x.Range)
			print_bogeydope(target, sorted_bogeys)
			time.sleep(10)
except Exception as e:
	print("Something went wrong. "+target+" is probably not in the server." + str(e))
	print("Here is a list of people currently in the server:\n")
	for i in range(len(data["objects"])):
		if data["objects"][i]["Flags"]["Human"] == True:
			print(data["objects"][i]["UnitName"])
	print("\r")
	os.system('pause')
