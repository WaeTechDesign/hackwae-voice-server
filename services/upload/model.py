"""
HackWae Voice Server

Model Upload Service
"""

from pathlib import Path

from core.engine_loader import engine_loader

from schemas.manifest import ModelManifest

from services.model.creator import creator
from services.model_manager import model_manager

from services.upload.extractor import extractor
from services.upload.temp import temporary
from services.upload.validator import validator

from utils.logger import logger


class ModelUploadService:

    # ==================================================
    # UPLOAD MODEL ZIP
    # ==================================================

    def upload_zip(
        self,
        archive: Path,
    ) -> dict:

        temp_dir = temporary.create()

        try:

            # ------------------------------------------
            # Extract
            # ------------------------------------------

            extractor.extract(

                archive=archive,

                output=temp_dir,

            )

            # ------------------------------------------
            # Find model directory
            # ------------------------------------------

            model_dir = (
                self._find_model_directory(
                    temp_dir
                )
            )

            if model_dir is None:

                raise ValueError(
                    "Model package tidak memiliki "
                    "manifest.yaml."
                )

            # ------------------------------------------
            # Validate manifest
            # ------------------------------------------

            manifest = (
                validator.validate_model(
                    model_dir
                )
            )

            # ------------------------------------------
            # Duplicate protection
            # ------------------------------------------

            existing = model_manager.get(
                manifest.engine
            )

            if existing is not None:

                raise FileExistsError(

                    f"Model engine "
                    f"'{manifest.engine}' "
                    "sudah terpasang."

                )

            # ------------------------------------------
            # Install model
            # ------------------------------------------

            installed = creator.create(

                manifest=manifest,

                source=model_dir,

            )

            logger.success(

                f"Model installed: "
                f"{installed.engine}"

            )

            # ------------------------------------------
            # Register engine
            # ------------------------------------------

            engine_registered = False

            engine_error = None

            try:

                engine_loader.register(

                    installed.engine

                )

                engine_registered = True

                logger.success(

                    f"Engine registered after "
                    f"model upload: "
                    f"{installed.engine}"

                )

            except Exception as exc:

                engine_error = str(exc)

                logger.warning(

                    f"Model installed but engine "
                    f"'{installed.engine}' "
                    f"could not be registered: "
                    f"{exc}"

                )

            # ------------------------------------------
            # Result
            # ------------------------------------------

            return {

                "manifest": installed,

                "engine_registered": (
                    engine_registered
                ),

                "engine_error": engine_error,

            }

        finally:

            temporary.remove(

                temp_dir

            )

    # ==================================================
    # FIND MODEL DIRECTORY
    # ==================================================

    def _find_model_directory(

        self,

        root: Path,

    ) -> Path | None:

        # ------------------------------------------
        # ZIP contains manifest directly
        # ------------------------------------------

        if validator.model(root):

            return root

        # ------------------------------------------
        # ZIP contains nested directory
        # ------------------------------------------

        for path in root.rglob(
            "manifest.yaml"
        ):

            if path.is_file():

                return path.parent

        return None


model_upload = ModelUploadService()
