import os
import sys
import logging
from dotenv import load_dotenv
from celery import Celery

# init config
load_dotenv()
CELERY_BROKER = os.environ.get('CELERY_BROKER', 'pyamqp://guest@localhost//')

# Enable loging
logging.root.handlers = []
logging.basicConfig(
    encoding='utf-8',
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Init Celery broker
broker = Celery('queues',
             broker=CELERY_BROKER,
             backend='rpc://',
             include=['queues.broadcast_tasks'])

# Optional configuration, see the application user guide.
broker.conf.update(
    result_expires=3600,
)

# Default handler
if __name__ == '__main__':
    broker.start()