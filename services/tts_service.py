"""
HackWae Voice Server

TTS Service
"""

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from core.config import settings

from services.engine_service import engine_service
from services.voice_service import voice_service
from services.history_service import history_service

from schemas.history import HistoryItem

from utils.file_name import generate_audio_filename


class TTSService:

    # ==================================================
    # GENERATE
    # ==================================================

    def generate(
        self,
        text: str,
        voice: str = "putri",
        engine: str = "chatterbox",
        output: str | None = None,
    ):

        # ----------------------------------------------
        # Normalize
        # ----------------------------------------------

        text = text.strip()
        voice = voice.strip()
        engine = engine.strip().lower()

        # ----------------------------------------------
        # Validate text
        # ----------------------------------------------

        if not text:
            raise ValueError(
                "Text tidak boleh kosong."
            )

        # ----------------------------------------------
        # Validate engine
        # ----------------------------------------------

        ai = engine_service.get(engine)

        if ai is None:
            raise ValueError(
                f"Engine '{engine}' tidak ditemukan."
            )

        # ----------------------------------------------
        # Validate voice
        # ----------------------------------------------

        speaker = voice_service.get(voice)

        if speaker is None:
            raise ValueError(
                f"Voice '{voice}' tidak ditemukan."
            )

        # ----------------------------------------------
        # Resolve output
        # ----------------------------------------------

        output_path = self._resolve_output(
            output
        )

        # ----------------------------------------------
        # Generate
        # ----------------------------------------------

        result = ai.generate(
            text=text,
            voice=speaker,
            output=output_path,
        )

        # ----------------------------------------------
        # Save history
        # ----------------------------------------------

        history_service.add(
            HistoryItem(
                id=uuid4().hex,
                filename=result.name,
                text=text,
                voice=voice,
                engine=engine,
                sample_rate=24000,
                created=datetime.now(),
            )
        )

        return {
            "filename": result.name,
            "path": result,
        }

    # ==================================================
    # OUTPUT
    # ==================================================

    def _resolve_output(
        self,
        output: str | None,
    ) -> Path:

        history_root = (
            settings.paths.history
        ).resolve()

        history_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ----------------------------------------------
        # Automatic filename
        # ----------------------------------------------

        if output is None:

            # Generate until we get a filename
            # that does not already exist.
            for _ in range(10):

                filename = (
                    generate_audio_filename()
                )

                final_path = (
                    history_root / filename
                ).resolve()

                try:
                    final_path.relative_to(
                        history_root
                    )
                except ValueError:
                    continue

                if not final_path.exists():
                    return final_path

            raise RuntimeError(
                "Gagal membuat nama file audio "
                "yang unik."
            )

        # ----------------------------------------------
        # User supplied filename
        # ----------------------------------------------

        if not isinstance(output, str):
            raise ValueError(
                "Output filename harus berupa string."
            )

        output = output.strip()

        if not output:
            raise ValueError(
                "Output filename tidak boleh kosong."
            )

        requested = Path(output)

        # ----------------------------------------------
        # Only allow filename
        # ----------------------------------------------

        if (
            requested.name != output
            or requested.parent != Path(".")
        ):
            raise ValueError(
                "Output hanya boleh berupa "
                "nama file, bukan path directory."
            )

        # ----------------------------------------------
        # Prevent traversal / separators
        # ----------------------------------------------

        if requested.name in (
            "",
            ".",
            "..",
        ):
            raise ValueError(
                "Output filename tidak valid."
            )

        if (
            "/" in output
            or "\\" in output
        ):
            raise ValueError(
                "Output filename tidak boleh "
                "mengandung path separator."
            )

        # ----------------------------------------------
        # Extension
        # ----------------------------------------------

        if not requested.suffix:
            requested = requested.with_suffix(
                ".wav"
            )

        if requested.suffix.lower() != ".wav":
            raise ValueError(
                "Output file harus menggunakan "
                "format WAV."
            )

        # ----------------------------------------------
        # Final path
        # ----------------------------------------------

        final_path = (
            history_root
            / requested.name
        ).resolve()

        # ----------------------------------------------
        # Final containment check
        # ----------------------------------------------

        try:
            final_path.relative_to(
                history_root
            )
        except ValueError as exc:
            raise ValueError(
                "Output path tidak valid."
            ) from exc

        # ----------------------------------------------
        # Prevent overwrite
        # ----------------------------------------------

        if final_path.exists():
            raise FileExistsError(
                f"Output file '{requested.name}' "
                "sudah ada."
            )

        return final_path


tts_service = TTSService()
