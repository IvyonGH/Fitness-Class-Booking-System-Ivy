"""MongoDB connection helper.

Reads MONGODB_URI / MONGODB_DB from the environment (see .env.example).
The client connects lazily on first use so the app can still be imported
and started without a database configured.
"""
import os

from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument

load_dotenv()

_client = None


def get_db():
    global _client
    if _client is None:
        uri = os.environ.get("MONGODB_URI")
        if not uri:
            raise RuntimeError(
                "MONGODB_URI is not set. Copy .env.example to .env and fill in "
                "your MongoDB Atlas connection string."
            )
        _client = MongoClient(uri)
    return _client[os.environ.get("MONGODB_DB", "wonderfitness")]


def next_sequence(db, name):
    """Atomically returns the next integer in a named sequence, starting at 1."""
    doc = db.counters.find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return doc["seq"]
