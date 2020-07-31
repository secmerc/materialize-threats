from .GraphObj import GraphObj


class Node(GraphObj):
    def __init__(self, xml, sid, gid, value, label, rect, texts, fill, stroke):

        super(Node, self).__init__(sid, gid, value)

        self.xml = xml
        self.rect = rect
        self.texts = texts
        self.fill = fill
        self.stroke = stroke
        self.label = label
        self.shape = None

    def get_value(self, name):
        return self.xml.get(name)

    def set_value(self, name, value):
        return self.xml.set(name, value)
    
    def text_to_mx_value(self):
        value = ""
        last_text = len(self.texts) - 1
        for i, t in enumerate(self.texts):
            style = t.get_mx_style()
            value += "<p style='" + style + "'>" + t.text + "</p>"
            if i != last_text:
                value += "<hr size='1'/>"
        return value
