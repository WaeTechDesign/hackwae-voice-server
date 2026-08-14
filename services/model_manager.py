"""
HackWae Voice Server

Model Manager
"""

from pathlib import Path

from core.config import settings
from providers.filesystem import filesystem
from providers.manifest import manifest_provider
from schemas.manifest import ModelManifest
from utils.logger import logger


class ModelManager:

    def __init__(self):
        self.models_root = settings.paths.models

    # --------------------------------------------------

    def engine_path(self, engine: str) -> Path:
        return filesystem.model_path(engine)

    # --------------------------------------------------

    def exists(self, engine: str) -> bool:
        return self.engine_path(engine).exists()

    # --------------------------------------------------

    def list_engines(self) -> list[str]:

        return [
            item.name
            for item in filesystem.list_directories(
                self.models_root
            )
        ]

    # --------------------------------------------------

    def manifest_path(self, engine: str) -> Path:

        return self.engine_path(engine) / "manifest.yaml"

    # --------------------------------------------------

    def load_manifest(
        self,
        engine: str,
    ) -> ModelManifest | None:

        manifest = self.manifest_path(engine)

        if not manifest.exists():
            return None

        return manifest_provider.load(manifest)

    # --------------------------------------------------

    def default_model(self) -> ModelManifest | None:

        for model in self.scan():

            if model.default:
                return model

        return None

    # --------------------------------------------------

    def get(
        self,
        engine: str,
    ) -> ModelManifest | None:

        return self.load_manifest(engine)

    # --------------------------------------------------

    def scan(self) -> list[ModelManifest]:

        logger.info("Scanning installed models...")

        models = []

        for engine in self.list_engines():

            manifest = self.load_manifest(engine)

            if manifest is None:
                continue

            models.append(manifest)

        return models


model_manager = ModelManager()
