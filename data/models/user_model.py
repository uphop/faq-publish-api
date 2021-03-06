from sqlalchemy import Column, String, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

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