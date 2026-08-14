"""
HackWae Voice Server

Manifest Provider
"""

from pathlib import Path

import yaml

from schemas.manifest import ModelManifest


class ManifestProvider:

    # --------------------------------------------------
    # LOAD
    # --------------------------------------------------

    @staticmethod
    def load(
        path: Path,
    ) -> ModelManifest:

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:

            data = yaml.safe_load(f)

        return ModelManifest(
            **data
        )

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    @staticmethod
    def save(
        path: Path,
        manifest: ModelManifest,
    ) -> None:

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as f:

            yaml.safe_dump(
                manifest.model_dump(),
                f,
                allow_unicode=True,
                sort_keys=False,
            )


manifest_provider = ManifestProvider()
