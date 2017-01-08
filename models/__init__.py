from mongoengine import *
from config import config

db = connect(
    host=config['mongodb']
)
