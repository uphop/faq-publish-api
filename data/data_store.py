from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import User, Topic, Base
from datetime import datetime, timedelta
import uuid

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

    def create_user(self, name):
        new_uuid = str(uuid.uuid4())
        new_user = User(user_id=new_uuid, name=name, created=datetime.now().timestamp())
        self.session.add(new_user)
        self.session.commit()

        return new_uuid

 


