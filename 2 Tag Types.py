import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

CT_osm = 'cape-town_south-africa-sample.osm'

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

'''
key_type goes through all the tags to see if they're lower case, if they contain a colon while being lower case
and to see if there are any special characters that might be problematic.

The results show quite a few 'other' tag values. It looks like the predominant issues are more than one colon and
upper case characters.

Looking at the upper case tags, they a prefixed by CoCT (City of Cape Town). These seem to refer to road signs

The double colon tags mainly refer to sea marks, but also contain mountain bike route information and some other
miscellaneous information
'''


def key_type(element, keys):
    if element.tag == "tag":
        elem = element.attrib['k']

        l = lower.search(elem)  # test if lower case
        lc = lower_colon.search(elem)  # test if lower case with colon
        pc = problemchars.search(elem)  # checks if string contains special characters
        if l:
            keys['lower'] += 1

        if lc:
            keys['lower_colon'] += 1

        if pc:
            keys['problemchars'] += 1
            print 'problem chars ', elem, element.attrib['v']

        if not l and not lc and not pc:  # if none of the above, classify as 'other'
            keys['other'] += 1
            print 'other ', elem, '|', element.attrib['v']

        pass
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}  # sets up array for classification
    for _, element in ET.iterparse(filename):  # loops through elements
        keys = key_type(element, keys)  # calls the above function

    return keys

print process_map(CT_osm)

