"""
HackWae Voice Server

Voice Creator
"""

import shutil
from pathlib import Path

from core.config import settings

from schemas.voice_manifest import VoiceManifest

from .database import database
from .validator import validator


class VoiceCreator:

    # --------------------------------------------------

    def create(

        self,

        manifest: VoiceManifest,

        source: Path,

    ) -> VoiceManifest:

        directory = (

            settings.paths.voices

            / manifest.gender

            / manifest.id

        )

        directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        voice_file = directory / "voice.wav"

        shutil.copy2(

            source,

            voice_file,

        )

        metadata = directory / "voice.json"

        database.save(

            metadata,

            manifest.model_dump(),

        )

        if not validator.validate(directory):

            raise RuntimeError(

                "Voice validation failed."

            )

        return manifest


creator = VoiceCreator()
