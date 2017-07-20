from sqlalchemy import *
from sqlalchemy.orm import mapper
import sqlite3
from sqlalchemy.orm import create_session, query

db = create_engine('sqlite:///joindemo.db')

db.echo = True

metadata = MetaData(db)

users = Table('users', metadata, autoload=True)
emails = Table('emails', metadata, autoload=True)

# These are the empty classes that will become our data classes
class User(object):
    pass
class Email(object):
    pass

usermapper = mapper(User, users)
emailmapper = mapper(Email, emails)

session = create_session()



session.flush()

fred = User()
fred.name = 'Fred'
fred.age = 37

print "About to flush() without a save()..."
session.flush()  # Will *not* save Fred's data yet




