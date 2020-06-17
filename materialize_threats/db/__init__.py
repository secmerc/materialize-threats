import peewee

db = peewee.SqliteDatabase(":memory:")
    # flows, entities, processes, data store

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Element(BaseModel):
    data = peewee.CharField() # a way to store external system specific entity metadata

class Node(Element):
    identifier = peewee.CharField()
    zone = peewee.IntegerField()
    label = peewee.CharField()
    type = peewee.CharField()
    
class Edge(Element):
    source = peewee.ForeignKeyField(Node, backref='source')
    destination = peewee.ForeignKeyField(Node, backref='destination')
    
    # our graph simplifies all kinds of relationships into flows,
    # and then adds metadata to flows with processes. processes 
    # align with workflows, or user actions, that trigger data flows
    # to occur
    process = peewee.ForeignKeyField(Node, backref='process')

class Threat(BaseModel):
    classification = peewee.CharField()

db.drop_tables([Node, Edge])
db.create_tables([Node, Edge])
