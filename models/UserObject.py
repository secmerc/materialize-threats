from .GraphObj import GraphObj


class UserObject(GraphObj):
    ZONE = 'zone'
    ZONE_PREFIX = 'z'
    ZONE_INDEX = 1

    TYPE = 'type'
    LABEL = 'label'


    def __init__(self, xml, label, sid=None, gid=None, value=None):
        super(UserObject, self).__init__(sid, gid, value)
        self.xml = xml

    def text_to_mx_value(self):
        value = ""
        last_text = len(self.texts) - 1
        for i, t in enumerate(self.texts):
            style = t.get_mx_style()
            value += "<p style='" + style + "'>" + t.text + "</p>"
            if i != last_text:
                value += "<hr size='1'/>"
        return value
    
    def get_trust_zone(self):
        zone = self.xml.get(self.ZONE)  
        return zone
    
    def set_trust_zone(self, zone):
        return self.xml.set(self.ZONE, zone)

    def get_object_type(self):
        return self.xml.get(self.TYPE)

class ZoneObject(UserObject):
    def __init__(self, xml, label):
        super(ZoneObject, self).__init__(xml, label)
    
    def get_trust_zone(self):
        zone = self.xml.get(self.LABEL)
        return zone.lower().split(self.ZONE_PREFIX)[self.ZONE_INDEX]

