"""
HackWae Voice Server

Voice Manager
"""

from pathlib import Path

from core.config import settings

from schemas.voice_manifest import VoiceManifest

from .creator import creator
from .remover import remover
from .scanner import scanner
from .updater import updater


class VoiceManager:

    # --------------------------------------------------

    def scan(self) -> list[VoiceManifest]:

        return scanner.scan()

    # --------------------------------------------------

    def get(

        self,

        voice_id: str,

    ) -> VoiceManifest | None:

        for voice in self.scan():

            if voice.id == voice_id:

                return voice

        return None

    # --------------------------------------------------

    def default(self) -> VoiceManifest | None:

        voices = self.scan()

        if not voices:

            return None

        return voices[0]

    # --------------------------------------------------

    def create(

        self,

        manifest: VoiceManifest,

        source: Path,

    ) -> VoiceManifest:

        return creator.create(

            manifest=manifest,

            source=source,

        )

    # --------------------------------------------------

    def update(

        self,

        manifest: VoiceManifest,

    ) -> VoiceManifest:

        directory = (

            settings.paths.voices

            / manifest.gender

            / manifest.id

        )

        return updater.update(

            directory=directory,

            manifest=manifest,

        )

    # --------------------------------------------------

    def remove(

        self,

        voice_id: str,

    ) -> bool:

        voice = self.get(voice_id)

        if voice is None:

            return False

        directory = (

            settings.paths.voices

            / voice.gender

            / voice.id

        )

        return remover.remove(

            directory=directory,

        )


voice_manager = VoiceManager()
