import urllib.request
import json
import time
import math
import os
import geopy.distance
class Bogey:
    def __init__(self, Type, Bearing, Range, Altitude, Threat):
        self.Type = Type
        self.Bearing = Bearing
        self.Range = Range
        self.Altitude = Altitude
		self.Threat = Threat
try:
	target = "[RED VIPER]"  #Enter Name Here
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
	while True:
			with urllib.request.urlopen("http://dcs.hoggitworld.com/") as url:
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
				print("---------------------------")
				print("Bogey dope for "+target+".")
				print("---------------------------\n")
				for i in range(len(data["objects"])):
					if data["objects"][i]["Flags"]["Human"] == False:
						if data["objects"][i]["Coalition"] == "Allies" and data["objects"][i]["Flags"]["Born"] == True:
							Type = False
							if data["objects"][i]["Name"] == "Su-27":
								Type = "Su-27"
							elif data["objects"][i]["Name"] == "F-5E-3":
								Type = "F5"
							elif data["objects"][i]["Name"] == "Su-25T":
								Type = "Su-25T"
							elif data["objects"][i]["Name"] == "Mi-26":
								Type = "Mi-26"
							elif data["objects"][i]["Name"] == "J-11A":
								Type = "J-11A"
							elif data["objects"][i]["Name"] == "A-50":
								Type = "A-50"


							Lat = data["objects"][i]["LatLongAlt"]["Lat"]
							Lon = data["objects"][i]["LatLongAlt"]["Long"]
							Alt = data["objects"][i]["LatLongAlt"]["Alt"]
							if Type != False:
								MyPos = (MyLat, MyLon)
								TPos = (Lat, Lon)
								Distance = geopy.distance.distance(MyPos,TPos).nm
								A = (MyLat, MyLon)
								B = (Lat, Lon)
								Bearing = calculate_initial_compass_bearing(A, B)
								b = Bogey(Type, Bearing, Distance, round(Alt/1000,1))
								unsorted_bogeys.append(b)
								sorted_bogeys = sorted(unsorted_bogeys, key=lambda x: x.Range)
								count = count + 1
			for i in sorted_bogeys:
				print("Target Type:\t"+i.Type)
				print("Distance:\t"+str(round(i.Range,1))+" Miles")
				print("Bearing:\t"+str(round(i.Bearing,0)))
				print("Altitude:\tAngels "+str(round(i.Altitude/1000,1)))
				print("\r")
			print("Target Count:\t"+str(count))
			time.sleep(10)
except:
	print("Something went wrong. The target is probably not in the server.")
