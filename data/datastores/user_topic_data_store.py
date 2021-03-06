import os
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from data.models.topic_model import Topic
from data.models.user_model import User
import logging

class UserTopicDataStore:
    def __init__(self):
        self.datastore_connection_string = os.environ.get('USER_TOPICS_DATASTORE_CONNECTION_STRING', 'sqlite:///data//datastore/user_topics_local.sqlite3')
        self.init_datastore()
        
    def init_datastore(self):
        engine = create_engine(self.datastore_connection_string)

        # Create all tables in the engine. This is equivalent to "Create Table"
        # statements in raw SQL.
        Base = declarative_base()
        Base.metadata.create_all(engine)

        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        self.session = DBSession()

    def create_user(self, id, name, created):
        # insert into data store and commit
        self.session.add(User(user_id=id, name=name, created=created))
        self.session.commit()

    def get_users(self):
        # select all users
        return self.session.query(User.name, User.created).all()

    def get_user(self, id):
        # select user by ID
        return self.session.query(User.name, User.created).filter(User.user_id == id).one_or_none()

    def delete_user(self, id):
        # check if user exists
        user = self.get_user(id)

        # if yes, drop that
        if not user is None:
            self.session.query(User).filter(User.user_id == id).delete()
            self.session.commit()
            return id
