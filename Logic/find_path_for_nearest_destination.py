import requests
import json
import geopy.distance

def find_path_for_nearest_destination(departures, destinations, dist_tresh=0.3, api_key="***********"):
    nearestDestinationPath = {}
    test=0
    for departureKey in departures.keys():
        minTime = 5*3600*1000
        nearestDestinationPath[departureKey] = {"id": None}
        for destinationKey in destinations.keys():
            if geopy.distance.distance(tuple(departures[departureKey]), tuple(destinations[destinationKey])).km < dist_tresh:

                info = { 
                "profile": "foot",
                "start": departures[departureKey],
                "end": destinations[destinationKey],
                "key": api_key
                }

                graphHopper_request = "https://graphhopper.com/api/1/route?" + \
                "&point=" + str(info["start"][0]) + "," + str(info["start"][1]) +  \
                "&point=" + str(info["end"][0]) + "," + str(info["end"][1]) + \
                "&vehicle=" + info["profile"] + \
                "&points_encoded=false" + \
                "&key=" + info["key"]

                response = requests.get(graphHopper_request)
                temp = json.loads(response.text)

                print("Request for")
                print((departureKey, destinationKey))
                print("Request status : " + str(response.status_code))
                print("Travel time: " + str(temp["paths"][0]["time"]) + " ms")
                print("Actual min time: " + str(minTime) + " ms")

                way = {}
                way["id"] = destinationKey
                way["time"] = temp["paths"][0]["time"]
                way["distance"] = temp["paths"][0]["distance"]
                way["path"] = temp["paths"][0]["points"]["coordinates"]

                if minTime > way["time"]:
                    nearestDestinationPath[departureKey] = way
                    minTime = way["time"]

        if nearestDestinationPath[departureKey]["id"] is None:
            print(departureKey + " too far from locations")
            
    return nearestDestinationPath

df = pd.read_csv("../Data/recensement-population-2015-grands-quartiers-activite.csv", encoding='latin-1', sep=";")
districts = {}
for index, row in df.iterrows():
    districts[row["Libelle des grands quartiers"]] = row["Geo Point"].split(",")

df = pd.read_csv("../Data/fontaine.csv", sep=";", encoding="ISO-8859-1")
fountains = {}
for index, row in df.iterrows():
    fountains[row["id"]] = [row["lat"], row["lon"]]
    
find_path_for_nearest_destination(districts, fountains)