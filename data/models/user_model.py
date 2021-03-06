from sqlalchemy import Column, String, Table
from sqlalchemy.orm import relationship, backref
from data.models.meta import Base

class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True)
    name = Column(String)
    created = Column(String)
    topics = relationship("Topic", backref=backref("user"))

    def __init__(self, id, name, created):
        self.id = id
        self.name = name
        self.created = created