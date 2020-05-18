import xml.etree.ElementTree, io, base64, urllib.parse, collections

from ..models import EdgeFactory, NodeFactory, MxGraph
from ..utils import MxConst
from .. import deflatedecompress

def decode_cell(cell):
    value = None

    if cell.tag == MxConst.USER_OBJECT:
        value = cell
        id = value.get('id')
    
    if value is not None:
        cell = value.find(MxConst.CELL)
        cell.set('id', id)

    return cell, value

def get_mxgraph_from_xml(root, cells):
    from materialize_threats.shapes.CoordsTranslate import CoordsTranslate
    from collections import OrderedDict

    coords = CoordsTranslate.from_xml_transform(root)

    edgefactory = EdgeFactory.EdgeFactory(coords)
    nodefactory = NodeFactory.NodeFactory(coords)

    edges = []
    nodes = collections.OrderedDict()

    for cell in cells:
        if cell.get('id') == str(0) or cell.get('id') == str(1):
            continue
        
        cell, value = decode_cell(cell)

        if cell.get('edge') == str(1):
            edges.append(edgefactory.from_xml(cell, value))
        else:
            nodes[cell.get('id')] = nodefactory.from_xml(cell, value)

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

def parse_from_xml(filename):

    tree = xml.etree.ElementTree.parse(filename)
    root = tree.getroot()

    diagram = root.find(MxConst.DIAGRAM)

    tree = xml.etree.ElementTree.parse(
        decompress_diagram_to_file(diagram.text)
    )

    diagram_root = tree.getroot()
    cells = diagram_root.find(MxConst.ROOT).getchildren()
    
    return get_mxgraph_from_xml(diagram_root, cells)