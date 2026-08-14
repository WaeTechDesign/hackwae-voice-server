"""
HackWae Voice Server

Chatterbox Loader
"""

from pathlib import Path

from chatterbox.tts import ChatterboxTTS
from safetensors.torch import load_file

from utils.logger import logger


class ChatterboxLoader:

    def __init__(self):

        self.model = None

        self.loaded = False

    # -------------------------------------------------

    def load(
        self,
        model_dir: Path,
        device: str = "cuda",
    ):

        if self.loaded:

            logger.info("Chatterbox already loaded.")

            return self.model

        logger.info("Loading Chatterbox...")

        model = ChatterboxTTS.from_pretrained(
            device=device
        )

        checkpoint = (
            model_dir /
            "checkpoints" /
            "t3_cfg.safetensors"
        )

        logger.info(
            "Loading Indonesian checkpoint..."
        )

        state = load_file(
            checkpoint,
            device="cpu",
        )

        model.t3.load_state_dict(state)

        self.model = model

        self.loaded = True

        logger.info("Chatterbox Ready.")

        return self.model


loader = ChatterboxLoader()
