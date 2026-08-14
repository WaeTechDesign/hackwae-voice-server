"""
HackWae Voice Server

Docker Configuration
"""

from pydantic import BaseModel


class DockerSettings(BaseModel):
    """
    Docker runtime configuration.
    """

    enabled: bool = False

    container_name: str = "hackwae-voice-server"

    network: str = "bridge"

    gpu: bool = True

    auto_restart: bool = True

    timezone: str = "Asia/Makassar"

    mount_models: str = "/ai/models"

    mount_voices: str = "/ai/voices"
