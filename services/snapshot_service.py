import uuid
from datetime import datetime, timedelta
from data.datastores.snapshot_data_store import SnapshotDataStore
from services.user_service import UserService
from services.topic_service import TopicService
import logging
logger = logging.getLogger(__name__)

'''
Manages snapshot entity.
'''
class SnapshotService:
    def __init__(self):
        # init data store
        self.data_store = SnapshotDataStore()
        # init user and topic services
        self.user_service = UserService()
        self.topic_service = TopicService()

    def create_snapshot(self, user_id):
        """Creates a new snapshot.
        @param: user_id: author's identifier
        """
        # check if such user exists
        user = self.get_user(user_id)
        logger.error('Checking user ID: ' + user_id)
        if user is None:
            return

        # get all active topics for the user
        topics = self.topic_service.get_topics(user_id)
        logger.error('Getting topics for user ID: ' + user_id)

        # generate new snapshot identifier and add to data store
        id = str(uuid.uuid4())
        self.data_store.create_snapshot(user_id, id, datetime.now().timestamp(), topics)
        return id

    def get_snapshots(self, user_id):
        """Return all snapshots for a user.
        @param: user_id: author's identifier
        """
        # check if such user exists
        user = self.get_user(user_id)
        if user is None:
            return

        # retrieve all snapshots from data store, convert to list and return
        results = self.data_store.get_snapshots(user_id)
        return [self.map_snapshot(user_id, id, created, published, None) for user_id, id, created, published, in results]

    def get_snapshot_by_id(self, user_id, id):
        """Get snapshot by identifier.
        @param: user_id: author's identifier
        @param id: snapshot's ID
        """
        # check if such user exists
        user = self.get_user(user_id)
        if user is None:
            return

        # check if snapshot ID passed
        if id is None or len(id) == 0:
            return

        # retrieve snapshot from data store by ID; if snapshot not found, return None
        snapshot = self.data_store.get_snapshot_by_id(user_id, id)
        if not snapshot is None:
            snapshot_topics = self.data_store.get_snapshot_topics(user_id, id)
            return self.map_snapshot(snapshot.user_id, snapshot.id, snapshot.created, snapshot.published, snapshot_topics)

    def delete_snapshot(self, user_id, id):
        """Delete snapshot by identifier.
        @param: user_id: author's identifier
        @param id: snapshot's ID
        """
        # check if such user exists
        user = self.get_user(user_id)
        if user is None:
            return

        # check if snapshot ID passed
        if id is None or len(id) == 0:
            return

        # retrieve snapshot from data store by ID; if user not found, return None
        result = self.data_store.get_snapshot_by_id(user_id, id)
        if not result is None:
            # delete snapshot from data store by ID
            self.data_store.delete_snapshot(user_id, id)
            return id

    def get_user(self, user_id):
        # check if user ID passed
        if user_id is None or len(user_id) == 0:
            return

        # check if such user exists
        return self.user_service.get_user_by_id(user_id)

    def map_snapshot(self, user_id, id, created, published, snapshot_topics):
        """Maps data store row to dict.
        """
        response = {
            'user_id': user_id, 
            'id': id, 
            'created': created
        }
        if published is not None:
            response['published'] = published

        if snapshot_topics is not None:
            response['topics'] = [{'question': question, 'answer': answer} for user_id, topic_id, question, answer, created, in snapshot_topics]

        return response
