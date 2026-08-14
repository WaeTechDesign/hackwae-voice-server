"""
HackWae Voice Server

Chatterbox Cache
"""

from pathlib import Path


class ChatterboxCache:

    def __init__(self):

        self._voices = {}

    # -----------------------------

    def get(self, path: Path):

        return self._voices.get(str(path))

    # -----------------------------

    def set(self, path: Path, value):

        self._voices[str(path)] = value

    # -----------------------------

    def clear(self):

        self._voices.clear()


cache = ChatterboxCache()
