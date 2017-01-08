from mongoengine import StringField, Document, IntField, ReferenceField, ListField

from models.users.character import Character
from passlib.hash import pbkdf2_sha256


def get_user(name):
    u = User.objects.filter(name=name).first()
    if not u:
        return False
    return u


def create_user(name, password):
    if not get_user(name):
        u = User(name=name)
        u.password = password
        u.save()
        return u
    else:
        return False


class User(Document):
    name = StringField(unique=True)
    characters = ListField(ReferenceField(Character))

    role = StringField(max_length=20, required=True, default='user')
    realm = StringField(max_length=20, required=True, default='realm1')

    _password = StringField()

    def __init__(self, name, *args, **kwargs):
        Document.__init__(self, *args, **kwargs)
        self.name = name

    @property
    def password(self):
        if self._password:
            return True
        return False

    @password.setter
    def password(self, passwd):
        print('setting password')
        # password format: $pbkdf2-digest$rounds$salt$checksum
        self._password = pbkdf2_sha256.encrypt(passwd, rounds=200000, salt_size=16)

    @property
    def password_digest(self):
        return self._password.split('$')[1].split('pbkdf2-')[1]

    @property
    def password_rounds(self):
        return self._password.split('$')[2]

    @property
    def password_salt(self):
        return self._password.split('$')[3]

    @property
    def password_checksum(self):
        return self._password.split('$')[4]

    def verify(self, password):
        return pbkdf2_sha256.verify(password, self._password)

    def add_character(self, name):
        if Character.objects.filter(name=name):
            return False
        c = Character(name).save()
        self.characters.append(c)
        return c
