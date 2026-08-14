"""
HackWae Voice Server

Voice Validator
"""

from pathlib import Path


class VoiceValidator:

    # --------------------------------------------------

    def validate(
        self,
        directory: Path,
    ) -> bool:

        required = (

            "voice.wav",

            "voice.json",

        )

        for filename in required:

            if not (directory / filename).exists():

                return False

        return True


validator = VoiceValidator()
