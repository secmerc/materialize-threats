import string
from gherkin.token_scanner import TokenScanner
from gherkin.token_matcher import TokenMatcher
from gherkin.parser import Parser
from gherkin.errors import ParserError, CompositeParserException

from .templates import Base, Scenarios

def create_gherkins_from_threats(threats):
    scenarios = Scenarios.stride

    gherkins = list()
   
    for threat_class in threats:
        for threat in threats[threat_class]:

            threat_gherkin = scenarios[threat_class].substitute(
                process = threat['process'],
                source = threat['source'],
                sourceZone = threat['sourceZone'],
                destination = threat['destination'],
                destinationZone = threat['destinationZone']
            )

            parser = Parser()
            feature_base = Base.feature_base

            try:
                parser.parse(
                    TokenScanner(
                        feature_base.substitute(
                            component="None",
                            scenario=threat_gherkin
                        )
                    )
                )
            except CompositeParserException:
                print("Invalid gherkin template created: {}".format(threat_gherkin))
            else:
                gherkins.append(threat_gherkin)
    
    return gherkins

def create_feature_file_for_gherkins(feature, gherkins):
    feature_file = Base.feature_bare.substitute(component=feature)
    for gherkin in gherkins:
        feature_file += gherkin

    Parser().parse(
        TokenScanner(feature_file)
    )
    return feature_file