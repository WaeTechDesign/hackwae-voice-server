"""
HackWae Voice Server

Queue Job
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid


@dataclass(slots=True)
class QueueJob:

    id: str = field(
        default_factory=lambda: uuid.uuid4().hex
    )

    text: str = ""

    voice: str = "putri"

    engine: str = "chatterbox"

    # Filename yang diminta user.
    # None = server akan membuat filename otomatis.
    requested_output: Optional[str] = None

    # Path/file hasil aktual dari proses TTS.
    output: Optional[Path] = None

    status: str = "queued"

    progress: int = 0

    created: datetime = field(
        default_factory=datetime.utcnow
    )

    started: Optional[datetime] = None

    finished: Optional[datetime] = None

    error: Optional[str] = None
