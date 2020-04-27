import materialize_threats.deflatedecompress as deflatedecompress
import base64
import sqlite3
import materialize_threats.mx.MxUtils as MxUtils


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

def main():
    MxUtils.parse_xml()

if __name__ == "__main__":
    main()

