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


class IMAGE(MongoModel):
    url = CharField()
    desc = CharField()
    package = ListField()
    delete = BooleanField()

    class Meta:
        collection_name = 'image'
        final = True


class PROJECT(MongoModel):
    creator = ObjectIdField()
    title = CharField()
    description = CharField(blank=True)
    requirement = CharField(blank=True)
    material = CharField(blank=True)
    reference = CharField(blank=True)
    tag = ReferenceField(TYPE)
    image = ReferenceField(IMAGE)
    labs = ListField()
    timeConsume = CharField()
    base = ReferenceField('PROJECT', blank=True)
    # base = ReferenceField('PROJECT')
    spec = CharField()
    delete = BooleanField(default=False)
    createdAt = DateTimeField()
    updatedAt = DateTimeField()

    class Meta:
        collection_name = 'project'
        final = True


class PURCHASE(MongoModel):
    purchaser = ObjectIdField()
    limit = DateTimeField()
    project = ReferenceField(PROJECT)
    remark = CharField(blank=True)
    createdAt = DateTimeField()
    updatedAt = DateTimeField()
    delete = BooleanField(default=False)

    class Meta:
        collection_name = 'purchase'
        final = True
