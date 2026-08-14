"""
HackWae Voice Server

TTS Schema
"""

from pydantic import BaseModel, Field


class TTSRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Text to synthesize.",
    )

    voice: str = Field(
        default="putri",
        min_length=1,
        max_length=100,
        description="Voice ID.",
    )

    engine: str = Field(
        default="chatterbox",
        min_length=1,
        max_length=100,
        description="TTS engine.",
    )

    output: str | None = Field(
        default=None,
        max_length=255,
        description="Optional output filename.",
    )
