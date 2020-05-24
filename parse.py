import materialize_threats.deflatedecompress as deflatedecompress
import base64
import sqlite3
import materialize_threats.utils.MxUtils as MxUtils

def main():
    graph = MxUtils.parse_from_xml(filename="materialize_threats/samples/sample.drawio")

    nodes = set(graph.nodes.keys())    
    edges = set()
    for edge in graph.edges:
        edges.add(edge.to)
        edges.add(edge.fr)
    
    orphans = nodes.difference(edges)
    nodes = nodes.difference(orphans)
    
    # For now, orphans are assumed to be the smaller inner objects
    for node in nodes:
        node = graph.get_node_by_sid(node)

        for orphan in orphans: 
            orphan = graph.get_node_by_sid(orphan)
            assert(orphan.value.xml.get('type') == 'trust zone')
        
            outer_rect = node.rect
            inner_rect = orphan.rect
            
            if outer_rect.is_overlapping(inner_rect):
                print("found {} {} inside {} {}".format(orphan.label, orphan.sid, node.label, node.sid))
                
                node.value.set_user_nvpair("zone", orphan.value.get_user_nvpair("label"))
                print(orphan.value.get_trust_zone())

if __name__ == "__main__":
    main()

