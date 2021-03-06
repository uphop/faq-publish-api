import unittest
import uuid
import names

from services.user_service import UserService

class TestUserService(unittest.TestCase):
    user_service = UserService()
    
    def test_create_user_nonexisting_name(self):
        user_name = names.get_full_name()
        user_id = self.user_service.create_user(user_name)

        # check if ID is generated
        self.assertIsNotNone(user_id)

        # check if ID is UUID
        try:
            uuid_obj = uuid.UUID(user_id, version=4)
        except ValueError:
            self.fail('Expected UUID, but got something else.')

        # clean-up
        self.user_service.delete_user(user_id)

   
    def test_create_user_existing_name(self):
        user_name = names.get_full_name()
        user_id = self.user_service.create_user(user_name)

        # check if ID is generated
        self.assertIsNotNone(user_id)

        # now try to create user with the same name
        user_id_2 = self.user_service.create_user(user_name)
        # check if ID is not generated
        self.assertIsNone(user_id_2)

        # clean-up
        self.user_service.delete_user(user_id)


    def test_create_user_empty_name(self):
        user_id = self.user_service.create_user(None)
        # check if ID is not generated
        self.assertIsNone(user_id)

        user_id = self.user_service.create_user('')
        # check if ID is not generated
        self.assertIsNone(user_id)


    def test_get_users(self):
        users = self.user_service.get_users()
        self.assertTrue(not users is None, 'User list expected, but not returned')


if __name__ == '__main__':
    unittest.main()

