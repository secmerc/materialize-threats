import base64, json, peewee, argparse, os
from materialize_threats.db import db, Node, Edge
from materialize_threats.mx.utils import MxUtils
from materialize_threats.gherkin_stride import create_gherkins_from_threats

"""
https://docs.microsoft.com/en-us/archive/blogs/larryosterman/threat-modeling-again-presenting-the-playsound-threat-model
"""

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

                """
                before fixup:
                [entity]--->(process)--->[entity]
                
                after fixup:
                [entity]--_-->[entity]
                          ^ (process stored as metadata)
                """
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

    SPOOFING = 'spoofing'
    TAMPERING = 'tampering'
    REPUDIATION = 'repudiation'
    INFORMATION_DISCLOSURE = 'informationDisclosure'
    DENIAL_OF_SERVICE = 'denialOfService'
    ELEVATION_OF_PRIVILEGE = 'elevationOfPrivilege'

    SOURCE = 'source'
    SOURCE_ZONE = 'sourceZone'
    DESTINATION = 'destination'
    DESTINATION_ZONE =  'destinationZone'
    PROCESS = 'process'

    threats = { 
        SPOOFING: [],
        TAMPERING: [],
        REPUDIATION: [],
        INFORMATION_DISCLOSURE: [],
        DENIAL_OF_SERVICE: [],
        ELEVATION_OF_PRIVILEGE: []
    }

    Source = Node.alias()
    Destination = Node.alias()
    Process = Node.alias()

    edgequery = (
        Edge.select(
            Source.label.alias(SOURCE), 
            Source.zone.alias(SOURCE_ZONE),
            Destination.label.alias(DESTINATION), 
            Destination.zone.alias(DESTINATION_ZONE),
            Process.label.alias(PROCESS)
        )
        .join(Source, on=(Source.id == Edge.source))
        .switch(Process)
        .join(Process, on=(Process.id == Edge.process))
        .switch(Destination)
        .join(Destination, on=(Destination.id == Edge.destination))
    ) 

    threats[ELEVATION_OF_PRIVILEGE] = list(
        edgequery.where(
            (Source.zone < Destination.zone)
        ).dicts()
    )

    threats[SPOOFING] = list(
       edgequery.where(
            (Source.zone == 0) & 
            (Destination.zone == 1)
        ).dicts()
    )

    threats[TAMPERING] = list(
        edgequery.where(
            (Source.zone < Destination.zone)
        ).dicts()
    )

    threats[REPUDIATION] = [threat for threat in threats[SPOOFING] if threat in threats[TAMPERING]]

    threats[DENIAL_OF_SERVICE] = list(
        edgequery.where(
            (Source.zone == 0) & 
            (Destination.zone == 1)
        ).dicts()
    )

    threats[INFORMATION_DISCLOSURE] = list(
        edgequery.where(
            (Source.zone > Destination.zone)
        ).dicts()
    )

    return threats

def output_threats(threats):
    print(
        json.dumps(threats, indent=4)
    )

def main():

    args = argparse.ArgumentParser(description="Enumerate STRIDE threats from a data flow diagram")
    args.add_argument(
        "--filename", 
        default="samples/sample.drawio",
        type=argparse.FileType('r'), 
        help="The draw.io filename containing the data flow diagram")

    graph = MxUtils.parse_from_xml(filename=args.parse_args().filename)
    enrich_graph_from_zone_annotations(graph)
    load_graph_into_db(graph)

    threats = get_flows_with_threats(graph)
    gherkin_candidates = create_gherkins_from_threats(threats) 
    
    for gherkin in gherkin_candidates:
        print(gherkin)
    
    #suggest_gherkins_for_candidates()
    output_threats(threats)
    

if __name__ == "__main__":
    main()

