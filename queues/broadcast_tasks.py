from broker import broker
from services.broadcast_service import BroadcastService
import logging
logger = logging.getLogger(__name__)

@broker.task
def publish(snapshot):
    broadcast_service = BroadcastService()
    broadcast_service.create_broadcast(snapshot)
    return 0