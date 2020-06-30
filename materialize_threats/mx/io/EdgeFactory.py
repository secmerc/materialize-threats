from ..io.CurveFactory import CurveFactory
from ..models.Edge import Edge


class EdgeFactory:
    def __init__(self, coords):
        super(EdgeFactory, self).__init__()
        self.curve_factory = CurveFactory(coords)

    def from_xml(self, xml, value):
        return Edge(
            sid=xml.get('id'),
            gid=xml.get('parent'),
            value=value,
            fr=xml.get('source'),
            to=xml.get('target'),
            curve=self.curve_factory.from_xml(xml)
        )