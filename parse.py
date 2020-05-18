import materialize_threats.deflatedecompress as deflatedecompress
import base64
import sqlite3
import materialize_threats.utils.MxUtils as MxUtils

def main():
    graph = MxUtils.parse_from_xml(filename="materialize_threats/samples/sample.drawio")

    #find orphaned nodes
    nodes = set(graph.nodes.keys())
    edges = set()
    
    for edge in graph.edges:
        edges.add(edge.to)
        edges.add(edge.fr)

    orphans = nodes.difference(edges)
    nodes = nodes.difference(orphans)
    
    # current overlap check can only detect comparing the larger rectangle to the smaller one inside.
    # it cannot take the smaller inner rectangle and detect that its wrapped in an outer rectangle
    # TODO: would it be better to rename this function to something like contains_rectangle()?

    # For now, orphans are assumed to be the smaller inner objects
    for node in nodes:
        outer_node = graph.get_node_by_sid(node)

        for orphan in orphans: 
            orphan = graph.get_node_by_sid(orphan)
            if outer_node.rect.is_overlapping(orphan.rect):
                import pdb; pdb.set_trace()
                print("found {} inside {}".format(orphan.sid, outer_node.sid))


    

    
    #find out if they intersect any of our nodes
    #if they do, flatten the orphans into node.value

if __name__ == "__main__":
    main()

