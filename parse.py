import materialize_threats.deflatedecompress as deflatedecompress
import base64
import materialize_threats.utils.MxUtils as MxUtils
from .db import db, Node, Edge

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

def load_graph_into_db(graph):
    flows = graph.edges.copy()

    for flow in flows:
        SOURCE = 0
        DESTINATION = 1

        source = graph.nodes[flow.fr]
        destination = graph.nodes[flow.to]
        
        process = None
        
        pair = []

        for node in (source, destination): 

            if node.value.get_object_type() == 'process':
                process = Node().create(
                    zone=node.value.get_trust_zone(),
                    label=node.label,
                    identifier=node.sid,
                    data='test',
                    type=node.value.get_object_type()
                )

                if node == source:
                    # fix up the source
                    candidates = [flow.fr for flow in flows if flow.to == node.sid]
                    assert(len(candidates) == 1)
                    node = graph.nodes[candidates[0]]
                else:
                    #fix up the destination
                    candidates = [flow.to for flow in flows if flow.fr == node.sid]
                    assert(len(candidates) == 1)
                    node = graph.nodes[candidates[0]]

                flows.remove(flow)

            pair.append(
                Node().create(
                    zone=node.value.get_trust_zone(),
                    label=node.label,
                    identifier=node.sid,
                    data='test',
                    type=node.value.get_object_type()
                )
            )

        Edge.create(
            source=pair[SOURCE],
            destination=pair[DESTINATION],
            process=process,
            data='test'
        )
    
    return True

def get_flows_with_threats(graph):
    threats = { 
        'spoofing': [],
        'tampering': [],
        'repudiation': [],
        'info_disclosure': [],
        'denial_of_service': [],
        'elevation_of_privilege': []
    }

    Source = Node.alias()
    Destination = Node.alias()


    threats['elevation_of_privilege'] = (
        Edge.select(Edge, Source.zone, Destination.zone)
        .join(Source, on=(Source.id == Edge.source))
        .switch(Destination)
        .join(Destination, on=(Destination.id == Edge.destination))
        .where(
            (Source.zone < Destination.zone)
        )
    )

    threats['spoofing'] = (
        Edge.select(Edge, Source.zone, Destination.zone)
        .join(Source, on=(Source.id == Edge.source))
        .switch(Destination)
        .join(Destination, on=(Destination.id == Edge.destination))
        .where(
            (Source.zone == 0) & 
            (Destination.zone == 1)
        )
    )

    threats['tampering'] = (
        Edge.select(Edge, Source.zone, Destination.zone)
        .join(Source, on=(Source.id == Edge.source))
        .switch(Destination)
        .join(Destination, on=(Destination.id == Edge.destination))
        .where(
            (Source.zone < Destination.zone)
        )
    )

    #repudiation
    threats['repudation'] = set(threats['spoofing']).intersection(set(threats['tampering']))


    threats['denial_of_service'] = (
        Edge.select(Edge, Source.zone, Destination.zone)
        .join(Source, on=(Source.id == Edge.source))
        .switch(Destination)
        .join(Destination, on=(Destination.id == Edge.destination))
        .where(
            (Source.zone == 0) & 
            (Destination.zone == 1)
        )
    )

    threats['information_disclosure'] = (
        Edge.select(Edge, Source.zone, Destination.zone)
        .join(Source, on=(Source.id == Edge.source))
        .switch(Destination)
        .join(Destination, on=(Destination.id == Edge.destination))
        .where(
            (Source.zone > Destination.zone)
        )
    )
    return threats

def main():
    graph = MxUtils.parse_from_xml(filename="materialize_threats/samples/sample.drawio")
    enrich_graph_from_zone_annotations(graph)
    load_graph_into_db(graph)

    threats = get_flows_with_threats(graph)
    

    for threat_class in threats.keys():
        if len(threat_class) >= 1:
            for threat in threats[threat_class]:
                print("You have {} threats from {} to {} caused by {}".format(threat_class, threat.source.label, threat.destination.label, threat.process.label))

if __name__ == "__main__":
    main()

