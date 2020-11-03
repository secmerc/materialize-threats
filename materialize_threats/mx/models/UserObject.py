from .GraphObj import GraphObj


class UserObject(GraphObj):
    ZONE = 'zone'
    ZONE_PREFIX = 'z'
    ZONE_INDEX = 1

    TYPE = 'type'
    TYPES = ['process', 'entity', 'data store', 'trust zone']
    LABEL = 'label'

    texts = "none"

    def __init__(self, xml, label, sid=None, gid=None, value=None):
        super(UserObject, self).__init__(sid, gid, value)
        self.xml = xml
        self.label = label

    def text_to_mx_value(self):
        value = ""
        last_text = len(self.texts) - 1
        for i, t in enumerate(self.texts):
            style = t.get_mx_style()
            value += "<p style='" + style + "'>" + t.text + "</p>"
            if i != last_text:
                value += "<hr size='1'/>"
        return value

    @classmethod
    def get_trust_zone_from_node_label(cls, label):
        # Sometimes we pass in a UserObject instead of a label
        if type(label) != str:
            label = label.label
        if label is not None:
            try:
                zone = label.lower().split(cls.ZONE_PREFIX)[cls.ZONE_INDEX]
                zone = zone.replace('</b>', '')
                if cls._is_valid_trust_zone(zone):
                    return zone
            except:
                print(f'found unparsable object with label {label}, skipping')
                return None
        return None

    def get_trust_zone(self):

        zone = self.xml.get(self.LABEL)

        if zone is not None:
            try:
                zone = zone.lower().split(self.ZONE_PREFIX)[self.ZONE_INDEX]
            except IndexError:
                pass
            else:
                if self._is_valid_trust_zone(zone):
                    return zone

        return None

    @classmethod
    def _is_valid_trust_zone(self, zone):
        return(int(zone) <= 9)

    def set_trust_zone(self, zone):
        return self.xml.set(self.ZONE, zone)

    def get_object_type(self):
        type = self.xml.get(self.TYPE)
        if type in self.TYPES:
            return type

    @classmethod
    def infer_type_from_node(cls, node):

        TRUST_ZONE = 'text;html=1;strokeColor=#82b366;fillColor=#d5e8d4;align=center;verticalAlign=middle;whiteSpace=wrap;overflow=hidden;'
        ELEMENT = 'rounded=0;whiteSpace=wrap;html=1;'
        PROCESS = 'ellipse;whiteSpace=wrap;html=1;aspect=fixed;'
        DATA_STORE = 'shape=partialRectangle;whiteSpace=wrap;html=1;left=0;right=0;fillColor=none;'

        types = {
            'trust zone': TRUST_ZONE,
            'element': ELEMENT,
            'process': PROCESS,
            'data store': DATA_STORE

        }

        for text in node.texts:
            for key, value in types.items():
                if text.text == value:
                    return key

        return None
