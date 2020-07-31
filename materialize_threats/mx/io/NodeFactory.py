
from ..shapes.Rect import Rect
from ..models.Node import Node 
from ..models.Text import Text 
from ..models.UserObject import UserObject 
from ..utils import MxUtils


class NodeFactory:
    def __init__(self, coords):
        super(NodeFactory, self).__init__()
        self.coords = coords

    def from_xml(self, xml, value):
        texts = []
        texts.append(Text.from_xml(xml.get('style')))
        
        if type(value) == str:
            label = value
        else:
            assert(MxUtils.is_user_object(value.xml))
            label = value.label
        
        return Node(
            xml=xml,
            sid=xml.get('id'),
            gid=xml.get('parent'),
            value=value,
            rect=Rect(
                x=int(xml.find('mxGeometry').get('x')),
                y=int(xml.find('mxGeometry').get('y')),
                width=int(xml.find('mxGeometry').get('width')),
                height=int(xml.find('mxGeometry').get('height'))
            ),
            label=label,
            texts=texts,
            fill=None,
            stroke=None
        )