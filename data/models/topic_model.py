from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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