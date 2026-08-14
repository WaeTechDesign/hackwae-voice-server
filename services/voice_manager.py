"""
HackWae Voice Server

Voice Manager
"""

from pathlib import Path

from core.config import settings
from providers.voice_manifest import voice_manifest_provider
from schemas.voice_manifest import VoiceManifest


class VoiceManager:

    def __init__(self):

        self.root = settings.paths.voices

    # --------------------------------------------------

    def scan(self) -> list[VoiceManifest]:

        voices = []

        if not self.root.exists():
            return voices

        for gender in self.root.iterdir():

            if not gender.is_dir():
                continue

            for voice in gender.iterdir():

                if not voice.is_dir():
                    continue

                manifest = voice / "manifest.yaml"

                if not manifest.exists():
                    continue

                voices.append(
                    voice_manifest_provider.load(manifest)
                )

        return voices

    # --------------------------------------------------

    def default(self) -> VoiceManifest | None:

        for voice in self.scan():

            if voice.default:

                return voice

        return None

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

    def exists(
        self,
        voice_id: str,
    ) -> bool:

        return self.get(voice_id) is not None


voice_manager = VoiceManager()
