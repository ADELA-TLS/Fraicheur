import requests
import pandas as pd
import json

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json][timeout:25];
area["name"="Toulouse"]["admin_level"="8"]->.boundaryarea;
way(area.boundaryarea)["amenity"="fountain"];
  foreach(
    node(w)->.d;
    .n is_in->.a;
    area.a[name][boundary=administrative][admin_level~"^[2-8]$"] -> .a;
    out center;
    convert way ::=::,
              ::id = id(),
              is_in=a.set("{" + t["admin_level"] + ":" + t["name"] + "}");

    out;
  );
"""
response = requests.get(overpass_url,
                        params={'data': overpass_query})
data = response.json()

fountainData = {"lat": [], "lon": [], "name": [], "id":[]}
for element in data["elements"]:
    if "is_in" not in element["tags"]:
        fountainData["id"].append(element["id"])
        fountainData["lat"].append(element["center"]["lat"])
        fountainData["lon"].append(element["center"]["lon"])
        if "name" in element["tags"]:
            fountainData["name"].append(element["tags"]["name"])
        else:
            fountainData["name"].append("Inconnu")

fountain = pd.DataFrame(fountainData)
fountain.to_csv("../Data/fontaine.csv", sep=";", encoding="ISO-8859-1", index=False)