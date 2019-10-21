import pandas as pd
import json
import re
import geopy.distance

df = pd.read_csv("../Data/arbres-d-alignement.csv", sep=";")

treeType = set()
for index, row in df.iterrows():

    # Compute length of the way
    parseGeoShape = json.loads(df.loc[index, "Geo Shape"])
    wayLength = 0
    if parseGeoShape["type"] == "LineString":
        points = parseGeoShape["coordinates"]
        for i in range(1, len(points)):
            wayLength += geopy.distance.distance(tuple(points[i - 1]), tuple(points[i])).m
    elif parseGeoShape["type"] == "MultiLineString":
        section = parseGeoShape["coordinates"]
        for points in section:
            for i in range(1, len(points)):
                wayLength += geopy.distance.distance(tuple(points[i - 1]), tuple(points[i])).m
    df.loc[index, "Longueur de la voie"] = wayLength

    # Retrieve number of trees for each type of trees in Patrimoine and compute the total number of trees
    parsePatrimoine = re.findall("([0-9]+)\s([A-Z-\s]+)", row["patrimoine"])
    nbrTrees = 0
    for couple in parsePatrimoine:
        df.loc[index, couple[1].rstrip()] = int(couple[0])
        nbrTrees += int(couple[0])
    df.loc[index, "Nombre total d'arbre"] = nbrTrees

df.to_csv("C:/Users/fabien/Desktop/OpenDataToulouse/OpenData/Environnement/arbres-d-alignement-reformated.csv", index=False, sep=";")
df.to_csv("../Data/arbres-d-alignement-reformated.csv", index=False, sep=";")