from abc import ABC, abstractmethod
from typing import Dict, Any
from state import State


class BaseStep(ABC):
    """Abstract base class for all steps."""

    @abstractmethod
    def run(self, state: State) -> Dict[str, Any]:
        pass
