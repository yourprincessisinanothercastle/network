import argparse


import config
from models import db
from models.users.user import create_user


if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("dbname")
    parser.add_argument('--drop', default=False, action='store_true')
    parser.add_argument('--createuser', nargs=2)
    args = parser.parse_args()

    if args.drop:
        db.drop_database(args.dbname)
    if args.createuser:
        create_user(args.createuser[0], args.createuser[1])

