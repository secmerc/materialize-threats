import xml.etree.ElementTree as et
import pdb

source = 'test.xml'

entity_style = 'rounded=0;whiteSpace=wrap;html=1;'
process_style = 'ellipse;whiteSpace=wrap;html=1;aspect=fixed;'
data_store_style = 'shape=partialRectangle;whiteSpace=wrap;html=1;left=0;right=0;fillColor=none;'

"""
xml turns into a tree
iterate over children of root
    child can be mxcell:
        can be entity or process or flow
        have child mxgeometry that includes x/y/size coords which we want to collapse onto one entity

DONE

once we have nodes with cartesian coords, we need to map edges
    for each edge, iterate over nodes and see if the start point or end point of the edge is touching the node (x or y equals side, y or x contained within side)

once we have nodes and edges, we need to map zones
    for each zone, iterate over noves and see if they are touching

once we have nodes, edges, and zones, we can lint threats

*** can we remove processes and make them metadata on flows?
"""

""" A leaf with edges has a child leaf that contains x, y, width, and height -
we want to flatten this onto the leaf itself
"""


def parse_user_object(leaf):
    leaf_list = [e for e in leaf.iter()]
    leaf.attrib['geometry'] = leaf_list[2].attrib
    if 'Z' in leaf.attrib.get('label'):
        leaf.attrib['element_type'] = 'zone'
    else:
        leaf.attrib['element_type'] = 'stride block'
    return leaf


def get_edges(leaf):
    iter = leaf.iter()
    next(iter)  # first element of an iterator is itself, you idiot. you moron.
    return next(iter).attrib


# holy shit this function is gross af but idc about cleaning it up right now
def parse_node(leaf):
    if leaf.attrib.get('style') == entity_style:
        leaf.attrib['element_type'] = 'entity'
        leaf.attrib['geometry'] = get_edges(leaf)
        leaf.attrib['sources'] = []
        leaf.attrib['sinks'] = []
    elif leaf.attrib.get('style') == process_style:
        leaf.attrib['element_type'] = 'process'
        leaf.attrib['sources'] = []
        leaf.attrib['sinks'] = []
        leaf.attrib['geometry'] = get_edges(leaf)
    elif leaf.attrib.get('style') == data_store_style:
        leaf.attrib['element_type'] = 'data store'
        leaf.attrib['geometry'] = get_edges(leaf)
        leaf.attrib['sources'] = []
        leaf.attrib['sinks'] = []
    else:
        leaf.attrib['element_type'] = 'flow'
    return leaf


def intersects(leaf, node):
    # leafs are floating and might intersect with a node
    # left side is x, right side is x+width
    # top is y, bottom is y+height
    try:
        leaf_points = leaf.attrib['geometry']
        node_points = node.attrib['geometry']

        leaf_bottom = int(leaf_points['y']) + int(leaf_points['height'])
        leaf_top = int(leaf_points['y'])
        leaf_left = int(leaf_points['x'])
        leaf_right = int(leaf_points['x']) + int(leaf_points['width'])

        node_bottom = int(node_points['y']) + int(node_points['height'])
        node_top = int(node_points['y'])
        node_left = int(node_points['x'])
        node_right = int(node_points['x']) + int(node_points['width'])

        # if leaf.attrib.get('element_type') == 'stride block':
        #     pdb.set_trace()

        if node_top > leaf_bottom or node_bottom < leaf_top:
            return False
        if node_right < leaf_left or leaf_right < node_left:
            return False

        return True
    except KeyError:
        return False


def get_leaves():
    root = et.parse('test.xml').getroot()
    leaves = []
    lim = []
    for i in root.iter():
        lim.append(i)

    for leaf in lim:
        if leaf.tag == 'UserObject':
            leaves.append(parse_user_object(leaf))
        if leaf.tag == 'mxCell':
            if leaf.attrib.get('id') == '0' or leaf.attrib.get('id') == '1':
                pass
            else:
                leaves.append(parse_node(leaf))
    # at this point, leaves contains all the nodes we need, plus flows and user elements
    # we need to iterate over the list - if an element is a node, find if any flows use it
    # as a source or a sink

    for leaf in leaves:
        if leaf.attrib.get('element_type') in ['entity', 'process', 'data store']:
            # it's something that might be a source or a sink
            for flow in leaves:
                if flow.attrib.get('source') == leaf.attrib.get('id'):
                    leaf.attrib['sources'].append(flow.attrib.get('id'))
                if flow.attrib.get('target') == leaf.attrib.get('id'):
                    leaf.attrib['sinks'].append(flow.attrib.get('id'))
        if leaf.attrib.get('element_type') in ['zone', 'stride block']:
            # it's a floating user element and we need to figure out what it intersects
            # with to attach it.
            for elem in leaves:
                if leaf.attrib.get('id') != elem.attrib.get('id') and intersects(leaf, elem):
                    if leaf.attrib.get('element_type') == 'zone':
                        elem.attrib['zone'] = leaf.attrib.get('label')
                    if leaf.attrib.get('element_type') == 'stride block':
                        elem.attrib['stride block'] = leaf.attrib.get('label')

    ## next steps are:
    # connect flows between entities and add process as metadata to flow
    # make output more readable
    # lint the stride threats based on rules
    # consider how to ingest output into snowhouse

    # KNOWN BUGS: YOU HAVE TO MAKE SURE A FLOW GOES TO AN ENTITY AND NOT A STRIDE BLOCK
    # KNOWN BUGS: FLOW PARSING IS NOT GREAT

    return leaves


def main():
    parsed_tree = get_leaves()
    for leaf in parsed_tree:
        print(leaf.attrib)


if __name__ == "__main__":
    main()
