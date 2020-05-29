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
    '''
    my current idea is to store processes as
    metdata on edges. 

    A flow can consist of nodes x,y so long as neither 
    x or y are processes.

    node -> process -> node
    
    becomes

    node -[process]-> node

    This means we are implicitly deleting two edges and
    replacing it with a single edge with attached metadata.

    Now this is interesting because you can have a many to
    may relationship 

        /----> process0 --> \
    node ----> process1 -->  node
        \----> process2 --> /


                process0 --> \
    node ----> process1 -->  node


        this means that when its a process, we need to 
        simply replace the source.to with process.to and
        store the process object on the edge

    assumptions:
        * processes exist on a single flow
        * no process will participate in multiple flows
        * a process is not mandatory on every flow

        to replace it:

        1. fetch the edge whose edge.fr is process.sid
        2. fetch the node at edge.to
        3. replace destination with edge.to

        problems
        - we are inside a for loop that iterates over flows,
        so its somewhat problematic to look up and switch context
        to another flow???

    '''


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
     
    # Select all edges who recieve data from nodes in a trust zone of 0
    dos_flows = (
        Edge.select()
        .join(Node, on=(Edge.source == Node.id))
        .where(Edge.source.zone == 0)
    )
    
    return dos_flows

def main():
    graph = MxUtils.parse_from_xml(filename="materialize_threats/samples/sample.drawio")

    enrich_graph_from_zone_annotations(graph)
    load_graph_into_db(graph)

    
    threats = get_flows_with_threats(graph)
    for threat in threats:
        print("You have DoS threats from {} to {} caused by {}".format(threat.source.label, threat.destination.label, threat.process.label))
    #store_graph_and_threats(graph, threats)

    

if __name__ == "__main__":
    main()

