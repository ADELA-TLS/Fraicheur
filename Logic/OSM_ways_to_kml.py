from lxml import etree
import json

def OSM_ways_to_kml(data):
    nodes = {}
    ways = {}
    for element in data["elements"]:
        ID = str(element["id"])
        if element["type"]=="node":
            nodes[ID] = [str(element["lon"]), str(element["lat"])]
        if element["type"]=="way":
            ways[ID] = {"nodes": element["nodes"], "name": "Inconnu"}
            if "tags" in element:
                if "name" in  element["tags"]:
                    ways[ID]["name"] = element["tags"]["name"]

    kml = etree.Element("kml")
    kml.attrib["xmlns"] = "http://www.opengis.net/kml/2.2"
    document = etree.SubElement(kml, "Document")
    for key in ways.keys():
        way = etree.SubElement(document, "Placemark")
        name = etree.SubElement(way, "name")
        name.text = key
        description = etree.SubElement(way, "description")
        description.text = ways[key]["name"]
        polygon = etree.SubElement(way, "Polygon")
        outerBoundaryIs = etree.SubElement(polygon, "outerBoundaryIs")
        LinearRing = etree.SubElement(outerBoundaryIs, "LinearRing")
        coordinates = etree.SubElement(LinearRing, "coordinates")
        coordinates.text = "\n".join([",".join(nodes[str(ID)]) for ID in ways[key]["nodes"]])
        
    return etree.tostring(kml, encoding="UTF-8", pretty_print=True, xml_declaration=True)
	
#Example
with open('../Data/park_osm.txt') as json_file:
    data = json.load(json_file)

kml = OSM_ways_to_kml(data)

with open('../Data/park_osm.kml', 'wb') as f:
    f.write(kml)
