from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.


class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

class Question(Base):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1024))
    def __init__(self, question):
        self.question = question
    def __repr__(self):
        return '<Question (ID=%s): %s>' % (self.id, self.question)

class Response(Base):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    answer = db.Column(db.Integer)
    def __repr__(self):
        return '<Response to (Question #%s): %s>' % (self.question_id, self.answer)



# Create tables.
Base.metadata.create_all(bind=engine)
