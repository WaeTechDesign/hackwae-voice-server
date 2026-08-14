from pathlib import Path

from core.base_engine import BaseEngine


class DummyEngine(BaseEngine):

    def generate(
        self,
        text,
        voice,
        output=None,
    ):

        return {
            "engine": self.name,
            "voice": voice.name,
            "text": text,
            "output": str(output),
        }
