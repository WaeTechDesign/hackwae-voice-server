"""
Engine Interface
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class EngineInterface(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def load(self):
        ...

    @abstractmethod
    def unload(self):
        ...

    @abstractmethod
    def health(self) -> bool:
        ...

    @abstractmethod
    def generate(self, *args, **kwargs):
        ...
