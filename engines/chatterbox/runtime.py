"""
HackWae Voice Server

Chatterbox Runtime
"""

from pathlib import Path

import torch
import torchaudio as ta

from utils.logger import logger

from .loader import loader


class ChatterboxRuntime:

    def generate(
        self,
        model_dir: Path,
        text: str,
        voice: Path,
        output: Path,
    ) -> Path:

        model = loader.load(model_dir)

        logger.info("Generating audio...")

        wav = model.generate(
            text,
            audio_prompt_path=str(voice),
        )

        if wav.dim() == 1:
            wav = wav.unsqueeze(0)

        ta.save(
            str(output),
            wav.cpu(),
            model.sr,
        )

        logger.info(f"Saved : {output}")

        return output


runtime = ChatterboxRuntime()
