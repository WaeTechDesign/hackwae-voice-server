"""
HackWae Voice Server

Voice Configuration
"""

from typing import Dict

from pydantic import BaseModel, Field


class VoiceItem(BaseModel):
    """
    Configuration for a single voice.
    """

    name: str

    gender: str

    language: str

    path: str

    enabled: bool = True

    default: bool = False


class VoiceSettings(BaseModel):
    """
    Global voice configuration.
    """

    default_voice: str = "putri"

    sample_rate: int = Field(
        default=24000,
        ge=8000,
        le=96000,
    )

    normalize_audio: bool = True

    trim_silence: bool = True

    output_format: str = "wav"

    voices: Dict[str, VoiceItem] = Field(
        default_factory=lambda: {
            "putri": VoiceItem(
                name="Putri",
                gender="female",
                language="id",
                path="/ai/voices/female/putri.wav",
                default=True,
            ),
            "narator": VoiceItem(
                name="Narrator",
                gender="male",
                language="id",
                path="/ai/voices/male/narrator.wav",
            ),
        }
    )
