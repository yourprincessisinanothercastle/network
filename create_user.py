import sys

import config
from models.users.user import create_user, User


user = sys.argv[1]
pw = sys.argv[2]

print('creating user %s with pw %s' % (user, pw))

create_user(name=user, password=pw)
u = User.objects.filter(name=user).first()

print(u._password)

print("done!")

