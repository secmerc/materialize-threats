import xml.etree.ElementTree, io, base64, urllib.parse, collections

from ..models import MxGraph

from ..io.NodeFactory import NodeFactory
from ..io.UserObjectFactory import UserObjectFactory
from ..io.EdgeFactory import EdgeFactory

from . import MxConst
from . import deflatedecompress

def decode_xml_element(cell):
    userobject = None

    userobjectfactory = UserObjectFactory()

    if cell.tag == MxConst.USER_OBJECT:
        userobject = userobjectfactory.from_xml(cell)
        
        id = userobject.xml.get('id')
        label = userobject.xml.get('label')
    
    if userobject is not None:
        cell = userobject.xml.find(MxConst.CELL)
        cell.set('id', id)
        cell.set('label', label)

    return cell, userobject

def get_mxgraph_from_xml(root, elements):
    from ..shapes.CoordsTranslate import CoordsTranslate
    from collections import OrderedDict

    coords = CoordsTranslate.from_xml_transform(root)

    edgefactory = EdgeFactory(coords)
    nodefactory = NodeFactory(coords)

    edges = []
    nodes = collections.OrderedDict()

    for element in elements:
        if element.get('id') == str(0) or element.get('id') == str(1):
            continue
        
        cell, userobject = decode_xml_element(element)

        if cell.get('edge') == str(1):
            edges.append(edgefactory.from_xml(cell, userobject))
        else:
            nodes[cell.get('id')] = nodefactory.from_xml(cell, userobject)

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