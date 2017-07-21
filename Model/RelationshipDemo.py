from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased
from sqlalchemy import text
from sqlalchemy import func



engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()

class User(Base):
         __tablename__ = 'users'
         id = Column(Integer, primary_key=True)
         name = Column(String)
         fullname = Column(String)
         password = Column(String)
         def __repr__(self):
             return "<User(name='%s', fullname='%s', password='%s')>" % (
                                 self.name, self.fullname, self.password)


print User.__tablename__

Base.metadata.create_all(engine)
ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')

Session = sessionmaker(bind=engine)
session = Session()
session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first()
print our_user.name, our_user.fullname, our_user.password

print ed_user is our_user

user1=User(name='wendy', fullname='Wendy Williams', password='foobar')
user2=User(name='mary', fullname='Mary Contrary', password='xxg527')
user3=User(name='fred', fullname='Fred Flinstone', password='blah')

session.add_all([
        user1,
        user2,
        user3])
ed_user.password = 'f8s7ccs'
print '======dirty data0:    ', session.dirty
print '======new data0:    ', session.new
#our_user = session.query(User)
#print '======The number:  ', our_user.count()
user1.password = '1234'
print  '======dirty data1:    ', session.dirty
print '======new data1:    ', session.new 

for instance in session.query(User).order_by(User.id):
         print (instance.name, instance.fullname)

for name, fullname in session.query(User.name, User.fullname):
         print(name, fullname)

for fullname in session.query(User.fullname):
         print(fullname)
full_name = session.query(User.fullname)
print '=========',full_name.count()
print '=========', session.query(User.fullname).count()

for row in session.query(User, User.name).all():
        print(row.User, row.name)

for row in session.query(User.name.label('name_label')).all():
        print(row.name_label)

user_alias = aliased(User, name='user_alias')
for row in session.query(user_alias, user_alias.name).all():
        print(row.user_alias)

for u in session.query(User).order_by(User.id)[1:3]:
        print(u)

for name, in session.query(User.name).filter_by(fullname='Ed Jones'):
        print(name)
for name, in session.query(User.name).filter(User.fullname=='Ed Jones'):
        print(name)

for user in session.query(User).filter(User.name=='ed').filter(User.fullname=='Ed Jones'):
        print(user)

print '===1=====', session.query(User.name).filter(User.name.in_(
        session.query(User.name).filter(User.name.like('%ed%'))))

query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
print query.all()
print query.first()
#user = query.one()
#print user
for user in session.query(User).filter(text("id<224")).order_by(text("id")).all():
    print(user.name)

session.query(func.count(User.name), User.name).group_by(User.name).all()

session.query(func.count('*')).select_from(User).scalar()














