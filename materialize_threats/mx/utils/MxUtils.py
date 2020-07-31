import xml.etree.ElementTree, io, base64, urllib.parse, collections

from ..models import MxGraph, Edge, Node

from ..io.NodeFactory import NodeFactory
from ..io.UserObjectFactory import UserObjectFactory
from ..io.EdgeFactory import EdgeFactory

from . import MxConst
from . import deflatedecompress

def is_edge(element):
    return element.get('edge') == str(1)

def is_user_object(element):
    return element.tag == MxConst.USER_OBJECT

def decode_xml_element_to_cell(element, coords):
    edgefactory = EdgeFactory(coords)
    nodefactory = NodeFactory(coords)
    userobjectfactory = UserObjectFactory()

    value = element.get('value')

    if is_edge(element):
        cell = edgefactory.from_xml(xml=element, value=None)
        return cell
        #return edgefactory.from_xml(xml=element, value=None)

    if is_user_object(element):
        value = userobjectfactory.from_xml(element)
        
        id = value.xml.get('id')
        label = value.xml.get('label')
    
        if value is not None:
            # extract the plain node it wraps, invert the relationship
            # old: userobject.node
            element = value.xml.find(MxConst.CELL)
            element.set('id', id)
            element.set('label', label)

    cell = nodefactory.from_xml(xml=element, value=value)
    return cell


def get_mxgraph_from_xml(root, elements):
    from ..shapes.CoordsTranslate import CoordsTranslate
    from collections import OrderedDict

    coords = CoordsTranslate.from_xml_transform(root)

    edges = []
    nodes = collections.OrderedDict()

    for element in elements:
        # Every mxGraph contains an existing element of id 0 and 1, skip them
        if element.get('id') == str(0) or element.get('id') == str(1):
            continue
        
        cell = decode_xml_element_to_cell(element, coords)

        if type(cell) == Edge.Edge:
            edges.append(cell)
        else:
            nodes[cell.sid] = cell

    return(MxGraph.MxGraph(nodes=nodes, edges=edges))


def decompress_diagram_to_file(compressed_diagram):
    compressed_bytes = io.BytesIO(
        base64.b64decode(compressed_diagram)
    )

    urlencoded_diagram = deflatedecompress.Decompressor.decompress_to_bytes(
        deflatedecompress.BitInputStream(compressed_bytes)
    )

    diagram_xml = urllib.parse.unquote(
        urlencoded_diagram.decode('utf-8')
    )

    return(
        io.BytesIO(
            bytes(diagram_xml, 'utf-8')
        )
    )

def parse_from_xml(file):

    tree = xml.etree.ElementTree.parse(file)
    root = tree.getroot()

    diagram = root.find(MxConst.DIAGRAM)

    tree = xml.etree.ElementTree.parse(
        decompress_diagram_to_file(diagram.text)
    )

    diagram_root = tree.getroot()
    cells = diagram_root.find(MxConst.ROOT).getchildren()
    
    return get_mxgraph_from_xml(diagram_root, cells)