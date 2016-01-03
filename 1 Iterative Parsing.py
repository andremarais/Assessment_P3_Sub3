import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
from zipfile import ZipFile

'''The purpose of this function is to iterate through the OSM file to see what types of tags there are, and
how many'''


CT_osm ='cape-town_south-africa-sample.osm'

tags = defaultdict(int)

def count_tags(filename):
    for value, elm in ET.iterparse(CT_osm):
        m = elm.tag
        tags[m] += 1
    return tags

tags_ = count_tags(CT_osm)
pprint.pprint(tags_)



"""
{'node': 242589,
'nd': 296162,
'member': 6600,
'tag': 109185,
'relation': 585,
'way': 43152,
'osm': 1})

tags are quite very to the chicago data. will look into nodes and ways.
relation doesn't seem to have data of a uniform nature. It refers to malls, boundaries and traffic rules, but will
still include it regardless

"""

