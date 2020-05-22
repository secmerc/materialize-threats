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
    
   
    # TODO: would it be better to rename this function to something like contains_rectangle()?
    # TODO: extend mx library with userobject concept, being loading our metadata into the parsed objects

    # For now, orphans are assumed to be the smaller inner objects
    for node in nodes:
        node = graph.get_node_by_sid(node)

        for orphan in orphans: 
            orphan = graph.get_node_by_sid(orphan)
            assert(orphan.value.xml.get('type') == 'trust zone')
        
            outer_rect = node.rect
            inner_rect = orphan.rect
            
            if outer_rect.is_overlapping(inner_rect):
                import pdb; pdb.set_trace()
                print("found {} {} inside {} {}".format(orphan.label, orphan.sid, node.label, node.sid))
                
                node.value.set_user_nvpair("zone", orphan.value.get_user_nvpair("label"))
                print(node.value.get_user_nvpair("zone"))

if __name__ == "__main__":
    main()

