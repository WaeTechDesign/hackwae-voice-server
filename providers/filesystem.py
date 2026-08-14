"""
HackWae Voice Server

Filesystem Provider
"""

from __future__ import annotations

import shutil
from pathlib import Path

from core.config import settings
from utils.logger import logger


class FilesystemProvider:
    """
    Filesystem helper class.
    """

    @staticmethod
    def exists(path: str | Path) -> bool:
        return Path(path).exists()

    @staticmethod
    def mkdir(path: str | Path) -> Path:
        path = Path(path)

        path.mkdir(parents=True, exist_ok=True)

        return path

    @staticmethod
    def remove(path: str | Path) -> bool:
        path = Path(path)

        if not path.exists():
            return False

        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

        logger.info(f"Removed: {path}")

        return True

    @staticmethod
    def list_files(path: str | Path):

        path = Path(path)

        if not path.exists():
            return []

        return sorted(
            [
                item
                for item in path.iterdir()
                if item.is_file()
            ]
        )

    @staticmethod
    def list_directories(path: str | Path):

        path = Path(path)

        if not path.exists():
            return []

        return sorted(
            [
                item
                for item in path.iterdir()
                if item.is_dir()
            ]
        )

    @staticmethod
    def model_path(engine: str) -> Path:

        return settings.paths.models / engine

    @staticmethod
    def voice_path(category: str, voice: str) -> Path:

        return (
            settings.paths.voices
            / category
            / voice
        )

    @staticmethod
    def storage_path(name: str) -> Path:

        return settings.paths.storage / name


filesystem = FilesystemProvider()
