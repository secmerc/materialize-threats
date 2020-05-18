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
    # TODO: extend mx library with userobject concept, being loading our metadata into the parsed objects


    # For now, orphans are assumed to be the smaller inner objects
    for node in nodes:
        node = graph.get_node_by_sid(node)

        for orphan in orphans: 
            orphan = graph.get_node_by_sid(orphan)
            assert(orphan.value.get('type') == 'trust zone')
        
            outer_rect = node.rect
            inner_rect = orphan.rect
            
            if outer_rect.is_overlapping(inner_rect):
                import pdb; pdb.set_trace()
                print("found {} inside {}".format(orphan.sid, node.sid))
                
                node.set_user_nvpair("zone", orphan.get_user_nvpair("label"))
                print(node.get_user_nvpair("zone"))

if __name__ == "__main__":
    main()

