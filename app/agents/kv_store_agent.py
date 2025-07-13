from ..tools.stores.mongo_store import MongoStore
from ..tools.stores.redis_store import RedisStore
from ..models.key_value import KeyValue

class KeyValueStorageAgent:
    def __init__(self):
        self.store_map = {
            "redis": RedisStore,
            "mongo": MongoStore,
        }

    def run(self, task: dict):
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
        return {"status": "success", "stored_to": store_type}
