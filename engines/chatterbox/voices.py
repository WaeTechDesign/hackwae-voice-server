"""
HackWae Voice Server

Voice Loader
"""

from pathlib import Path

import torchaudio

from utils.logger import logger

from .cache import cache


class VoiceLoader:

    def load(
        self,
        voice: Path,
    ):

        cached = cache.get(voice)

        if cached is not None:

            return cached

        logger.info(f"Loading voice: {voice.name}")

        audio, sr = torchaudio.load(voice)

        cache.set(
            voice,
            (audio, sr),
        )

        return audio, sr


voice_loader = VoiceLoader()
