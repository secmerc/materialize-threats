import pytest, io

from materialize_threats.materialize import ThreatMaterializer
from materialize_threats.mx.utils import MxUtils
from materialize_threats.db import dbgraph
from materialize_threats.gherkin_stride import create_gherkins_from_threats, create_feature_file_for_gherkins

def test_materialize():
    DIAGRAM_FILE_CONTENTS = '<mxfile host="Electron" modified="2020-06-14T23:15:16.465Z" agent="5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/13.0.1 Chrome/80.0.3987.163 Electron/8.2.1 Safari/537.36" etag="IN-Iz_mcs6xnJd7p4Jyn" version="13.0.1" type="device"><diagram id="ONy8Yiw1vq8pj1ndpYMv" name="Page-1">5VjbcpswEP0aP6bDxcb4MXWctDPtNG2mzeVNNmtQKktUyPHl67sCEQQkhKRx25n4xezR6sLZs7uyB/50tT2TJE0+iwjYwHOi7cA/GXieN554+KWRXYG44dgpkFjSyGAVcEH3YMDSbU0jyGqOSgimaFoHF4JzWKgaRqQUm7rbUrD6rimJoQVcLAhro5c0UkmBhiOnwj8AjZNyZ9cxIytSOhsgS0gkNhbkzwb+VAqhiqfVdgpMs1fyUsw7fWT0/mASuOoz4df1zfr27Os+/TjehyS4uwymcOSa+GRqV74xREiAMYVUiYgFJ2xWoe+lWPMI9LIOWpXPJyFSBF0Eb0GpnYkmWSuBUKJWzIzClqor6/laL/VuZKyTrVk5N3alwZXcXdmGNUub1bTcKue1aTLMZWItF9DBzcTIjcgYVBeHJsCaOGsHE4UzECvAA6GDBEYUvasrixiBxvd+VQzxwYQxN79nIL/Mb7XM8Vi7tAwYV1QV8xxG5sAKeGbBnRqYWKc1mrHkUA/2JqEKLlKSE7fBnK8H9lGy70Aq2HayY0aP3CA0hJqacTQugU2VgW6ZVomVfYHzbE7RtGjtojmVYgFZ1uL53Ma7k83pZBoBrGrwNMskS4tSt6RbHZnXoX04btI+adMePsB6eEjWI6JITpOQ0KL+pDXYzb/byT8W6HxX5FFRwr7hUQiPWY+AMFgqkyDS8KKfl5SxqWBCos0Fh9eKlDdsRir4qwnSs7UMzZsRtjYMt3sNj451k0ZrwUiW0QVylGHFVW3Y4nspuCqJHXj+6amPnz/oES/pRy/vK2W/eLqxuD0bixX20QNRL7He/cfscC4oV7US4TaEFzRzv3h5M9G+jLTW8oOmiP3GWgU/rbVyfd6//DP6pJLrTCN7nYrNUnJTXugYJnmCt0SQ9ZsjJyuzzg8iKZmzXhVn1FlxMONVXdmZkuInWNoOvbkfBI1igng0gjAa6mbAaMx1oqAOAQff60pC8QJ7bAZWNIoeLWICvZcsz7QE/YC/Vo0aTXo0cf8BsXqH7Cb/QgLBW5XAcDh6+kLxn0lgchAJjN+qBHrdVA4nAYSq39dF36j+pvBnvwE=</diagram></mxfile>'
    EXPECTED_FEATURE_FILE_CONTENTS = '\nFeature: test\n\nScenario: Tampering\n    Given Process causes data to flow from less trusted Entity in 0 to more trusted Data store in 9\n    When Entity modifies or otherwise tampers with data related to Process\n    Then treat all input as malcious and handle it safely by ...\n\n# Mitigation details\n# https://github.com/OWASP/ASVS/blob/master/4.0/en/0x18-V10-Malicious.md\n\nScenario: Elevation of Privilege\n    Given Process causes data to flow from less trusted Entity in 0 to more trusted Data store in 9\n    When Entity attempts to gain addition capabilities without authorization related to Process\n    Then ensure acces control is enforced by ...\n\n# Mitigation details\n# https://github.com/OWASP/ASVS/blob/master/4.0/en/0x12-V4-Access-Control.md\n'

    diagram = io.StringIO(DIAGRAM_FILE_CONTENTS)
    graph = MxUtils.parse_from_xml(file=diagram)
    zones = dbgraph.get_node_trust_zones_from_graph(graph)
    dbgraph.load_graph_into_db(graph, zones)

    threats = ThreatMaterializer.get_flows_with_threats()

    gherkin_candidates = create_gherkins_from_threats(threats)
    feature_file = create_feature_file_for_gherkins('test', gherkin_candidates)
    
    assert feature_file == EXPECTED_FEATURE_FILE_CONTENTS