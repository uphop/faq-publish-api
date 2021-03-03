from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    user_id = Column(String, primary_key=True)
    name = Column(String)
    created = Column(String)
    topics = relationship("Topic", backref=backref("user"))

    def __init__(self, user_id, name, created):
        self.user_id = user_id
        self.name = name
        self.created = created

class Topic(Base):
    __tablename__ = "topic"
    topic_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user.user_id"))
    question = Column(String)
    answer = Column(String)
    created = Column(String)

    def __init__(self, topic_id, user_id, question, answer, created):
        self.topic_id = topic_id
        self.user_id = user_id
        self.question = question
        self.answer = answer
        self.created = created


