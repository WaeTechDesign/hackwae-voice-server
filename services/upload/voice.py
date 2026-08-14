"""
HackWae Voice Server

Voice Upload Service
"""

from pathlib import Path

from schemas.voice_manifest import VoiceManifest

from services.upload.extractor import extractor
from services.upload.temp import temporary
from services.upload.validator import validator

from services.voice.creator import creator
from services.voice.manager import voice_manager


class VoiceUploadService:

    # --------------------------------------------------

    def upload_zip(

        self,

        archive: Path,

    ) -> VoiceManifest:

        temp_dir = temporary.create()

        try:

            extractor.extract(

                archive=archive,

                output=temp_dir,

            )

            voice_dir = self._find_voice_directory(

                temp_dir,

            )

            if voice_dir is None:

                raise ValueError(

                    "Voice package tidak memiliki "
                    "voice.wav dan voice.json."

                )

            manifest = validator.validate_voice(

                voice_dir,

            )

            # --------------------------------------
            # Duplicate protection
            # --------------------------------------

            existing = voice_manager.get(

                manifest.id

            )

            if existing is not None:

                raise FileExistsError(

                    f"Voice '{manifest.id}' "
                    "sudah terpasang."

                )

            # --------------------------------------

            source = voice_dir / "voice.wav"

            return creator.create(

                manifest=manifest,

                source=source,

            )

        finally:

            temporary.remove(temp_dir)

    # --------------------------------------------------

    def _find_voice_directory(

        self,

        root: Path,

    ) -> Path | None:

        if validator.voice(root):

            return root

        for path in root.rglob("*"):

            if not path.is_dir():

                continue

            if validator.voice(path):

                return path

        return None


voice_upload = VoiceUploadService()
