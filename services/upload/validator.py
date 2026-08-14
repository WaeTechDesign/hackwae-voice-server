"""
HackWae Voice Server

Upload Validator
"""

import json
import wave

from pathlib import Path

from schemas.voice_manifest import VoiceManifest
from schemas.manifest import ModelManifest

from providers.manifest import manifest_provider


class UploadValidator:

    # ==================================================
    # VOICE
    # ==================================================

    def voice(
        self,
        directory: Path,
    ) -> bool:

        voice_file = directory / "voice.wav"

        metadata = directory / "voice.json"

        return (
            voice_file.is_file()
            and metadata.is_file()
        )

    # --------------------------------------------------

    def validate_voice(
        self,
        directory: Path,
    ) -> VoiceManifest:

        voice_file = directory / "voice.wav"

        metadata = directory / "voice.json"

        # ------------------------------------------
        # Required files
        # ------------------------------------------

        if not voice_file.is_file():

            raise ValueError(
                "voice.wav tidak ditemukan."
            )

        if not metadata.is_file():

            raise ValueError(
                "voice.json tidak ditemukan."
            )

        # ------------------------------------------
        # Load JSON
        # ------------------------------------------

        try:

            with open(
                metadata,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

        except json.JSONDecodeError as exc:

            raise ValueError(
                "voice.json bukan JSON yang valid."
            ) from exc

        # ------------------------------------------
        # Validate schema
        # ------------------------------------------

        try:

            manifest = VoiceManifest(
                **data
            )

        except Exception as exc:

            raise ValueError(
                "Voice metadata tidak valid."
            ) from exc

        # ------------------------------------------
        # Validate identifier
        # ------------------------------------------

        self._validate_identifier(
            manifest.id,
            "Voice ID",
        )

        # ------------------------------------------
        # Normalize identifier
        # ------------------------------------------

        manifest.id = manifest.id.lower()

        # ------------------------------------------
        # Validate gender
        # ------------------------------------------

        if not manifest.gender.strip():

            raise ValueError(
                "Voice gender tidak boleh kosong."
            )

        # ------------------------------------------
        # Validate language
        # ------------------------------------------

        if not manifest.language:

            raise ValueError(
                "Voice language tidak boleh kosong."
            )

        # ------------------------------------------
        # Validate sample rate
        # ------------------------------------------

        if manifest.sample_rate <= 0:

            raise ValueError(
                "Voice sample rate tidak valid."
            )

        # ------------------------------------------
        # Validate WAV
        # ------------------------------------------

        try:

            with wave.open(
                str(voice_file),
                "rb",
            ) as audio:

                sample_rate = (
                    audio.getframerate()
                )

                channels = (
                    audio.getnchannels()
                )

                frames = (
                    audio.getnframes()
                )

        except (
            wave.Error,
            EOFError,
        ) as exc:

            raise ValueError(
                "voice.wav bukan file WAV yang valid."
            ) from exc

        # ------------------------------------------
        # Sample rate
        # ------------------------------------------

        if sample_rate != manifest.sample_rate:

            raise ValueError(

                "Sample rate audio tidak sesuai "
                "dengan voice.json."

            )

        # ------------------------------------------
        # Channels
        # ------------------------------------------

        if channels < 1:

            raise ValueError(
                "Audio tidak memiliki channel."
            )

        # ------------------------------------------
        # Empty audio
        # ------------------------------------------

        if frames <= 0:

            raise ValueError(
                "Audio kosong."
            )

        return manifest

    # ==================================================
    # MODEL
    # ==================================================

    def model(
        self,
        directory: Path,
    ) -> bool:

        manifest = (
            directory / "manifest.yaml"
        )

        return manifest.is_file()

    # --------------------------------------------------

    def validate_model(
        self,
        directory: Path,
    ) -> ModelManifest:

        manifest_file = (
            directory / "manifest.yaml"
        )

        # ------------------------------------------
        # Required manifest
        # ------------------------------------------

        if not manifest_file.is_file():

            raise ValueError(
                "manifest.yaml tidak ditemukan."
            )

        # ------------------------------------------
        # Load manifest
        # ------------------------------------------

        try:

            manifest = manifest_provider.load(
                manifest_file
            )

        except Exception as exc:

            raise ValueError(
                "manifest.yaml tidak valid."
            ) from exc

        # ------------------------------------------
        # Empty manifest
        # ------------------------------------------

        if manifest is None:

            raise ValueError(
                "Model manifest kosong."
            )

        # ------------------------------------------
        # Schema validation
        # ------------------------------------------

        if not isinstance(
            manifest,
            ModelManifest,
        ):

            try:

                manifest = ModelManifest(
                    **manifest.model_dump()
                )

            except Exception as exc:

                raise ValueError(
                    "Model manifest tidak "
                    "sesuai schema."
                ) from exc

        # ------------------------------------------
        # Validate model ID
        # ------------------------------------------

        self._validate_identifier(
            manifest.id,
            "Model ID",
        )

        # ------------------------------------------
        # Validate engine
        # ------------------------------------------

        self._validate_identifier(
            manifest.engine,
            "Engine",
        )

        # ------------------------------------------
        # Normalize identifiers
        # ------------------------------------------

        manifest.id = (
            manifest.id.lower()
        )

        manifest.engine = (
            manifest.engine.lower()
        )

        # ------------------------------------------
        # Validate name
        # ------------------------------------------

        if not manifest.name.strip():

            raise ValueError(
                "Model name tidak boleh kosong."
            )

        # ------------------------------------------
        # Validate version
        # ------------------------------------------

        if not manifest.version.strip():

            raise ValueError(
                "Model version tidak boleh kosong."
            )

        return manifest

    # ==================================================
    # IDENTIFIER VALIDATION
    # ==================================================

    def _validate_identifier(
        self,
        value: str,
        label: str,
    ) -> None:

        # ------------------------------------------
        # Empty
        # ------------------------------------------

        if not value:

            raise ValueError(
                f"{label} tidak boleh kosong."
            )

        # ------------------------------------------
        # Length
        # ------------------------------------------

        if len(value) > 100:

            raise ValueError(
                f"{label} terlalu panjang."
            )

        # ------------------------------------------
        # Path traversal
        # ------------------------------------------

        if (
            "/" in value
            or "\\" in value
            or ".." in value
        ):

            raise ValueError(
                f"{label} tidak valid."
            )

        # ------------------------------------------
        # Special identifiers
        # ------------------------------------------

        if value in (
            ".",
            "..",
        ):

            raise ValueError(
                f"{label} tidak valid."
            )


validator = UploadValidator()
