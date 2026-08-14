from datetime import datetime

from pydantic import BaseModel


class HistoryItem(BaseModel):

    id: str

    filename: str

    text: str

    voice: str

    engine: str

    sample_rate: int

    created: datetime
