"""
HackWae Voice Server

Central application configuration.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import BaseModel

from core.settings.path import PathSettings
from core.settings.server import ServerSettings
from core.settings.engine import EngineSettings
from core.settings.voice import VoiceSettings
from core.settings.docker import DockerSettings


class Settings(BaseModel):
    """
    Main application settings.
    """

    server: ServerSettings = ServerSettings()

    paths: PathSettings = PathSettings()

    engine: EngineSettings = EngineSettings()

    voice: VoiceSettings = VoiceSettings()

    docker: DockerSettings = DockerSettings()

    def initialize(self) -> None:
        """
        Initialize application environment.
        """

        self.paths.ensure_directories()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return singleton Settings object.
    """

    settings = Settings()

    settings.initialize()

    return settings


settings = get_settings()
