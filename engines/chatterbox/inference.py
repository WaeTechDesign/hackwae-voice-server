"""
HackWae Voice Server

Inference
"""

from pathlib import Path

from .loader import loader
from .runtime import runtime


class ChatterboxInference:

    def tts(
        self,
        model_dir: Path,
        voice: Path,
        text: str,
        output: Path,
    ):

        loader.load(model_dir)

        return runtime.generate(
            model_dir=model_dir,
            voice=voice,
            text=text,
            output=output,
        )


inference = ChatterboxInference()
