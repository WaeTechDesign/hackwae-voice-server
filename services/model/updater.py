"""
HackWae Voice Server

Model Updater
"""

from pathlib import Path

from providers.manifest import manifest_provider

from schemas.manifest import ModelManifest


class ModelUpdater:

    # --------------------------------------------------

    def update(

        self,

        directory: Path,

        manifest: ModelManifest,

    ) -> ModelManifest:

        manifest_provider.save(

            directory / "manifest.yaml",

            manifest,

        )

        return manifest


updater = ModelUpdater()
