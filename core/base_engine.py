"""
HackWae Voice Server

Base Engine
"""

from __future__ import annotations

from abc import ABC
from pathlib import Path

from interfaces.engine import EngineInterface
from utils.logger import logger


class BaseEngine(EngineInterface, ABC):
    """
    Base class for all AI engines.
    """

    def __init__(
        self,
        name: str,
        model_path: Path,
    ) -> None:

        self._name = name

        self._model_path = Path(model_path)

        self._loaded = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def model_path(self) -> Path:
        return self._model_path

    @property
    def loaded(self) -> bool:
        return self._loaded

    def load(self):

        logger.info(f"Loading engine: {self.name}")

        self._loaded = True

    def unload(self):

        logger.info(f"Unloading engine: {self.name}")

        self._loaded = False

    def health(self) -> bool:

        return self.loaded
