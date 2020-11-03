import json, argparse, os
from .db import Node, Edge, dbgraph
from .mx.utils import MxUtils
from .gherkin_stride import create_gherkins_from_threats, create_feature_file_for_gherkins



class ThreatMaterializer(object):

    @classmethod
    def get_flows_with_threats(cls):

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

    @classmethod
    def output_threats(cls, threats):
        print(
            json.dumps(threats, indent=4)
        )

    @classmethod
    def materialize(cls):

        args = argparse.ArgumentParser(description="Enumerate STRIDE threats from a data flow diagram and create test case stubs")
        args.add_argument(
            "--diagram",
            default="samples/sample.drawio",
            type=argparse.FileType('r'),
            help="The draw.io data flow diagram filename"
        )
        filename = args.parse_args().diagram.name

        args.add_argument(
            "--featurefile",
            default=os.path.basename(filename) + ".feature",
            type=argparse.FileType('w+'),
            help="The feature filename to write"
        )

        graph = MxUtils.parse_from_xml(file=args.parse_args().diagram)
        zones = dbgraph.get_node_trust_zones_from_graph(graph)
        dbgraph.load_graph_into_db(graph, zones)

        threats = cls.get_flows_with_threats()

        gherkin_candidates = create_gherkins_from_threats(threats)
        feature_file = create_feature_file_for_gherkins(feature=filename, gherkins=gherkin_candidates)

        args.parse_args().featurefile.write(feature_file)

        cls.output_threats(threats)

