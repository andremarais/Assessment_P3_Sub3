import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

CT_osm = "cape-town_south-africa-sample.osm"

def audit_post_code(post_codes, post_code):
        if len(post_code) != 4:
            print post_code
            post_codes[post_code].add(post_code)


def is_post_code(elem):
    return elem.attrib['k'] == "addr:postcode"


def audit(osmfile):
    osm_file = open(osmfile, "r")
    post_codes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_post_code(tag):
                    # print tag.attrib['v']
                    audit_post_code(post_codes, tag.attrib['v'])

    return post_codes


post_codes = audit(CT_osm)

pprint.pprint(dict(post_codes))

