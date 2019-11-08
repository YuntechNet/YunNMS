from typing import Dict
from abc import ABC, abstractclassmethod


class SNMPTrapABC(ABC):
    @abstractclassmethod
    def is_trap_match(
        self, context: Dict, result: Dict[str, str], *args, **kwargs
    ) -> bool:
        """Method for checking instance can process trap or not"""

    @abstractclassmethod
    def trap_update(self, context: Dict, result: Dict[str, str]) -> None:
        """Method to handle the traps."""
