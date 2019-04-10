from pymodm import CharField, ReferenceField, ListField, \
    IntegerField, BooleanField, DateTimeField, ObjectIdField, FloatField
from pymodm.connection import connect
from pymodm import MongoModel
from app import app

connect(app.config['MONGODB_URL'])


class CATEGORY(MongoModel):
    name = CharField()
    delete = BooleanField()

    class Meta:
        collection_name = 'category'
        final = True


class TYPE(MongoModel):
    name = CharField()
    category = ReferenceField(CATEGORY)
    delete = BooleanField()

    class Meta:
        collection_name = 'type'
        final = True


class PROJECT(MongoModel):
    creator = ObjectIdField()
    title = CharField()
    description = CharField()
    requirement = CharField()
    material = CharField()
    reference = CharField()
    tag = ReferenceField(TYPE)
    image = CharField()
    labs = ListField()
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
