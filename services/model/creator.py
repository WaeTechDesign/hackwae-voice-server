"""
HackWae Voice Server

Model Creator
"""

import shutil

from pathlib import Path

from core.config import settings

from schemas.manifest import ModelManifest

from providers.manifest import manifest_provider


class ModelCreator:

    # --------------------------------------------------

    def create(
        self,
        manifest: ModelManifest,
        source: Path,
    ) -> ModelManifest:

        directory = (
            settings.paths.models
            / manifest.engine
        )

        # ------------------------------------------
        # Duplicate protection
        # ------------------------------------------

        if directory.exists():

            raise FileExistsError(
                f"Model engine '{manifest.engine}' "
                "sudah terpasang."
            )

        directory.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:

            # --------------------------------------
            # Copy model files
            # --------------------------------------

            shutil.copytree(
                source,
                directory,
            )

            # --------------------------------------
            # Save normalized manifest
            # --------------------------------------

            manifest_path = (
                directory / "manifest.yaml"
            )

            import yaml

            with open(
                manifest_path,
                "w",
                encoding="utf-8",
            ) as file:

                yaml.safe_dump(
                    manifest.model_dump(),
                    file,
                    allow_unicode=True,
                    sort_keys=False,
                )

            return manifest

        except Exception:

            # --------------------------------------
            # Rollback partial installation
            # --------------------------------------

            if directory.exists():

                shutil.rmtree(
                    directory,
                    ignore_errors=True,
                )

            raise


creator = ModelCreator()
