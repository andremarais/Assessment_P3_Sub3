CT_osm = "cape-town_south-africa-sample.osm"

import xml.etree.cElementTree as ET
import re
import codecs
import json



lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
is_address = re.compile(r'(addr:).*')
is_CoTC = re.compile(r'CoCT:')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    # array to form JSON template in which the data will be saved
    node = {'created': {}, 'address': {}, 'pos': {}, 'node_refs': {}}

    # only looking at nodes and tags
    if element.tag == "node" or element.tag == "way":
        for n in element.attrib:
            if n in CREATED:
                node['created'][n] = element.attrib[n]  # groups the CREATED attributes
            if n in ['lat', 'lon']:
                node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]  # groups lon & lat
            if n not in CREATED and n not in ['lat', 'lon']:
                node[n] = element.attrib[n]
            node['type'] = element.tag

        for tag in element.iter("tag"):
            m = tag.attrib['k']
            if is_address.search(m):
                if m.count(":") > 1:  # removes the double colon attributes
                    pass
                else:
                    node['address'][re.sub('addr:', '', m)] = tag.attrib['v']
            elif is_CoTC.search(m):  # removes the CoCT string and changes the remainder of string to Proper
                if tag.attrib['v'] != 0:  # ignores the zero value CoTC attributes
                    node[str.title(re.sub('CoCT:', '', m))] = tag.attrib['v']
            else:
                if m.count(":") <= 1:  # ignores all the attributes with more than one colon
                    node[m] = tag.attrib['v']  # ads the non-address and non CoCT attributes

        if element.tag == 'way':  # this statement loops through the Way tags to gather all the references values
            ref_set = []
            for ref in element.iter("nd"):
                ref_set.append(ref.attrib['ref'])
            node['node_refs'] = ref_set

        '''
        deletes empty arrays
        '''
        if len(node['address']) == 0:
            node.pop('address')
        if len(node['pos']) == 0:
            node.pop('pos')
        if len(node['node_refs']) == 0:
            node.pop('node_refs')

        return node
    else:
        return None


# output function
def process_map(file_in, pretty=False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")

    return data


process_map(CT_osm, True)

