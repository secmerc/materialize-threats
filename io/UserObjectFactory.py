from ..models.UserObject import UserObject


class UserObjectFactory:
    def __init__(self):
        super(UserObjectFactory, self).__init__()

    def from_xml(self, xml):
        import pdb; pdb.set_trace()

        return UserObject(xml=xml, label=xml.get('label'))