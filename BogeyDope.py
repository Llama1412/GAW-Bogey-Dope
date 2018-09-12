import urllib.request
import json
import time
import math
import os
import geopy.distance
from prettytable import PrettyTable
from termcolor import colored
class Bogey:
	def __init__(self, Type, Bearing, Range, Altitude, Threat):
			self.Type = Type
			self.Bearing = Bearing
			self.Range = Range
			self.Altitude = Altitude
			self.Threat = Threat

class Player:
	def __init__(self, Name, Plane):
		self.Name = Name
		self.Plane = Plane


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
	return Bogey(Type, Bearing, Distance, Alt, Threat)

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
while True:
	os.system('cls' if os.name=='nt' else 'clear')
	print("Welcome to the GAW GCI Tool.")
	print("1 - Bogey dope")
	print("2 - List all players")
	print("3 - Quit")
	choice = str(input("Make choice:\t"))
	if choice == str("1"):
		try:
			target = input("Enter user:\t")  #Enter Name Here
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
					print("Target Count:\t"+str(len(sorted_bogeys)))
					time.sleep(10)
		except Exception as e:
			print("Something went wrong. "+target+" is probably not in the server.")
			print("Here is a list of people currently in the server:\n")
			for i in range(len(data["objects"])):
				if data["objects"][i]["Flags"]["Human"] == True:
					print(data["objects"][i]["UnitName"])
			print("\r")
			print("Error message was: \t"+str(e))
			os.system('pause')

	elif choice == "2":
		os.system('cls' if os.name=='nt' else 'clear')
		count = 0
		people = []
		x = PrettyTable()
		x.field_names = ["Name", "Aircraft"]
		try:
			with urllib.request.urlopen("https://state.hoggitworld.com/") as url:
				data = json.loads(url.read().decode())
				for i in range(len(data["objects"])):
					if data["objects"][i]["Flags"]["Human"] == True:
						count = count + 1
						name = str(data["objects"][i]["UnitName"])
						plane = str(data["objects"][i]["Name"])
						people.append(Player(name, plane))
				sorted_people = sorted(people, key=lambda x: x.Name)
				for player in sorted_people:
					x.add_row([player.Name,player.Plane])
				x.align["Name"] = "l"
				x.align["Aircraft"] = "l"
				print(x)
			print("\r")
			print("Player count:\t"+str(count))
			os.system('pause')
		except Exception as e:
			print("An error has occurred.")
			print("Error message:\t"+str(e))
			raise
			os.system("pause")
	elif choice == "3":
		sys.exit()
	else:
		print("Invalid choice.")
		time.sleep(2)
