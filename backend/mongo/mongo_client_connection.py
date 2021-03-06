import os

from pymongo import MongoClient

from tools import logger


# Initialising the database
DEFAULT_URL = 'mongodb://localhost:27017/'
MONGO_URL = os.getenv('MONGO_URL', DEFAULT_URL)

logger.get_logger().warning('Starting web_server with mongo url: %s', MONGO_URL)

client = MongoClient(
    MONGO_URL,
    connect=True,  # Connect straight to DB, do not wait for 1st request
    serverSelectionTimeoutMS=3000  # Client timeout
)

# Use the documentation database
DB = client['documentation']
