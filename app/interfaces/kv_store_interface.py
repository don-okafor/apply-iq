from abc import ABC, abstractmethod
from ..models.key_value import KeyValue
from typing import Any

class KeyValueStore(ABC):
    @abstractmethod
    def save(self, data: KeyValue) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        pass
