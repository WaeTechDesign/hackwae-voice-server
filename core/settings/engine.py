"""
HackWae Voice Server

Engine Configuration
"""

from typing import Dict

from pydantic import BaseModel, Field


class EngineItem(BaseModel):
    """
    Configuration for a single engine.
    """

    enabled: bool = True

    model: str = ""

    device: str = "cuda"

    use_half: bool = True

    preload: bool = False


class EngineSettings(BaseModel):
    """
    Global engine configuration.
    """

    default: str = "chatterbox"

    auto_detect_gpu: bool = True

    unload_unused: bool = False

    engines: Dict[str, EngineItem] = Field(
        default_factory=lambda: {
            "chatterbox": EngineItem(
                enabled=True,
                model="Chatterbox-TTS-Indonesian",
                preload=True,
            ),
            "fishspeech": EngineItem(
                enabled=False,
                model="OpenAudio-S2",
            ),
            "kokoro": EngineItem(
                enabled=False,
                model="Kokoro-82M",
            ),
            "melo": EngineItem(
                enabled=False,
                model="MeloTTS-ID",
            ),
            "whisper": EngineItem(
                enabled=True,
                model="large-v3",
                device="cuda",
                use_half=False,
            ),
        }
    )
