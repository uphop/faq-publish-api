from data.data_store import DataStore
import uuid
from datetime import datetime, timedelta


class UserManager:
    def __init__(self):
        pass

    def create_user(self, name):
        id = str(uuid.uuid4())
        DataStore().create_user(id, name, datetime.now().timestamp())
        return id

    def get_users(self):
        # retrieve users
        results = DataStore().get_users()

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
        result = DataStore().get_user(id)

        # if user not found, return None
        if not result is None:
            # seems like user exists, return details
            user = {
                'name': result.name,
                'created': result.created
            }
            return user

    def delete_user(self, id):
        return DataStore().delete_user(id)
