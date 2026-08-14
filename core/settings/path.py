"""
HackWae Voice Server

Path Configuration
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class PathSettings(BaseModel):
    """
    Global filesystem paths used by HackWae Voice Server.
    """

    project: Path = Field(default=PROJECT_ROOT)

    models: Path = Field(default=Path("/ai/models"))

    voices: Path = Field(default=Path("/ai/voices"))

    storage: Path = Field(default=PROJECT_ROOT / "storage")

    uploads: Path = Field(default=PROJECT_ROOT / "uploads")

    cache: Path = Field(default=PROJECT_ROOT / "storage/cache")

    history: Path = Field(default=PROJECT_ROOT / "storage/history")

    previews: Path = Field(default=PROJECT_ROOT / "storage/previews")

    temp: Path = Field(default=PROJECT_ROOT / "storage/temp")

    logs: Path = Field(default=PROJECT_ROOT / "storage/logs")

    downloads: Path = Field(default=PROJECT_ROOT / "storage/downloads")

    def ensure_directories(self) -> None:
        """
        Create runtime directories if they do not exist.
        """

        directories = (
            self.storage,
            self.uploads,
            self.cache,
            self.history,
            self.previews,
            self.temp,
            self.logs,
            self.downloads,
        )

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
