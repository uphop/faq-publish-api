from queues import broadcast_tasks
import logging
logger = logging.getLogger(__name__)

'''
Braodcast queue client.
'''
class BroadcastQueue:
    def create_broadcast(self, snapshot):
        result = broadcast_tasks.publish.apply_async(args=[snapshot], queue='publish_queue', serializer='json')
        return -1