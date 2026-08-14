from pathlib import Path

import yaml

from schemas.voice_manifest import VoiceManifest


class VoiceManifestProvider:

    @staticmethod
    def load(path: Path) -> VoiceManifest:

        with open(path, "r", encoding="utf-8") as f:

            data = yaml.safe_load(f)

        return VoiceManifest(**data)


voice_manifest_provider = VoiceManifestProvider()
