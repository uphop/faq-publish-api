import os
from queues import broadcast_tasks
import logging
logger = logging.getLogger(__name__)

'''
Braodcast queue client.
'''
class BroadcastQueue:
    def __init__(self):
        self.CELERY_QUEUE = os.environ.get('CELERY_QUEUE', 'publish_queue')

    def create_broadcast(self, snapshot):
        result = broadcast_tasks.publish.apply_async(args=[snapshot], queue=self.CELERY_QUEUE, serializer='json')
        return -1