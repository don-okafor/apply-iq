from pymongo import MongoClient
from ...interfaces.kv_store_interface import KeyValueStore
from ...models.key_value import KeyValue
from typing import Any
import json

class MongoStore(KeyValueStore):
    def __init__(self, config: dict):
        """
        Initializes a MongoDB client and connects to the given database and collection.
        Config example:
        {
            "host": "localhost",
            "port": 27017,
            "db": "apply-ql-db",
            "collection": "resume"
        }
        """
        self.client = MongoClient(
            host=config.get("host", "localhost"),
            port=config.get("port", 27017)
        )
        self.db = self.client[config.get("db", "apply-ql-db")]
        self.collection = self.db[config.get("collection", "resume")]

    def save(self, data: KeyValue) -> None:
        """
        Inserts or updates a key-value pair in MongoDB.
        """
        self.collection.update_one(
            {"key": data.key},
            {"$set": {"value": data.value}},
            upsert=True
        )

    def get(self, key: str) -> Any:
        """
        Retrieves a value by key from MongoDB.
        """
        result = self.collection.find_one({"key": key})
        return result["value"] if result else None
