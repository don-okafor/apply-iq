from ..tools.stores.mongo_store import MongoStore
from ..tools.stores.redis_store import RedisStore
from ..models.key_value import KeyValue
#from .main_agent import BaseAgent
from typing import Any, Dict
import os

class KeyValueStorageAgent:
    def __init__(self, base: Any = None):
        self.base = base

        self.store_map = {
            "redis": RedisStore,
            "mongo": MongoStore,
        }
        
        
    """def run(self, task: dict):
        key = task["key"]
        value = task["value"]
        store_type = task.get("store_type", "mongo")
        store_config = task.get("store_config", {})

        store_cls = self.store_map.get(store_type)
        if not store_cls:
            raise ValueError(f"Unsupported store type: {store_type}")

        store = store_cls(config=store_config)
        kv = KeyValue(key=key, value=value)
        store.save(kv)
        return {"status": "success", "stored_to": store_type}"""
    

    async def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        #key = task.get("key")
        filepath = task.get("filepath")
        key = os.path.basename(filepath)
        value = task.get("value") or filepath

        if not key or value is None:
            return {"status": "error", "message": "Missing key or value"}
        
        store_type = task.get("store_type", "mongo")

        store_cls = self.store_map.get(store_type)
        if not store_cls:
            raise ValueError(f"Unsupported store type: {store_type}")

        store = store_cls()
        kv = KeyValue(key=key, value=value)
        await store.save(kv)
        return {"status": "success", "key": key, "stored_to": store_type}
