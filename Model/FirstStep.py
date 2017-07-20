from sqlalchemy import *

db = create_engine('sqlite:///tutorial.db')
# open a connection to the database you'll be using

db.echo = False  # Try changing this to True and see what happens

metadata = MetaData(db)
#create the object that will manage them
#the object that manages this collection of metadata is called a MetaData object. 

users = Table('users', metadata,
              Column('user_id', Integer, primary_key=True),
              Column('name', String(40)),
              Column('age', Integer),
              Column('password', String),)

users.drop()   # you can drop the Talbe before create()
users.create()


#users = Table('users', metadata, autoload=True)   #If the users table already existed, comment the creat()

i = users.insert()
i.execute(user_id=5,name='Mary', age=30, password='secret')
i.execute({'name': 'John', 'age': 42},
          {'name': 'Susan', 'age': 57},
          {'name': 'Carl', 'age': 33})

s = users.select()
rs = s.execute()

row = rs.fetchone()    
# fetchone() and fetchall() methods. As you'd expect, fetchone() returns a single row, while fetchall() returns a list of rows. 
print 'Id:', row[0]   #pretend it's a tuple and access its columns by position
print 'type:',type(row)  #access the row as if it were a dictionary (row['name'])
print 'user_id:',row['user_id']
print 'Name:', row['name']
print 'Age:', row.age
print 'Password:', row[users.c.password]

for row in rs:
    print row.name, 'is', row.age, 'years old'    #access the columns as if they were attributes of the row object.


















#questions = Table('questions', Base.metadata,
#                  Column(id,primary_key=True),
#                  Column(user_id))



    






