import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import User, Topic, Base


class DataStore:
    def __init__(self):
        LOCAL_DB_FILE = 'data/local.db'
        engine = create_engine('sqlite:///' + LOCAL_DB_FILE)
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
