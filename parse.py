import materialize_threats.deflatedecompress as deflatedecompress
import base64
import sqlite3
import materialize_threats.utils.MxUtils as MxUtils

def enrich_graph_from_zone_annotations(graph):
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
            
            assert(orphan.value.get_object_type() == 'trust zone')
        
            outer_rect = node.rect
            inner_rect = orphan.rect
            
            if outer_rect.is_overlapping(inner_rect):
                print("found {} {} inside {} {}".format(orphan.value.get_trust_zone(), orphan.sid, node.label, node.sid))
                node.value.set_trust_zone(
                    orphan.value.get_trust_zone()
                )
                print("Set {} on {} {}".format(node.value.get_trust_zone(), node.label, node.sid))
    
    return orphans

def analyze_graph_flows_for_threats(graph):
    
    flows = graph.edges.copy()
    
    threats = dict()

    for flow in flows:

        source = graph.nodes[flow.fr]
        source_zone = int(source.value.get_trust_zone())
        
        destination = graph.nodes[flow.to]
        destination_zone = int(destination.value.get_trust_zone())

        if not destination in threats:
            threats[destination] = list()
        if not source in threats:
            threats[source] = list()
    
        if source_zone == 0 and destination_zone >= 1:                
            print("{} recieves D from {}".format(destination.label, source.label))
            threats[destination].append("D")    


def main():
    graph = MxUtils.parse_from_xml(filename="materialize_threats/samples/sample.drawio")

    enrich_graph_from_zone_annotations(graph)
    threats = analyze_graph_flows_for_threats(graph)

    

if __name__ == "__main__":
    main()

