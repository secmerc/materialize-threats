from ..models.UserObject import UserObject


class UserObjectFactory:
    ZONE_OBJ = 'trust zone'

    def __init__(self):
        super(UserObjectFactory, self).__init__()

    def from_xml(self, xml):
        #uo_type = xml.get('type')


        """
        TODO: 
        Deprecate zone objects, just let them be user objects
        """
        #if uo_type == self.ZONE_OBJ:
        #   return ZoneObject(xml=xml, label=xml.get('label'))
        #else:
        return UserObject(xml=xml, label=xml.get('label'))

    def from_node(self, node):
        pass