from pymodm import CharField, ReferenceField, ListField,\
    IntegerField, BooleanField, DateTimeField, ObjectIdField, FloatField
from pymodm.connection import connect
from pymodm import MongoModel
from app import app

connect(app.config['MONGODB_URL'])


class PROJECT(MongoModel):
    creator = ObjectIdField()
    title = CharField()
    description = CharField()
    requirement = CharField()
    material = CharField()
    reference = CharField()
    image = CharField()
    timeConsume = CharField()
    base = ReferenceField('PROJECT', blank=True)
    # base = ReferenceField('PROJECT')
    spec = CharField()
    delete = BooleanField()
    createdAt = DateTimeField()
    updatedAt = DateTimeField()

    class Meta:
        collection_name = 'project'
        final = True
