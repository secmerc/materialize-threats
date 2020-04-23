import urllib.parse
import materialize_threats.deflatedecompress as deflatedecompress
import base64
import io
import xml.etree.ElementTree
import sqlite3
    
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

def analyze_drawio_cells(root, cells):
    """
    <mxGraphModel dx="1001" dy="793" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
        <root>
            <mxCell id="0"/>
            <mxCell id="1" parent="0"/>
            
            <mxCell id="NMYBy3lZM14OKT5Cw64l-1" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1"> 
                <mxGeometry x="140" y="130" width="120" height="60" as="geometry"/>
            </mxCell>
            
            <mxCell id="NMYBy3lZM14OKT5Cw64l-2" value="" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;" vertex="1" parent="1">
                <mxGeometry x="330" y="150" width="80" height="80" as="geometry"/>
            </mxCell>
            
            <mxCell id="NMYBy3lZM14OKT5Cw64l-3" value="" style="shape=partialRectangle;whiteSpace=wrap;html=1;left=0;right=0;fillColor=none;" vertex="1" parent="1">
                <mxGeometry x="570" y="100" width="120" height="60" as="geometry"/>
            </mxCell>

            <mxCell id="NMYBy3lZM14OKT5Cw64l-4" value="" style="endArrow=classic;html=1;fontColor=#FF3333;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="NMYBy3lZM14OKT5Cw64l-1" target="NMYBy3lZM14OKT5Cw64l-2">
                <mxGeometry width="50" height="50" relative="1" as="geometry">
                    <mxPoint x="260" y="120" as="sourcePoint"/>
                    <mxPoint x="310" y="70" as="targetPoint"/>
                </mxGeometry>
            </mxCell>

            <mxCell id="NMYBy3lZM14OKT5Cw64l-7" value="" style="endArrow=classic;startArrow=classic;html=1;fontColor=#FF3333;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="NMYBy3lZM14OKT5Cw64l-2" target="NMYBy3lZM14OKT5Cw64l-3">
                <mxGeometry width="50" height="50" relative="1" as="geometry">
                    <mxPoint x="140" y="300" as="sourcePoint"/>
                    <mxPoint x="190" y="250" as="targetPoint"/>
                </mxGeometry>
            </mxCell>
        </root>
    </mxGraphModel>
    """
    data_flow = dict()


    from materialize_threats.mx import EdgeFactory
    from materialize_threats.mx import NodeFactory
    from materialize_threats.mx import MxGraph
    from materialize_threats.models.CoordsTranslate import CoordsTranslate
    from collections import OrderedDict


    #import pdb; pdb.set_trace()
    coords = CoordsTranslate.from_xml_transform(root)
    edgefactory = EdgeFactory.EdgeFactory(coords)
    nodefactory = NodeFactory.NodeFactory(coords)
    edges = []
    nodes = OrderedDict()

    for cell in cells:
        #if cell.get('id') == str(0) or cell.get('id') == str(1):
        #    continue
        if cell.get('edge') == str(1):
            edges.append(edgefactory.from_xml(cell))
        else:
            #import pdb; pdb.set_trace()
            nodes[cell.get('id')] = nodefactory.from_xml(cell)


    mxgraph = MxGraph.MxGraph(nodes=nodes, edges=edges)
    import pdb; pdb.set_trace()

def drawio_to_neo4j(root, cells):
    from materialize_threats.mx import EdgeFactory
    from materialize_threats.mx import NodeFactory
    from materialize_threats.mx import MxGraph
    from materialize_threats.models.CoordsTranslate import CoordsTranslate
    from collections import OrderedDict


    #import pdb; pdb.set_trace()
    edgefactory = EdgeFactory.EdgeFactory()
    nodefactory = NodeFactory.NodeFactory()
    edges = []
    nodes = OrderedDict()

    for cell in cells:
        #if cell.get('id') == str(0) or cell.get('id') == str(1):
        #    continue
        if cell.get('edge') == str(1):
            edges.append(edgefactory.from_xml(cell))
        else:
            #import pdb; pdb.set_trace()
            nodes[cell.get('id')] = nodefactory.from_xml(cell)


    mxgraph = MxGraph.MxGraph(nodes=nodes, edges=edges)
    import pdb; pdb.set_trace()


    pass

def drawio_to_mxgraph():
    dfd = None

    tree = xml.etree.ElementTree.parse("materialize_threats/samples/sample.drawio")
    root = tree.getroot()

    diagrams = root.findall('./diagram')

    for diagram in diagrams:
        tree = xml.etree.ElementTree.parse(
            decompress_diagram_to_file(diagram.text)
        )
        root = tree.getroot()
        
        cells = root.findall('./root/mxCell')
        
        analyze_drawio_cells(root, cells)
    return dfd


def main():
    drawio_to_graph()

 


if __name__ == "__main__":
    main()

