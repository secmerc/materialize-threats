from ..models.Curve import Curve


class CurveFactory:
    def __init__(self, coords):
        super(CurveFactory, self).__init__()
        self.coords = coords

    def from_xml(self, xml):
        geometry = xml.find('mxGeometry')
        points = geometry.findall('mxPoint')

        start = 0
        end = 0

        for point in points:
            x = float(point.get('x'))
            y = float(point.get('y'))
            
            if point.get('as') == 'sourcePoint':
                start = complex(x, y)
            elif point.get('as') == 'targetPoint':
                end = complex(x, y)

        
        return Curve(start=start, end=end, cb=None)