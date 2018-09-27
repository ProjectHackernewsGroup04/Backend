from mongoengine import *
import datetime

connect('hackernews', host='localhost', port=27017)

# Local functions
from database import (
    get_db_conn,
    prepare_db,
    collection_name_items,
)

class User(Document):
    username = StringField(unique=True,required=True)
    password = StringField(required=True)
    delay = FloatField()
    karma = IntField(default_value=0)
    about = StringField(max_length=50)
    submitted = ListField(IntField())

class Item(Document):
    id = IntField(unique=True,required=True)
    deleted = BooleanField(default=False)
    type = StringField(required=True)
    by = StringField(required=True)
    time = DateTimeField(default=datetime.datetime.utcnow)
    text = StringField()
    dead = BooleanField(default=False)
    parent = LongField()
    poll = LongField()
    kids = ListField(IntField())
    url = StringField()
    score = IntField(default_value=0)
    title = StringField()
    parts = ListField(IntField())
    descendants = IntField(default_value=0)

def get_newest():
    print 'from odm'
    for user in User.objects:
        print '===', user.username, '==='
    print User.objects
    return User.objects



def initialize():
    if User.objects.count() == 0:
        user = User()
        user.username = "cjs"
        user.password = "hdfjsdf"
        user.save()
