"""
HackWae Voice Server

Voice Updater
"""

from pathlib import Path

from schemas.voice_manifest import VoiceManifest

from .database import database


class VoiceUpdater:

    # --------------------------------------------------

    def update(

        self,

        directory: Path,

        manifest: VoiceManifest,

    ) -> VoiceManifest:

        metadata = directory / "voice.json"

        database.save(

            metadata,

            manifest.model_dump(),

        )

        return manifest


updater = VoiceUpdater()
