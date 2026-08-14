from pydantic import BaseModel


class ModelManifest(BaseModel):
    id: str
    name: str
    engine: str
    version: str

    author: str = "Unknown"

    description: str = ""

    language: list[str] = []

    tags: list[str] = []

    tts: bool = False

    stt: bool = False

    voice_clone: bool = False

    voice_conversion: bool = False

    gpu: bool = True

    default: bool = False
