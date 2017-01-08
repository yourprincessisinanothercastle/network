from mongoengine import StringField, Document, IntField, ReferenceField, ListField, dereference

class Character(Document):
    name = StringField(unique=True)

    def __init__(self, name, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)
        self.name = name