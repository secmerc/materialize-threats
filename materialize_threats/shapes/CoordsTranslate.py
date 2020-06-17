class CoordsTranslate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def complex_translate(self, cnum):
        return complex(cnum.real + self.x, cnum.imag + self.y)

    def translate(self, x, y):
        return float(x) + self.x, float(y) + self.y

    @staticmethod
    def from_xml_transform(xml):
        x = xml.get('dx')
        y = xml.get('dy')
        return CoordsTranslate(x=float(x), y=float(y))
