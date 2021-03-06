from data.datastore.user_topic_data_store import UserTopicDataStore
import uuid
from datetime import datetime, timedelta
from utils import log

class UserService:
    def __init__(self):
        
        self.data_store = UserTopicDataStore()

    def create_user(self, name):
        id = str(uuid.uuid4())
        self.data_store.create_user(id, name, datetime.now().timestamp())
        return id

    def get_users(self):
        # retrieve users
        results = self.data_store.get_users()

        # iterate through results and return
        users = []
        for row in results:
            users.append({
                'name': row.name,
                'created': row.created
            })

        return users

    def get_user(self, id):
        # retrieve user by ID
        result = self.data_store.get_user(id)

        # if user not found, return None
        if not result is None:
            # seems like user exists, return details
            user = {
                'name': result.name,
                'created': result.created
            }
            return user

    def delete_user(self, id):
        return self.data_store.delete_user(id)
