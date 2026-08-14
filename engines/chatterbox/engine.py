"""
HackWae Voice Server

Chatterbox Engine
"""

from pathlib import Path

from core.base_engine import BaseEngine
from core.config import settings
from core.lock.engine_lock import engine_lock

from services.model_manager import model_manager

from utils.logger import logger

from .loader import loader
from .runtime import runtime


class ChatterboxEngine(BaseEngine):

    def __init__(self):

        manifest = model_manager.get("chatterbox")

        if manifest is None:
            raise RuntimeError(
                "Manifest chatterbox tidak ditemukan."
            )

        super().__init__(
            name="chatterbox",
            model_path=settings.paths.models / "chatterbox",
        )

        self.manifest = manifest
        self.engine_config = settings.engine.engines["chatterbox"]

    # ----------------------------------------------------------

    def load(self):

        if self.loaded:
            logger.info(
                "Chatterbox Engine already loaded."
            )
            return

        logger.info(
            "Loading Chatterbox Engine..."
        )

        loader.load(
            model_dir=self.model_path,
            device=self.engine_config.device,
        )

        self._loaded = True

        logger.info(
            "Chatterbox Engine Ready."
        )

    # ----------------------------------------------------------

    def unload(self):

        logger.info(
            "Unloading Chatterbox Engine..."
        )

        loader.model = None
        loader.loaded = False

        self._loaded = False

    # ----------------------------------------------------------

    def generate(
        self,
        text: str,
        voice,
        output: Path,
    ) -> Path:

        self.load()

        voice_file = (
            settings.paths.voices
            / voice.gender
            / voice.id
            / "voice.wav"
        )

        if not voice_file.exists():

            raise FileNotFoundError(
                f"Voice file tidak ditemukan: {voice_file}"
            )

        lock = engine_lock.get(self.name)

        with lock:

            logger.info(
                f"Acquire Engine Lock : {self.name}"
            )

            result = runtime.generate(

                model_dir=self.model_path,

                text=text,

                voice=voice_file,

                output=output,

            )

            logger.info(
                f"Release Engine Lock : {self.name}"
            )

            return result
