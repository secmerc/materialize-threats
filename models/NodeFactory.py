
from materialize_threats.shapes.Rect import Rect
from .Node import Node
from .Text import Text


class NodeFactory:
    def __init__(self, coords):
        super(NodeFactory, self).__init__()
        self.coords = coords

    def from_xml(self, xml, value):
        texts = []
        texts.append(Text.from_xml(xml.get('style')))
    
        return Node(
            sid=xml.get('id'),
            gid=xml.get('parent'),
            value=value,
            rect=Rect(
                x=int(xml.find('mxGeometry').get('x')),
                y=int(xml.find('mxGeometry').get('y')),
                width=int(xml.find('mxGeometry').get('width')),
                height=int(xml.find('mxGeometry').get('height'))
            ),
            texts=texts,
            fill=None,
            stroke=None
        )