from queues import broadcast_tasks
from dotenv import load_dotenv
import logging
logger = logging.getLogger(__name__)

'''
Braodcast queue client.
'''
class BroadcastQueue:
    def __init__(self):
        pass

    def create_broadcast(self, snapshot):
        broadcast_tasks.publish.delay(snapshot)
        return -1