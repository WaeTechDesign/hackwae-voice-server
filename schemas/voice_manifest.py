from pydantic import BaseModel


class VoiceManifest(BaseModel):

    id: str

    name: str

    gender: str

    language: list[str]

    author: str = "Unknown"

    description: str = ""

    sample_rate: int = 24000

    engines: list[str] = []

    default: bool = False

    enabled: bool = True
