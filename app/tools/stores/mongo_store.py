from pymongo import MongoClient
from ...interfaces.kv_store_interface import KeyValueStore
from ...models.key_value import KeyValue
from typing import Any
import json
import motor.motor_asyncio
from ...config import get_settings

class MongoStore(KeyValueStore):
    def __init__(self, mongo_db: str, mongo_collection: str):
        """self.client = MongoClient(
            host=config.get("host", "localhost"),
            port=config.get("port", 27017)
        )
        self.db = self.client[config.get("db", "apply-ql-db")]
        self.collection = self.db[config.get("collection", "resume")]"""

        cfg = get_settings()
        self.client = motor.motor_asyncio.AsyncIOMotorClient(cfg.mongo_uri)
        #self.db = self.client[cfg.mongo_db]
        #self.col = self.db[cfg.mongo_collection]
        self.db = self.client[mongo_db]
        self.col = self.db[mongo_collection]


    async def save(self, data: KeyValue):
        await self.col.update_one(
            {"key": data.key},
            {"$set": {"value": data.value}},
            upsert=True,
        )

    async def get(self, key: str):
        doc = await self.col.find_one({"key": key})
        return doc["value"] if doc else None
