import uuid
from datetime import datetime, timedelta
from data.datastores.user_data_store import UserDataStore

'''
Manages user entity.
'''
class UserService:
    def __init__(self):
        # init data store
        self.data_store = UserDataStore()

    def create_user(self, name):
        """Creates a new user.
        @param name: the full user's name
        """
        # check if name is passed
        if not name or len(name) == 0:
            return

        # check if name not taken yet
        user_with_same_name = self.get_user_by_name(name)
        if len(user_with_same_name) == 1:
            return user_with_same_name[0]['id']
        elif len(user_with_same_name) > 1:
            return

        # generate new user identifier and add to data store
        id = str(uuid.uuid4())
        self.data_store.create_user(id, name, datetime.now().timestamp())
        return id

    def get_users(self):
        """Return all users.
        """
        # retrieve all users from data store, convert to list and return
        results = self.data_store.get_users()
        return [self.map_user(id, name, created) for id, name, created, in results]

    def get_user_by_id(self, id):
        """Get user by identifier.
        @param id: user's ID
        """
        # check if ID is passed
        if not id or len(id) == 0:
            return

        # retrieve user from data store by ID; if user not found, return None
        result = self.data_store.get_user_by_id(id)
        if not result is None:
            return self.map_user(result.id, result.name, result.created)

    def get_user_by_name(self, name):
        """Get user by name.
        @param name: user's full name
        """
        # check if name is passed
        if not name or len(name) == 0:
            return

        # retrieve user from data store by full name
        results = self.data_store.get_user_by_name(name)
        return [self.map_user(id, name, created) for id, name, created, in results]

    def delete_user(self, id):
        """Delete user by identifier.
        @param id: user's ID
        """
        # check if ID is passed
        if not id or len(id) == 0:
            return
            
        # retrieve user from data store by ID; if user not found, return None
        result = self.data_store.get_user_by_id(id)
        if not result is None:
            # delete user from data store by ID
            self.data_store.delete_user(id)
            return id

    def map_user(self, id, name, created):
        """Maps data store row to dict.
        """
        return {'id': id, 'name': name, 'created': created}
