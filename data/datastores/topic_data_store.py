import os
import logging
from dotenv import load_dotenv
load_dotenv()

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models.meta import Base
from data.models.topic_model import Topic

class TopicDataStore:
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

    def create_topic(self, user_id, id, question, answer, created):
        # insert into data store and commit
        self.session.add(Topic(user_id=user_id, id=id, question=question, answer=answer, created=created))
        self.session.commit()

    def get_topics(self, user_id):
        # select all topics
        return self.session.query(Topic.user_id, Topic.id, Topic.question, Topic.answer, Topic.created).filter(Topic.user_id == user_id)

    def get_topic_by_id(self, user_id, id):
        # select user by ID
        return self.session.query(Topic.user_id, Topic.id, Topic.question, Topic.answer, Topic.created).filter(Topic.user_id == user_id, Topic.id == id).one_or_none()

    def delete_topic(self, user_id, id):
        # delete record from data store and commit
        self.session.query(Topic).filter(Topic.user_id == user_id, Topic.id == id).delete()
        self.session.commit()


