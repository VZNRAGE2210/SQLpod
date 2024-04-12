from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import  declarative_base 
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime
from datetime import datetime  
Base =declarative_base()

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True)
    name=Column(String(50))
    email=Column(String(50),unique=True)
    password=Column(String(64))
    create_at=Column(DateTime,default=datetime.now)
    
class Query(Base):
    __tablename__='queries'
    id=Column(Integer,primary_key=True)
    query=Column(String(255))
    user_id=Column(Integer,ForeignKey('users.id'),default=1)
    create_at=Column(DateTime,default=datetime.now)

class Response(Base):   
    __tablename__='responses'
    id=Column(Integer,primary_key=True)
    content=Column(String)
    query_id=Column(Integer,ForeignKey('queries.id'))
    create_at=Column(DateTime,default=datetime.now)

class Report(Base):
    __tablename__='reports'
    id=Column(Integer,primary_key=True)
    feedback= Column(String(50))
    user_id=Column(Integer,ForeignKey('users.id'))
    create_at=Column(DateTime,default=datetime.now)
           
def get_db():
       engine =create_engine('sqlite:///example.db')
       return sessionmaker(bind=engine)()
   
def save_to_db(object):
       db=get_db()
       db.add(object)
       db.commit()
       db.close()


if __name__ == "__main__":
    engine =create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)