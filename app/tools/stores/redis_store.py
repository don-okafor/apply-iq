import redis
import json
from ...interfaces.kv_store_interface import KeyValueStore
from ...models.key_value import KeyValue

class RedisStore(KeyValueStore):
    def __init__(self, config: dict):
        self._client = redis.Redis(
            host=config.get("host", "localhost"),
            port=config.get("port", 6379),
            db=config.get("db", 0)
        )

    def save(self, data: KeyValue):
        self._client.set(data.key, json.dumps(data.value))

    def get(self, key: str):
        value = self._client.get(key)
        return json.loads(value) if value else None
