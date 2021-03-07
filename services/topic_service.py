import uuid
from datetime import datetime, timedelta
from data.datastores.topic_data_store import TopicDataStore
from services.user_service import UserService

'''
Manages topic entity.
'''
class TopicService:
    def __init__(self):
        # init data store
        self.data_store = TopicDataStore()
        # init user service for valdidation
        self.user_service = UserService()

    def create_topic(self, user_id, question, answer):
        """Creates a new topic.
        @param: user_id: author's identifier
        @param: question: topic's question
        @param: answer: topic's answer
        """
        # check if question passed
        if question is None or len(question) == 0:
            return
        
        # check if answer passed
        if answer is None or len(answer) == 0:
            return

        # check if such user exists
        user = self.get_user(user_id)
        if user is None:
            return

        # generate new topic identifier and add to data store
        id = str(uuid.uuid4())
        self.data_store.create_topic(user_id, id, question, answer, datetime.now().timestamp())
        return id

    def get_topics(self, user_id):
        """Return all topics for a user.
        @param: user_id: author's identifier
        """
        # check if such user exists
        user = self.get_user(user_id)
        if user is None:
            return

        # retrieve all topics from data store, convert to list and return
        results = self.data_store.get_topics(user_id)
        return [self.map_topic(user_id, id, question, answer, created) for user_id, id, question, answer, created, in results]

    def get_topic_by_id(self, user_id, id):
        """Get user by identifier.
        @param: user_id: author's identifier
        @param id: topic's ID
        """
        # check if such user exists
        user = self.get_user(user_id)
        if user is None:
            return

        # check if topic ID passed
        if id is None or len(id) == 0:
            return

        # retrieve toic from data store by ID; if topic not found, return None
        result = self.data_store.get_topic_by_id(user_id, id)
        if not result is None:
            return self.map_topic(result.user_id, result.id, result.question, result.answer, result.created)

    def delete_topic(self, user_id, id):
        """Delete topic by identifier.
        @param: user_id: author's identifier
        @param id: topic's ID
        """
        # check if such user exists
        user = self.get_user(user_id)
        if user is None:
            return

        # check if topic ID passed
        if id is None or len(id) == 0:
            return

        # retrieve user from data store by ID; if user not found, return None
        result = self.data_store.get_topic_by_id(user_id, id)
        if not result is None:
            # delete topic from data store by ID
            self.data_store.delete_topic(user_id, id)
            return id

    def get_user(self, user_id):
        # check if user ID passed
        if user_id is None or len(user_id) == 0:
            return

        # check if such user exists
        return self.user_service.get_user_by_id(user_id)

    def map_topic(self, user_id, id, question, answer, created):
        """Maps data store row to dict.
        """
        return {'user_id': user_id, 'id': id, 'question': question, 'answer': answer, 'created': created}
