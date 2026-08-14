"""
HackWae Voice Server

Voice Service
"""

from pathlib import Path

from schemas.voice_manifest import VoiceManifest

from services.voice.manager import voice_manager


class VoiceService:

    # --------------------------------------------------

    def list(self):

        return voice_manager.scan()

    # --------------------------------------------------

    def get(

        self,

        voice_id: str,

    ):

        return voice_manager.get(voice_id)

    # --------------------------------------------------

    def default(self):

        return voice_manager.default()

    # --------------------------------------------------

    def create(

        self,

        manifest: VoiceManifest,

        source: Path,

    ):

        return voice_manager.create(

            manifest=manifest,

            source=source,

        )

    # --------------------------------------------------

    def update(

        self,

        manifest: VoiceManifest,

    ):

        return voice_manager.update(

            manifest=manifest,

        )

    # --------------------------------------------------

    def remove(

        self,

        voice_id: str,

    ):

        return voice_manager.remove(

            voice_id,

        )


voice_service = VoiceService()
