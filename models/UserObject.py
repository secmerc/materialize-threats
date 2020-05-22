from .GraphObj import GraphObj


class UserObject(GraphObj):
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

    def set_user_nvpair(self, name, value):
        return self.xml.set(name, value)

    def get_user_nvpair(self, name):
        return self.xml.get(name)

class ZoneObject(UserObject):
    def __init__(self, sid, gid, **kwargs):
        super(ZoneObject, self).__init__(sid, gid)
        #data = **kwargs
    
    def get_trust_zone(self):
        pass

