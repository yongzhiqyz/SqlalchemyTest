from sqlalchemy import create_engine, text, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Table
from sqlalchemy.orm import sessionmaker, relationship, aliased, subqueryload, contains_eager, joinedload
from sqlalchemy.sql import func, exists


engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()

class User(Base):
         __tablename__ = 'users'
         id = Column(Integer, primary_key=True)
         name = Column(String)
         fullname = Column(String)
         password = Column(String)
         def __repr__(self):
             return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

class Address(Base):
         __tablename__ = 'addresses'
         id = Column(Integer, primary_key=True)
         email_address = Column(String, nullable=False)
#         family_address = Column(String, nullable=False)
         user_id = Column(Integer, ForeignKey('users.id'))
         user = relationship("User", back_populates="addresses")
         def __repr__(self):
             return "<Address(email_address='%s')>" % self.email_address


User.addresses = relationship("Address", order_by=Address.id, back_populates="user")             

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


jack = User(name='jack', fullname='Jack Bean', password='gjffdd')

print jack.addresses

jack.addresses = [Address(email_address='jack@google.com'), Address(email_address='j25@yahoo.com')]
#jack.addresses = [Address(family_address='jack@google.com'), Address(family_address='j25@yahoo.com')]

print '-------------------------------------------'
print jack.addresses
print ('-----email_address-----', jack.addresses[1].email_address)

session.add(jack)
session.commit()
jack = session.query(User).filter_by(name='jack').one()
print ('-----user.id------', jack.addresses[1].user_id)
ad=session.query(Address).first()
print ad.email_address

for u, a in session.query(User, Address).filter((User.id==Address.user_id) & (Address.email_address=='jack@google.com')).all():
#for u, a in session.query(User, Address).filter(User.id==Address.user_id).filter(Address.email_address=='jack@google.com').all():
    print ('----User--------', u)
    print ('----Address-----', a)

for u in session.query(User).join(Address).\
             filter(Address.email_address=='jack@google.com').\
             all():
    print ('-----User-------', u)
          
adalias1 = aliased(Address)
adalias2 = aliased(Address)
for username, email1, email2 in \
     session.query(User.name, adalias1.email_address, adalias2.email_address).\
     join(adalias1, User.addresses).\
     join(adalias2, User.addresses).\
     filter(adalias1.email_address=='jack@google.com').\
     filter(adalias2.email_address=='j25@yahoo.com'):
     print  ('----username, email1, email2-----', username, email1, email2)
stmt = session.query(Address.user_id, func.count('*').\
                     label('address_count')).\
                     group_by(Address.user_id).subquery()

for u, count in session.query(User, stmt.c.address_count).\
         outerjoin(stmt, User.id==stmt.c.user_id).order_by(User.id):
             print ('------u, count-----', u, count)

stmt = session.query(Address).\
                 filter(Address.email_address != 'j25@yahoo.com').\
                 subquery()
adalias = aliased(Address, stmt)
for user, address in session.query(User, adalias).\
        join(adalias, User.addresses):
     print('----user    ------', user)
     print('----address------', address)

stmt = exists().where(Address.user_id==User.id)
for name, in session.query(User.name).filter(stmt):
    print('---name-----', name)

for name, in session.query(User.name).\
        filter(User.addresses.any()):
    print('-----name------', name)

for name, in session.query(User.name).\
    filter(User.addresses.any(Address.email_address.like('%google%'))):
    print('-----name------', name)

session.query(Address).\
        filter(~Address.user.has(User.name=='jack')).all()

jack = session.query(User).\
                options(subqueryload(User.addresses)).\
                filter_by(name='jack').one()

jack = session.query(User).\
                      options(joinedload(User.addresses)).\
                      filter_by(name='jack').one()


jacks_addresses = session.query(Address).\
                             join(Address.user).\
                             filter(User.name=='jack').\
                             options(contains_eager(Address.user)).\
                             all()

print ('------jacks-address-------', jacks_addresses)

print '--------------------------------------------------------'
session.delete(jack)
session.query(User).filter_by(name='jack').count()

print '--------------------------------------------------------'
print session.query(Address).filter(
     Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).count()

session.close()


print '----------------------New----------------------------'
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    addresses = relationship("Address", back_populates='user',
                       cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                            self.name, self.fullname, self.password)

class Address(Base):
     __tablename__ = 'addresses'
     id = Column(Integer, primary_key=True)
     email_address = Column(String, nullable=False)
     user_id = Column(Integer, ForeignKey('users.id'))
     user = relationship("User", back_populates="addresses")

     def __repr__(self):
         return "<Address(email_address='%s')>" % self.email_address

jack = session.query(User).get(1)
print ('--------jack---------', jack)
del jack.addresses[1]
session.query(Address).filter(
     Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).count()

print '----------------------------------------------'
session.delete(jack)
print ('----User-------', session.query(User).filter_by(name='jack').count())
print ('----Address----', session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).count())

post_keywords = Table('post_keywords', Base.metadata,
                      Column('post_id', ForeignKey('posts.id'), primary_key=True),
                      Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
)

class BlogPost(Base):
     __tablename__ = 'posts'

     id = Column(Integer, primary_key=True)
     user_id = Column(Integer, ForeignKey('users.id'))
     headline = Column(String(255), nullable=False)
     body = Column(Text)

     # many to many BlogPost<->Keyword
     keywords = relationship('Keyword',
                             secondary=post_keywords,
                             back_populates='posts')

     def __init__(self, headline, body, author):
         self.author = author
         self.headline = headline
         self.body = body

     def __repr__(self):
         return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)


class Keyword(Base):
     __tablename__ = 'keywords'

     id = Column(Integer, primary_key=True)
     keyword = Column(String(50), nullable=False, unique=True)
     posts = relationship('BlogPost',
                          secondary=post_keywords,
                          back_populates='keywords')

     def __init__(self, keyword):
         self.keyword = keyword

BlogPost.author = relationship(User, back_populates="posts")
User.posts = relationship(BlogPost, back_populates="author", lazy="dynamic")


Base.metadata.create_all(engine)


print ('----------create new engine------------')
wendy = session.query(User).\
                 filter_by(name='wendy').\
                 first()
print ('-------wendy-------', wendy)
post = BlogPost("Wendy's Blog Post", "This is a test", wendy)
session.add(post)

post.keywords.append(Keyword('wendy'))
post.keywords.append(Keyword('firstpost'))

session.query(BlogPost).\
             filter(BlogPost.keywords.any(keyword='firstpost')).\
             all()
print ('------wendy-----', session.query(BlogPost).\
             filter(BlogPost.author==wendy).\
             filter(BlogPost.keywords.any(keyword='firstpost')).\
             all())


#wendy.posts.\
#         filter(BlogPost.keywords.any(keyword='firstpost')).\
#         all()










































