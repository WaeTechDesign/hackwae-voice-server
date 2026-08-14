"""
HackWae Voice Server

Server Configuration
"""

from pydantic import BaseModel, Field


class ServerSettings(BaseModel):
    """
    HTTP Server configuration.
    """

    host: str = Field(
        default="0.0.0.0",
        description="Bind address."
    )

    port: int = Field(
        default=8082,
        ge=1,
        le=65535,
        description="Server port."
    )

    reload: bool = Field(
        default=False,
        description="Enable auto reload."
    )

    workers: int = Field(
        default=1,
        ge=1,
        description="Number of workers."
    )

    cors: bool = Field(
        default=True,
        description="Enable CORS."
    )

    docs: bool = Field(
        default=True,
        description="Enable Swagger UI."
    )

    redoc: bool = Field(
        default=True,
        description="Enable ReDoc."
    )
