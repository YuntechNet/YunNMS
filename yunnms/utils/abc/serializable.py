from typing import Dict
from abc import ABC, abstractstaticmethod


class Serializable(ABC):
    @abstractstaticmethod
    def serialize(obj: "Serializable", *args, **kwargs) -> Dict:
        pass

    @abstractstaticmethod
    def deserialize(data: Dict, *args, **kwargs) -> "Serializable":
        pass
