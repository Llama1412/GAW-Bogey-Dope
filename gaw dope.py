import urllib.request
import json
import time
import math
target = "Terminus"  #Enter Name Here
count = 0
def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
with urllib.request.urlopen("http://dcs.hoggitworld.com/") as url:
    data = json.loads(url.read().decode())
    for i in range(len(data["objects"])):
        if data["objects"][i]["Flags"]["Human"] == True:
            if data["objects"][i]["UnitName"] == target:
                MyLat = data["objects"][i]["LatLongAlt"]["Lat"]
                MyLon = data["objects"][i]["LatLongAlt"]["Long"]
                MyAlt = data["objects"][i]["LatLongAlt"]["Alt"]

    for i in range(len(data["objects"])):
        if data["objects"][i]["Flags"]["Human"] == False:
            if data["objects"][i]["Coalition"] == "Allies":
                Type = False
                if data["objects"][i]["Name"] == "Su-27":
                    Type = "Su-27"
                elif data["objects"][i]["Name"] == "F-5E-3":
                    Type = "F5"
                elif data["objects"][i]["Name"] == "Su-25T":
                    Type = "Su-25T"
                elif data["objects"][i]["Name"] == "Mi-26":
                    Type = "Mi-26"

                Lat = data["objects"][i]["LatLongAlt"]["Lat"]
                Lon = data["objects"][i]["LatLongAlt"]["Long"]
                Alt = data["objects"][i]["LatLongAlt"]["Alt"]
                if Type != False:
                    Distance = math.sqrt(((MyLat+Lat))*(MyLat+Lat)+((MyLon+Lon)*(MyLon+Lon)))
                    A = (MyLat, MyLon)
                    B = (Lat, Lon)
                    Bearing = calculate_initial_compass_bearing(A, B)
                    print("Target Type:\t"+Type)
                    print("Distance:\t"+str(round(Distance,1))+" Miles")
                    print("Bearing:\t"+str(round(Bearing,0)))
                    print("Altitude:\tAngels: "+str(round(Alt/1000,1)))
                    print("\r")
                    count = count + 1
print("Target Count:\t"+str(count))
