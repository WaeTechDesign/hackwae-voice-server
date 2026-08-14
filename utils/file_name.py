"""
HackWae Voice Server

Filename Generator
"""

from datetime import datetime
from uuid import uuid4


def generate_audio_filename() ->str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    uid = uuid4().hex[:6]

    return f"tts_{timestamp}_{uid}.wav"
