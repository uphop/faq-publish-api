import uuid
import logging
logger = logging.getLogger(__name__)

'''
Manages broadcast entity.
'''
class BroadcastService:
    def __init__(self):
        pass

    def create_broadcast(self, snapshot):
        print('Got snapshot: ' + snapshot['id'])