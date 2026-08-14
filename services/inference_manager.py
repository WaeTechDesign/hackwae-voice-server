"""
HackWae Voice Server

Inference Manager
"""

from pathlib import Path

from core.engine_registry import engine_registry
from services.voice_manager import voice_manager
from utils.logger import logger


class InferenceManager:

    def tts(
        self,
        engine: str,
        voice: str,
        text: str,
        output: Path | None = None,
    ):

        logger.info(f"TTS Request : {engine}")

        engine_instance = engine_registry.get(engine)

        if engine_instance is None:
            raise RuntimeError(f"Engine '{engine}' tidak ditemukan.")

        voice_manifest = voice_manager.get(voice)

        if voice_manifest is None:
            raise RuntimeError(f"Voice '{voice}' tidak ditemukan.")

        logger.info(f"Voice : {voice_manifest.name}")

        return engine_instance.generate(
            text=text,
            voice=voice_manifest,
            output=output,
        )


inference_manager = InferenceManager()
