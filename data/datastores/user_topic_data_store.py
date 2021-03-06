import os
import logging
from dotenv import load_dotenv
load_dotenv()

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models.meta import Base
from data.models.topic_model import Topic
from data.models.user_model import User

class UserTopicDataStore:
    def __init__(self):
        # init engine
        USER_TOPICS_DATASTORE_CONNECTION_STRING = os.environ.get('USER_TOPICS_DATASTORE_CONNECTION_STRING', 'sqlite:///data//datastores/local.sqlite3?check_same_thread=False')
        engine = create_engine(USER_TOPICS_DATASTORE_CONNECTION_STRING)

        # create all tables in the engine
        Base.metadata.create_all(engine)

        # bind the engine to the metadata of the Base class so that the declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine

        # init database session
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def create_user(self, id, name, created):
        # insert into data store and commit
        self.session.add(User(id=id, name=name, created=created))
        self.session.commit()

    def get_users(self):
        # select all users
        return self.session.query(User.id, User.name, User.created).all()

    def get_user_by_id(self, id):
        # select user by ID
        return self.session.query(User.id, User.name, User.created).filter(User.id == id).one_or_none()

    def get_user_by_name(self, name):
        # select user by full name
        return self.session.query(User.id, User.name, User.created).filter(User.name == name)

    def delete_user(self, id):
        # delete record from data store and commit
        self.session.query(User).filter(User.id == id).delete()
        self.session.commit()


