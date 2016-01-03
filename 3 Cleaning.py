import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

CT_osm = "cape-town_south-africa-sample.osm"

#########################
# Cleaning street types #
#########################

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Way", "Close", "Crescent"]

mapping = {"St": "Street",
           "St.": "Street",
           "Ave" : "Avenue",
           'Rd.' : "Road",
           "st" : "Street",
           "Rd" :"Road"}


# returns the last word from the address string. if there is a second word, it will check of the word is in the
# expected list. If not, it will add the 'new' street type to the street_types dictionary
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


# function to check of the tag is a street address
def is_street_name(elem):
    return elem.attrib['k'] == "addr:street"


# function to iterate through all the elements and apply the audit function to each node and tag, if the tag is a
# street address
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


# function to find and replace the values in the mapping array
def update_name(name, mapping):
    to_replace = street_type_re.search(name).group()
    if to_replace in mapping.keys():
        name = re.sub(to_replace,mapping.values()[mapping.keys().index(to_replace)], name)
    return name




street_types = audit(CT_osm)

for st_type, ways in street_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name

