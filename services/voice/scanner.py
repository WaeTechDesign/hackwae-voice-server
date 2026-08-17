"""
HackWae Voice Server

Voice Scanner
"""

from pathlib import Path

from core.config import settings
from schemas.voice_manifest import VoiceManifest
from providers.voice_manifest import voice_manifest_provider
from services.voice.database import database


class VoiceScanner:

    # --------------------------------------------------

    def scan(self) -> list[VoiceManifest]:

        voices = []

        root = settings.paths.voices

        if not root.exists():
            return voices

        for gender_dir in root.iterdir():

            if not gender_dir.is_dir():
                continue

            for voice_dir in gender_dir.iterdir():

                if not voice_dir.is_dir():
                    continue

                voice = self.load(
                    directory=voice_dir,
                    gender=gender_dir.name,
                )

                if voice is not None:
                    voices.append(voice)

        return voices

    # --------------------------------------------------

    def load(
        self,
        directory: Path,
        gender: str,
    ) -> VoiceManifest | None:

        voice_file = directory / "voice.wav"

        if not voice_file.exists():
            return None

        # ------------------------------------------
        # Preferred: manifest.yaml
        # ------------------------------------------

        manifest = directory / "manifest.yaml"

        if manifest.exists():

            return voice_manifest_provider.load(
                manifest
            )

        # ------------------------------------------
        # Legacy: voice.json
        # ------------------------------------------

        metadata = directory / "voice.json"

        if metadata.exists():

            data = database.load(metadata)

            if data is not None:
                return VoiceManifest(**data)

        # ------------------------------------------
        # Fallback: Legacy Voice
        # ------------------------------------------

        return VoiceManifest(
            id=directory.name,
            name=directory.name.capitalize(),
            gender=gender,
            language=["id"],
            author="Unknown",
            description="",
            sample_rate=24000,
            engines=["chatterbox"],
            default=False,
            enabled=True,
        )


scanner = VoiceScanner()
