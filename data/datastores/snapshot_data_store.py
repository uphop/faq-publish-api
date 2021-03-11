import os
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models.meta import Base
from data.models.snapshot_model import Snapshot
from data.models.topic_model import Topic
from data.models.snapshot_topic_model import SnapshotTopic
from dotenv import load_dotenv
load_dotenv()
import logging
logger = logging.getLogger(__name__)

class SnapshotDataStore:
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

    def create_snapshot(self, user_id, id, created, topics):
        # insert into data store and commit
        self.session.add(Snapshot(user_id=user_id, id=id, created=created, published=None))
        for topic in topics:
            self.session.add(SnapshotTopic(snapshot_id=id, topic_id=topic['id']))
        self.session.commit()

    def get_snapshots(self, user_id):
        # select all snapshots
        return self.session.query(Snapshot.user_id, Snapshot.id, Snapshot.created, Snapshot.published).filter(Snapshot.user_id == user_id)

    def get_snapshot_by_id(self, user_id, id):
        # select snapshot by ID
        return self.session.query(Snapshot.user_id, Snapshot.id, Snapshot.created, Snapshot.published).filter(Snapshot.user_id == user_id, Snapshot.id == id).one_or_none()

    def get_snapshot_topics_by_id(self, user_id, id):
        # select snapshot topics by ID
        return self.session.query(Topic.user_id, Topic.id, Topic.question, Topic.answer, Topic.created).filter(Snapshot.user_id == user_id, Snapshot.id == id, SnapshotTopic.snapshot_id == Snapshot.id, SnapshotTopic.topic_id == Topic.id).all()

    def delete_snapshot(self, user_id, id):
        # delete record from data store and commit
        self.session.query(Snapshot).filter(Snapshot.user_id == user_id, Snapshot.id == id).delete()
        self.session.query(SnapshotTopic).filter(SnapshotTopic.snapshot_id == id).delete()
        self.session.commit()


