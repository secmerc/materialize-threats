from . import db, Node, Edge, dbgraph
from ..mx.models.UserObject import UserObject

def node_is_user_object(node):
    value = node.value
    if (value is not None) and (type(value) == UserObject):
        return True
    return False

def get_node_trust_zones_from_graph(graph):
    zones = dict()
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

        node_type = UserObject.infer_type_from_node(node)

        for orphan in orphans:
            zone = None
            orphan = graph.get_node_by_sid(orphan)


            outer_rect = node.rect
            inner_rect = orphan.rect

            # here, both the element node and zone node could be wrapped user objects
            if outer_rect.is_overlapping(inner_rect):

                # maybe using our shape library
                if node_is_user_object(node) and node_is_user_object(orphan):
                    assert(orphan.value.get_object_type() == 'trust zone')
                    zone = orphan.value.get_trust_zone()

                # using the built-in shape library
                else:
                    zone = UserObject.get_trust_zone_from_node_label(orphan.value)

            if zone is not None:
                zones[node] = zone
                print("found {} {} inside {} {}".format(zones[node], orphan.sid, node.label, node.sid))

    return zones

def load_graph_into_db(graph, zones):
    flows = graph.edges.copy()

    remove_flow = lambda flow: flows.remove(flow)

    # we only care about things that are connected, so we start by traversing all of the edges in the graph
    for flow in flows:
        SOURCE = 0
        DESTINATION = 1

        source = graph.nodes[flow.fr]
        destination = graph.nodes[flow.to]

        # Processes get special treatment in our scheme. They represent metadata about a given flow
        process = None

        pair = []

        for node in (source, destination):
            print("inspecting {} {}".format(node.label, node.sid))
            element_type = None

            if node_is_user_object(node):
                element_type = node.value.get_object_type()
            else:
                element_type = UserObject.infer_type_from_node(node)

            if element_type == 'process':
                try:
                    process = Node().create(
                        zone=zones[node],
                        label=node.label,
                        identifier=node.sid,
                        data='test',
                        type=element_type
                    )
                except:
                    print(f"Looks like {node.label} is missing something; does it have a trust zone?")
                    exit()

                if node == source:
                    print("fix up source {} {}".format(node.label, node.sid))

                    inbound_flow, inbound_node = [(flow, flow.fr) for flow in flows if flow.to == node.sid][0]
                    node = graph.nodes[inbound_node]
                    dangling_flow = inbound_flow

                else:
                    print("fix up destination {} {}".format(node.label, node.sid))

                    outbound_flow, outbound_node = [(flow, flow.to) for flow in flows if flow.fr == node.sid][0]
                    node = graph.nodes[outbound_node]
                    dangling_flow = outbound_flow

                flows.remove(flow)
                flows.remove(dangling_flow)

            if element_type is not None:
                pair.append(
                    Node().create(
                        zone=zones[node],
                        label=node.label,
                        identifier=node.sid,
                        data='test',
                        type=element_type
                    )
                )

        if element_type is not None:
            Edge.create(
                source=pair[SOURCE],
                destination=pair[DESTINATION],
                process=process,
                data='test'
            )

    return True

