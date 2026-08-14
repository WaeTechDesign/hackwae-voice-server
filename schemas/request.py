from pydantic import BaseModel


class TTSRequest(BaseModel):

    text: str

    voice: str = "putri"

    engine: str = "chatterbox"

    output: str | None = None
