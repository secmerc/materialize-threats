from abc import ABC


class GraphObj(ABC):
    def __init__(self, sid, gid, value):
        self.sid = sid
        self.gid = gid
        self.value = value
    
    def get_user_object(self):
        uo_type = self.value.get('type')
        assert(
            (uo_type == 'trust zone') or
            (uo_type == 'process') or
            (uo_type == 'entity') or
            (uo_type == 'data store')
        )



    def enrich_from_graph(self, attrs):
        for e in attrs:
            self.__setattr__(e[0], e[1])
